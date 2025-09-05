from rest_framework import serializers
from .models import CustomUser
from django.utils import timezone
from django.contrib.auth import authenticate




class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "first_name", "last_name", "role", "phone"]

class  RegisterUserSerializer(serializers.ModelSerializer):
    first_name=serializers.CharField(required=True)
    last_name=serializers.CharField(required=True)
    email=serializers.EmailField(required=True)
    phone=serializers.CharField(required=True)
    password=serializers.CharField(write_only=True, required=True)
    confirm_password=serializers.CharField(write_only=True, required=True)

    class Meta:
        model=CustomUser
        fields = ["id", "username", "email", "first_name", "last_name", "role", "phone", "password", "confirm_password"]
        extra_kwargs = {
            "password": {"write_only": True},
            "confirm_password": {"write_only": True}
        }
    def validate(self,data):
        if data["password"]!=data["confirm_password"]:
              raise serializers.ValidationError("password not match")
        return data
    
    def create(self,validated_data):
         user=CustomUser.objects.create_user(
              username=validated_data["username"],
              first_name=validated_data["first_name"],
              last_name=validated_data["last_name"],
              email=validated_data["email"],
              phone=validated_data["phone"],
              password=validated_data["password"],
              role=validated_data.get("role", "buyer")
         )
         return user




class VerifyOtpSerializer(serializers.Serializer):
     email=serializers.EmailField(required=True)
     otp=serializers.CharField(required=True)
     def validate(self, data):
          email=data.get("email")
          otp=data.get("otp")

          try:
               user=CustomUser.objects.get(email=email)
          except CustomUser.DoesNotExist:
               raise serializers.ValidationError("email not exists")
          if user.otp!=otp:
               raise serializers.ValidationError("invalid otp")
          if user.otp_expiry and user.otp_expiry< timezone.now():
               raise serializers.ValidationError("otp expired")
          user.is_verified=True
          user.save()
          return data
     




class AuthenticateUserSerializer(serializers.ModelSerializer):
     email=serializers.EmailField(required=True)
     password=serializers.CharField(write_only=True, required=True)
     class Meta:
          model=CustomUser
          fields=["email","password"]


     def validate(self, data):
          email=data.get("email")
          password=data.get("password")

          if not email or not password:
                raise serializers.ValidationError("all fields are required")
          
          user=authenticate(email=email, password=password)
          if not user:
                raise serializers.ValidationError(" wrong email or password")
          data["user"]=user
          return data
               
