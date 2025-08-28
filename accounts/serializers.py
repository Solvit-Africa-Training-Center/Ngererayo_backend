from rest_framework import serializers
from .models import CustomUser


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
            
