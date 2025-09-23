from rest_framework import serializers
from .models import CustomUser,Role
from django.utils import timezone
from django.contrib.auth import authenticate
from market.models import Owner
from market.serializers import OwnerSerialzer,ConsultantSerializer



class RoleSerializer(serializers.ModelSerializer):
     class Meta:
          model=Role
          fields=["id","name"]
          extra_kwargs = {
               "id": {"read_only": True},
          }

class UserSerializer(serializers.ModelSerializer):
    role=RoleSerializer(many=True,read_only=True)
    owner=OwnerSerialzer(read_only=True)
    consultant=ConsultantSerializer(read_only=True)
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "first_name", "last_name", "role", "phone", "owner", "consultant"]

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "first_name", "last_name", "phone", "role"]


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
           
         )
         buyer_role,_=Role.objects.get_or_create(name="buyer")
         user.role.add(buyer_role)
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
               



class ForgotPasswordSerializer(serializers.Serializer):
     email=serializers.EmailField(required=True)
     def validate_email(self, value):
        if not CustomUser.objects.filter(email__iexact=value.strip()).exists():
            raise serializers.ValidationError("No account found with this email.")
        return value.strip().lower()
     




class ResetPasswordSerializer(serializers.Serializer):
     email=serializers.EmailField(required=True)
     otp=serializers.CharField(required=True)
     new_password=serializers.CharField(write_only=True, required=True, max_length=128)



     def validate(self, data):
          try:
               user=CustomUser.objects.get(email=data["email"])
          except CustomUser.DoesNotExist:
               raise serializers.ValidationError("user with this email does not exist")
          if not user.verify_otp(data["otp"]):
               raise serializers.ValidationError("invalid otp or expired")
          return data
     
     def save(self):
          user=CustomUser.objects.get(email=self.validated_data["email"])
          user.set_password(self.validated_data["new_password"])
          user.otp=None
          user.otp_expiry=None
          user.save()
          return user
