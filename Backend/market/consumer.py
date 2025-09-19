import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Product, ProductMessage


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.product_id = self.scope['url_route']['kwargs']['product_id']
        self.chat_group_name = f"chat_{self.product_id}"

        
        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data) 
        message = data["message"]
        sender = self.scope["user"]

        product = await self.get_product(self.product_id)
        receiver = product.owner.user if sender != product.owner.user else None

        if not receiver:
            return 

        saved_message = await self.save_message(product, sender, receiver, message)

    
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                "type": "chat_message",
                "id": saved_message.id,
                "product": product.product_name,
                "sender": sender.username,
                "receiver": receiver.username,
                "message": saved_message.message,
                "created_at": str(saved_message.created_at),
            }
        )

    async def chat_message(self, event):
   
        await self.send(text_data=json.dumps(event))

    @database_sync_to_async
    def get_product(self, product_id):
        return Product.objects.get(id=product_id)

    @database_sync_to_async
    def save_message(self, product, sender, receiver, message):
        return ProductMessage.objects.create(
            product=product,
            sender=sender,
            receiver=receiver,
            message=message
        )
