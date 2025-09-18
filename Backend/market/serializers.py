
from rest_framework import serializers
from .models import (Product,Owner,
                     ProductMessage,
                     ProductComments,
                     Testimonials,
                     Consultant,ConsultantPost,
                     Order,RequestTobeOwer,
                     CustomerSupport,OrderItem,
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

    class Meta:
        model=Product
        fields=["id","product_name","description","price","quantity","product_image","owner"]
        extra_kwargs = {
           "id": {"read_only": True},
           "owner": {"read_only": True},
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



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields=["product","quantity"]




class OrderSerialzier(serializers.ModelSerializer):
      items=OrderItemSerializer(many=True)

      class Meta:
          model=Order
          fields=["id","user","items","address","created_at"]
          read_only_fields = ["id", "user", "created_at"]

      def create(self, validated_data):
          request=self.context.get("request")
          user=request.user
          items_data=validated_data.pop("items")
          order=Order.objects.create(user=user,**validated_data)


          for item in items_data:
              product=item["product"]
              quantity=item["quantity"]

              if product.quantity<quantity: 
                  raise serializers.ValidationError({
                      "error":f" not enough stock for {product.product_name} availbale quantity {product.quantity}  requested {quantity}"
                  })
              product.quantity -=quantity
              product.save()
              OrderItem.objects.create(order=order, product=product,quantity=quantity)
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









class ConsultantPostSerializer(serializers.ModelSerializer):
     class Meta:
         model=ConsultantPost
         fields=["id","consultant","post_title","post_description","post_image","created_at"]


     def validate(self, data):
             if not data.get("post_description") and not data.get("post_image"):
                 raise serializers.ValidationError("Either post description or post image must be provided.")
             return data





class ConsultantSerializer(serializers.ModelSerializer):
    user=serializers.StringRelatedField()
    posts=ConsultantPostSerializer(many=True,read_only=True)
    followers_count=serializers.SerializerMethodField()
    class Meta:
        model=Consultant
        fields=["id","user","location","posts","followers_count"]


    def get_followers_count(self,obj):
        return obj.followers.count()
        






