
from rest_framework.response import Response
from rest_framework import viewsets,status,generics
from rest_framework.views import APIView
from rest_framework import permissions

from .serializers import ProductSerializer,OwnerSerialzer,CartSerializer, CartItemSerilizer
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


def get_user_cart(user):
    cart, created = Cart.objects.get_or_create(user=user)
    return cart

class CartView(generics.RetrieveAPIView):
    serializer_class = CartSerializer

    def get_object(self):
        return get_user_cart(self.request.user)


class AddToCartView(generics.GenericAPIView):
    serializer_class = CartItemSerilizer

    def post(self, request, *args, **kwargs):
        product_id = request.data.get("product_id")
        quantity = int(request.data.get("quantity", 1))

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found please find other one"}, status=status.HTTP_404_NOT_FOUND)

        cart = get_user_cart(request.user)
        
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        cart_item.save()

        return Response(CartItemSerilizer(cart_item).data, status=status.HTTP_201_CREATED)
