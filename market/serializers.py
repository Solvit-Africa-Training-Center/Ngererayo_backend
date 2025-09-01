
from rest_framework import serializers
from .models import Product,Owner,CartItem, Cart
from accounts.models import CustomUser



class OwnerSerialzer(serializers.ModelSerializer):
    class Meta:
        model=Owner
        fields=["id","user","farming_name","location"]
        extra_kwargs = {
            "id": {"read_only": True},
        }  




class ProductSerializer(serializers.ModelSerializer):
    owner=OwnerSerialzer(read_only=True)
    owner_id=serializers.PrimaryKeyRelatedField(queryset=Owner.objects.all(),source='owner',write_only=True)
    

    class Meta:
        model=Product
        fields=["id","product_name","description","price","quantity","product_image","owner","owner_id"]
        extra_kwargs = {
           "id": {"read_only": True},
       }



class CartItemSerilizer(serializers.ModelSerializer):
    
    product_id=serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),source='product',write_only=True)
    product=ProductSerializer(read_only=True)

    class Meta:
        model= CartItem
        fields=["id","product_id", "quantity", "product"]





class CartSerializer(serializers.ModelSerializer):
    item=CartItemSerilizer(source="cartitem_set",many=True)

    class Meta:
        model= Cart
        fields=["id","user","item","session_key"]


