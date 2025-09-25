
from rest_framework import serializers
from .models import (Product,Owner,
                     ProductMessage,
                     ProductComments,
                     Testimonials,
                     ProductImages,
                     ConsultantFollow,
                     ProductDiscount,
                     RequestTobeConsultant,
                     Consultant,ConsultantPost,
                     Order,RequestTobeOwer,
                     CustomerSupport,OrderItem,
                     )
from accounts.models import CustomUser
# from accounts.serializers import FollowerSerializer




class OwnerSerialzer(serializers.ModelSerializer):
    class Meta:
        model=Owner
        fields=["id","user","farming_name","location"]
        extra_kwargs = {
            "id": {"read_only": True},
        }  


class ProductSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "description",
            "price",
            "quantity",
            "product_image",
            "owner",
            "discounted_price",
        ]
        extra_kwargs = {
            "id": {"read_only": True},
            "owner": {"read_only": True},
        }

    def get_discounted_price(self, obj):
        request = self.context.get("request")

        if not request or not request.user.is_authenticated:
            return obj.price  

        
        discount = obj.discounts.filter(customer=request.user).first()

        if discount:
           
            return discount.get_discounted_price()

        return obj.price
    def get_prooduct_image(self,obj):
        request=self.context.get("request")
        if not  request:
            return None
        return request.build_absolute_uri(obj.product_image.url)
    





class ProductDiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductDiscount
        fields=["id","owner","product","customer","discount_type","amount","created_at"]
        extra_kwargs = {
            "id": {"read_only": True},
            "owner": {"read_only": True},
            "product": {"read_only": True},
            "customer": {"read_only": True},
            }


class ProductImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductImages
        fields=["id","product","image"]
        extra_kwargs = {
            "id": {"read_only": True},
            "product": {"read_only": True}
        }




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

             







class ReplaySerializer(serializers.ModelSerializer):
    sender = serializers.ReadOnlyField(source='sender.username')
    reply_message=serializers.CharField(source='parent.sender.username',read_only=True)
    class Meta:
        model=ProductMessage
        fields=["id","reply_message","message","created_at","sender"]


class ProductMessageSerializer(serializers.ModelSerializer):
     sender=serializers.ReadOnlyField(source='sender.username')
     receiver=serializers.ReadOnlyField(source='receiver.farming_name')
     replies=ReplaySerializer(many=True,read_only=True)
     class Meta:
         model=ProductMessage
         fields=["id","sender","receiver","message","created_at","is_read","parent","replies"]


class  ProductCommentsRepliesSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    reply_text=serializers.CharField(source='parent.user.username',read_only=True)
    class Meta:
        model=ProductComments
        fields=["id","user","comment","created_at","reply_text"]

class ProductCommentsSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source='user.username')
    product=serializers.ReadOnlyField(source='product.product_name')
    replies=ProductCommentsRepliesSerializer(many=True,read_only=True)
    class Meta:
        model=ProductComments
        fields=["id","user","product","comment","created_at","updated_at","parent","replies"]





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
         read_only_fields = ["id", "consultant", "created_at"]


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
        



class ConsultantFollowSerializer(serializers.ModelSerializer):
    follower = serializers.SerializerMethodField()

    class Meta:
        model = ConsultantFollow
        fields = ["id", "follower", "created_at"]

    def get_follower(self, obj):
        from accounts.serializers import FollowerSerializer
        return FollowerSerializer(obj.user).data  









class RequestTobeConsultantSerializer(serializers.ModelSerializer):
     class Meta:
         model=RequestTobeConsultant
         fields=["id","user","national_id","location","license"]
         read_only_fields=["id","user"]





