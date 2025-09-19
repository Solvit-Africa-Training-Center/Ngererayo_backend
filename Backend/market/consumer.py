import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Product, ProductMessage


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.product_id = self.scope['url_route']['kwargs']['product_id']
        self.chat_group_name = f"chat_{self.product_id}"

        # Add this connection to the group
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove this connection from the group
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        parent_id = data.get("parent_id")  # Optional for replies
        sender = self.scope.get("user")

        if sender is None or sender.is_anonymous:
            await self.send(text_data=json.dumps({"error": "Authentication required"}))
            return

        product = await self.get_product(self.product_id)
        receiver = await self.get_receiver(product, sender)

        if not receiver:
            return

        parent_message = None
        if parent_id:
            parent_message = await self.get_message(parent_id)

        # Save the message (normal or reply)
        saved_message = await self.save_message(
            product, sender, receiver, message, parent=parent_message
        )

        # Broadcast message to all clients in the group
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                "type": "chat_message",
                "id": saved_message.id,
                "product": product.product_name,
                "sender": sender.username,
                "receiver": receiver.username,
                "message": saved_message.message,
                "parent_id": parent_message.id if parent_message else None,
                "created_at": str(saved_message.created_at),
            }
        )

    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps(event))

    # ----------------- Database helpers -----------------

    @database_sync_to_async
    def get_product(self, product_id):
        return Product.objects.select_related("owner__user").get(id=product_id)

    @database_sync_to_async
    def get_receiver(self, product, sender):
        """
        Returns the product owner if sender is not owner,
        else None
        """
        try:
            owner_user = product.owner.user
            return owner_user if sender != owner_user else None
        except Exception:
            return None

    @database_sync_to_async
    def get_message(self, message_id):
        try:
            return ProductMessage.objects.get(id=message_id)
        except ProductMessage.DoesNotExist:
            return None

    @database_sync_to_async
    def save_message(self, product, sender, receiver, message, parent=None):
        return ProductMessage.objects.create(
            product=product,
            sender=sender,
            receiver=receiver,
            message=message,
            parent=parent  # Link reply to parent if provided
        )
