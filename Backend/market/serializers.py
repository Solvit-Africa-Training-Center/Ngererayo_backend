
from rest_framework import serializers
from .models import (Product,Owner,
                     ProductMessage,
                     ProductComments,
                     Testimonials,
                     Order,RequestTobeOwer,
                     CustomerSupport,
                     CartItem, Cart)
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

    def validate(self, data):
         product=data['product']
         quantity=data["quantity"]

         if quantity > product.quantity:
             raise serializers.ValidationError({"quantity":f" only {product.quantity} available products in stock"})
         cart=self.context.get("cart")
         if cart:
             existing_item=CartItem.objects.filter(cart=cart,product=product).first()
             if existing_item:
                 new_total_quantity=existing_item.quantity+quantity
                 if new_total_quantity > product.quantity:
                     raise serializers.ValidationError({"quantity":f" you already have {existing_item.quantity} in cart   and only {product.quantity} available products in stock"})
                 existing_item.quantity=new_total_quantity
                 existing_item.save()

  

         return data     
    


class CartSerializer(serializers.ModelSerializer):
    item=CartItemSerilizer(source="cartitem_set",many=True)

    class Meta:
        model= Cart
        fields=["id","user","item","session_key"]


    # ...................... place order serializer ........................................


class OrderSerialzier(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields=["id","user","cart","address","created_at"]
        read_only_fields = ["id", "user", "created_at"]
    def create(self, validated_data):
        request=self.context["request"]
        user=request.user
        cart=validated_data["cart"]


        if   cart.cartitem_set.exists():
            raise serializers.ValidationError({"cart":f"you can not place order without any product in cart"})
        



        for item in cart.cartitem_set.all():
            if item.quantity >item.product.quantity:
                raise serializers.ValidationError(f"Not enough stock for {item.product.product_name} but available {item.product.quantity} requested {item.quantity}")
            




        for item in cart.cartitem_set.all():
            item.product.quantity -=item.quantity
            item.product.save()


        # user = self.context['request'].user

        order=Order.objects.create(user=user,**validated_data)
        cart.cartitem_set.all().delete()
        return order





class RequestTobeOwerSerializer(serializers.ModelSerializer):
    class Meta:
        model=RequestTobeOwer
        fields=["id","user","farming_name","location","license","national_id","status"]
        read_only_fields = ["id", "user"]
    def create(self, validated_data):
        request = self.context.get("request")
        return RequestTobeOwer.objects.create(user=request.user, **validated_data)

             










class ProductMessageSerializer(serializers.ModelSerializer):
     sender=serializers.ReadOnlyField(source='sender.username')
     receiver=serializers.ReadOnlyField(source='receiver.farming_name')
     class Meta:
         model=ProductMessage
         fields=["id","sender","receiver","message","created_at","is_read","parent"]




class ProductCommentsSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    product=serializers.ReadOnlyField(source='product.product_name')
    class Meta:
        model=ProductComments
        fields=["id","user","product","comment","created_at","updated_at"]





class TestimonialsSerializer(serializers.ModelSerializer):
      class Meta:
          model=Testimonials
          fields=["id","user","content","created_at"]
          read_only_fields = ["id", "user", "created_at"]





class CustomerSupportSerializer(serializers.ModelSerializer):
    full_name=serializers.CharField(required=True)
    email=serializers.EmailField(required=True)
    status=serializers.ChoiceField(choices=CustomerSupport.STATUS_CHOICES,required=True)
    subject=serializers.CharField(required=True)
    message=serializers.CharField(required=True)
    class Meta:
        model=CustomerSupport
        fields=["id","full_name","email","status","subject","message","created_at"]



    def create(self, validated_data):
        support=CustomerSupport.objects.create(
            full_name=validated_data["full_name"],
            email=validated_data["email"],
            status=validated_data["status"],
            subject=validated_data["subject"],
            message=validated_data["message"],

        )
        return support    


