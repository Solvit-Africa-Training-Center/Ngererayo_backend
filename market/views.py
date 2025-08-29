from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cart, CartItem, Product
from .serializers import CartSerializer, CartItemSerilizer


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
