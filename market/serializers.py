from .models import CartItem, Product, Cart
from rest_framework import serializers


class CartItemSerilizer(serializers.ModelSerializer):
    product_name=serializers.CharField(source="product.product_name", read_only=True)

    class Meta:
        model= CartItem
        fields=["id","product", "product_name", "quantity",]



class CartSerializer(serializers.ModelSerializer):
    item=CartItemSerilizer(source="cartitem_set",many=True)

    class Meta:
        model= Cart
        fields=["id","user","item",]

