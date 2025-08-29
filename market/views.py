from rest_framework.response import Response
from rest_framework import viewsets,status,generics
from rest_framework.views import APIView
from rest_framework import permissions

from .serializers import ProductSerializer,OwnerSerialzer
from .models import *



class OwnerView(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerialzer
    permission_classes=[permissions.IsAuthenticated]




class ProductListView(APIView):
    def get(self, request):
        try:
            product=Product.objects.all()
            serializer=ProductSerializer(product,many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        


class ProductDetailView(APIView):
    def get(self, request,product_id):
        try:
            product=Product.objects.get(id=product_id)
            serializer=ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        





class ProductView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serialzier):
        owner=Owner.objects.get(user=self.request.user)
        serialzier.save(owner=owner)




class OwnerProductsView(generics.ListAPIView):
    serializer_class=ProductSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        owner_id=self.kwargs['owner_id']
        return Product.objects.filter(owner__id=owner_id)




class OwnerEditProductView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self, product_id,user):
        try:
              owner=Owner.objects.get(user=user)
              return Product.objects.get(id=product_id,owner=owner)
        except (Owner.DoesNotExist, Product.DoesNotExist):
              return None


    def get(self, request,product_id):
        try:
            product=Product.objects.get(id=product_id)
            if not product:
                return Response({"product not found": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer=ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def put(self, request,product_id):
        try:
            product=Product.objects.get(id=product_id)
            if not product:
                return Response({"product not found": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer=ProductSerializer(product,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        




class OwnerDeleteProduct(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self, product_id,user):
        try:
            owner=Owner.objects.get(user=user)
            return Product.objects.get(id=product_id,owner=owner)
        except (Owner.DoesNotExist, Product.DoesNotExist):
            return None

    def get(self, request,product_id):
        try:
            prouct=Product.objects.get(id=product_id)
            if not prouct:
                return Response({"product not found": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer=ProductSerializer(prouct)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, product_id):
        try:
            product=Product.objects.get(id=product_id)
            if not product:
                return Response({"product not found": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
