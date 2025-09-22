from rest_framework import status,permissions
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from .models import ProductComments,Product
from .serializers import ProductCommentsSerializer




class SendCommentView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request,product_id):
        comment=request.data.get("comment")
        if not comment:
            return Response("comment not found",status=status.HTTP_400_BAD_REQUEST  )
        
        user=request.user
        product=get_object_or_404(Product, product_id=product_id)

        comment=ProductComments(
            comment=comment,
            user=user,
            product=product
        )
        return Response("product comments sent successfully",status=status.HTTP_201_CREATED)
    




class CommentsRepliesView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request, comment_id):
        reply_text=request.data.get("comment")
        if not reply_text:
            return Response("reply text not found",status=status.HTTP_400_BAD_REQUEST  )
        
        user=request.user
        parent_comment=get_object_or_404(ProductComments, id=comment_id)
        product=parent_comment.product
        reply=ProductComments(
            comment=reply_text,
            user=user,
            product=product,
            parent=parent_comment
        )
        reply.save()
        return Response("reply sent successfully",status=status.HTTP_201_CREATED)



class GetCommentsView(APIView):
    permission_classes=[permissions.IsAuthenticated ]
    def get(self, request, product_id):
        product=get_object_or_404(Product, product_id=product_id)
        serializer=ProductCommentsSerializer(product.comments.all(),many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class GetOneCommentView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get(self, request, comment_id):
        comment=get_object_or_404(ProductComments, id=comment_id)
        serializer=ProductCommentsSerializer(comment)
        return Response(serializer.data,status=status.HTTP_200_OK)
    