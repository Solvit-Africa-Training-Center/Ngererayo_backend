from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status,generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from .serializers import (ProductSerializer,
                          OwnerSerialzer,CartSerializer,
                          ProductMessageSerializer,
                          CartItemSerilizer)
from .models import *






class AllProductOwnersView(APIView):
    def get(self, request):
        count = Owner.objects.count()
        return Response({"owners_count": count})



class ProductView(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        try:
            product=Product.objects.all().order_by(' created_at')[:6]
            serializer=ProductSerializer(product,many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

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




class CartView(generics.RetrieveAPIView):
    serializer_class=CartSerializer
    @swagger_auto_schema(
    tags=["Cart"],
    operation_description="Get the cart for the authenticated user"
)
    def get_object(self):
        user=self.request.user  if self.request.user.is_authenticated else None
        session_key=self.request.session.session_key or self.request.session.create()
        if user:
            cart,_=Cart.objects.get_or_create(user=user )
        else:
            cart, _=Cart.objects.get_or_create(session_key=session_key)
        return cart        
    
class DeleteItemFromcartView(APIView):
    
    def delete(self, request, cart_item_id):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)
        user = request.user if request.user.is_authenticated else None
        # session_key = request.session.session_key or request.session.create()
        if cart_item.cart.user:
            if cart_item.cart.user != user:
                raise PermissionDenied("You do not have permission to modify this cart item.")
        # else:
            # if cart_item.cart.session_key != session_key:
                # raise PermissionDenied("You do not have permission to modify this cart item.")

        cart_item.delete()
        return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)

class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerilizer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user if self.request.user.is_authenticated else None
        session_key = self.request.session.session_key or self.request.session.create()

        cart, _ = Cart.objects.get_or_create(
            user=user if user else None,
            session_key=None if user else session_key
        )
        context["cart"] = cart
        return context

    def perform_create(self, serializer):
        cart = self.get_serializer_context()["cart"]
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": quantity}
        )

        if not created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer.instance = cart_item



class UpdateQuantityOnCartView(APIView):
    def put(self, request, cart_item_id):
        try:
            cart_item = CartItem.objects.get(id=cart_item_id)
        except CartItem.DoesNotExist:
            return Response({"error": "Cart item not found"}, status=status.HTTP_404_NOT_FOUND)

        user = request.user if request.user.is_authenticated else None
        # session_key = request.session.session_key or request.session.create()

        if cart_item.cart.user:
            if cart_item.cart.user != user:
                raise PermissionDenied("You do not have permission to modify this cart item.")
        # else:
        #     if cart_item.cart.session_key != session_key:
        #         raise PermissionDenied("You do not have permission to modify this cart item.")


        new_quantity = request.data.get("quantity")
        operation = request.data.get("operation")  

        if new_quantity is not None:
            new_quantity = int(new_quantity)
            if new_quantity < 0:
                return Response({"error": "Quantity must be non-negative"}, status=status.HTTP_400_BAD_REQUEST)

            if new_quantity == 0:
                cart_item.delete()
                return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)

            if new_quantity > cart_item.product.quantity:
                return Response({"error": f"Only {cart_item.product.quantity} items available in stock"}, status=status.HTTP_400_BAD_REQUEST)

            cart_item.quantity = new_quantity

        elif operation in ["increase", "decrease"]:
            amount = int(request.data.get("amount", 1))
            if operation == "increase":
                if cart_item.quantity + amount > cart_item.product.quantity:
                    return Response({"error": f"Only {cart_item.product.quantity} items available in stock"}, status=status.HTTP_400_BAD_REQUEST)
                cart_item.quantity += amount
            elif operation == "decrease":
                if cart_item.quantity - amount < 1:
                    cart_item.delete()
                    return Response({"message": "Item removed from cart"}, status=status.HTTP_200_OK)
                cart_item.quantity -= amount
        else:
            return Response({"error": "Provide either 'quantity' or 'operation'"}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.save()
        serializer = CartItemSerilizer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)
