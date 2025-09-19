from drf_yasg.utils import swagger_auto_schema
from rest_framework.response import Response
from rest_framework import status,generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from django.core.exceptions import PermissionDenied
from .models import ProductMessage, Product,ProductComments
from django.shortcuts import get_object_or_404

from .serializers import  ProductMessageSerializer,ProductCommentsSerializer





class ProductMessageView(generics.ListCreateAPIView):
    serializer_class=ProductMessageSerializer
    permission_classes=[permissions.IsAuthenticated] 

    def get_queryset(self):
        product_id = self.kwargs["product_id"]
        product = Product.objects.get(id=product_id)
        
        if product.owner.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this product.")
        
    
        return ProductMessage.objects.filter(product=product, parent=None).order_by("-created_at")




class SendProductMessageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        message_text = request.data.get("message")
        if not message_text:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        product = get_object_or_404(Product, id=product_id)
        sender = request.user                 
        receiver = product.owner.user

        if receiver is None:
            return Response({"error": "Product has no owner"}, status=status.HTTP_400_BAD_REQUEST)

        message = ProductMessage.objects.create(
            product=product,
            sender=sender,
            receiver=receiver,
            message=message_text
        )

        return Response({
            "id": message.id,
            "product": product.product_name,
            "sender": sender.username,
            "receiver": receiver.username,
            "message": message.message,
            "created_at": message.created_at
        }, status=status.HTTP_201_CREATED)

class DeleteProductMessageView(APIView):
    def delete(self, request, message_id):
        message = get_object_or_404(ProductMessage, id=message_id)
        if message.sender != request.user:
            return Response({"error": "You do not have permission to delete this message."}, status=status.HTTP_403_FORBIDDEN)
        message.delete()
        return Response({"message": "Message deleted successfully."}, status=status.HTTP_200_OK)



class EditProductMessageView(APIView):
    permission_classes = [IsAuthenticated]
    def put(self, request, message_id):
        message = get_object_or_404(ProductMessage, id=message_id)
        if message.sender != request.user:
            return Response({"error": "You do not have permission to edit this message."}, status=status.HTTP_403_FORBIDDEN)
        new_text = request.data.get("message")
        if not new_text:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)
        message.message = new_text
        message.save()
        return Response({"message": "Message updated successfully."}, status=status.HTTP_200_OK)
class GetMessageYouSent(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request,product_id):
        messages=ProductMessage.objects.filter(product_id=product_id,sender=request.user)
        serializer=ProductMessageSerializer(messages,many=True)
        return Response(serializer.data)
    
    

class ReplayMessage(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, message_id):
        reply_text = request.data.get("message")
        if not reply_text:
            return Response({"error": "Message is required"}, status=status.HTTP_400_BAD_REQUEST)

        original_message = ProductMessage.objects.filter(id=message_id).first()
        if not original_message:
            return Response({"error": "Original message not found"}, status=status.HTTP_404_NOT_FOUND)

        sender = request.user

        # ✅ Create reply with parent=original_message
        reply_message = ProductMessage.objects.create(
            product=original_message.product,
            sender=sender,
            receiver=original_message.sender,  # reply goes to original sender
            message=reply_text,
            parent=original_message           # ✅ Link reply to parent
        )

        return Response({
            "id": reply_message.id,
            "product": reply_message.product.product_name,
            "sender": reply_message.sender.username,
            "receiver": reply_message.receiver.username,
            "message": reply_message.message,
            "created_at": reply_message.created_at
        }, status=status.HTTP_201_CREATED)




class GetSendMessage(APIView):
    def get(self,request,product_id):
        message=ProductMessage.objects.filter(product_id=product_id)
        serializer=ProductMessageSerializer(message,many=True)
        return Response(serializer.data)

class GetReplyMessage(APIView):
    def get(self, request, message_id):
         replies=ProductMessage.objects.filter(parent_id=message_id)
         serializer = ProductMessageSerializer(replies, many=True)
         return Response(serializer.data)

class SendProductCommentsView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request, product_id):
        try:
            comment=request.data.get("comment")
            if not comment:
                return Response({"error": "Comment is required"}, status=status.HTTP_400_BAD_REQUEST)

            product = get_object_or_404(Product, id=product_id)
            user = request.user if request.user.is_authenticated else None

            comment = ProductComments.objects.create(
                product=product,
                user=user,
                comment=comment
            )

            return Response({
                "id": comment.id,
                "product": product.product_name,
                "user": user.username if user else "Anonymous",
                "comment": comment.comment,
                "created_at": comment.created_at,
                "updated_at": comment.updated_at
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class ReplyProductComments(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self,request,comment_id):
        try:
            replay_comment=request.data.get("comment")
            if not replay_comment:
                return Response({"error": "Comment is required"}, status=status.HTTP_400_BAD_REQUEST)
            original_comment=ProductComments.objects.filter(id=comment_id).first()
            if not original_comment:
                return Response({"error": "Comment not found"}, status=status.HTTP_404_NOT_FOUND)
            user = request.user if request.user.is_authenticated else None
            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
            
            reply_comment = ProductComments.objects.create(
                product=original_comment.product,
                user=user,
                comment=replay_comment,
                parent=original_comment
            )
            return Response({
                "id": reply_comment.id,
                "product": reply_comment.product.product_name,
                "user": user.username,
                "comment": reply_comment.comment,
                "created_at": reply_comment.created_at,
                "updated_at": reply_comment.updated_at
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)




class GetProductCommentsView(APIView):
    

    def get(self, request, product_id):
        comments = ProductComments.objects.filter(product_id=product_id, parent=None)
        serializer = ProductCommentsSerializer(comments, many=True)
        return Response(serializer.data)


class GetProductCommentsReplyView(APIView):
    

    def get(self, request, comment_id):
        replies = ProductComments.objects.filter(parent_id=comment_id)
        serializer = ProductCommentsSerializer(replies, many=True)
        return Response(serializer.data)
