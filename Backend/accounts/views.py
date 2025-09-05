from django.shortcuts import render
from rest_framework import viewsets,generics,status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import login,logout
from django.core.mail import send_mail
from rest_framework.permissions import AllowAny
from accounts.tasks import send_welcome_email_task
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from .serializers import (RegisterUserSerializer,
                          AuthenticateUserSerializer,
                          UserSerializer,
                          VerifyOtpSerializer)
from .models import CustomUser



# Create your views here.

class RegisterUserView(viewsets.ModelViewSet):
      queryset=CustomUser.objects.all()
      serializer_class=RegisterUserSerializer
      def create(self, request,*args,**kwargs):
            serializer=self.get_serializer(data=request.data)
            if serializer.is_valid():
                  user=serializer.save()
                  user.generate_otp()
                  send_mail(
                        subject="Welcome to ngererayo platform",
                        message=f"Hello {user.first_name},\n\nThank you for registering on ngererayo platform. This is your OTP for activating your account: {user.otp}",
                        from_email="gihozoismail@gmail.com",
                        recipient_list=[user.email]
                  )
                  return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      

class VerifyOtpView(viewsets.ModelViewSet):
      queryset=CustomUser.objects.all()
      serializer_class=VerifyOtpSerializer
      def create(self,request,*args,**kwargs):
            serializer=self.get_serializer(data=request.data)
            if serializer.is_valid():
                  email=serializer.validated_data["email"]
                  user=CustomUser.objects.get(email=email)
                  user.is_active=True
                  user.otp=None
                  user.otp_expiry=None
                  user.is_verified=True
                  user.save()
                  return Response({"message": "OTP verified successfully."}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





class LoginView(viewsets.ModelViewSet):
      queryset=CustomUser.objects.none()
      serializer_class=AuthenticateUserSerializer                                                                                                                                     
      permission_classes=[AllowAny]
      def create(self, request, *args, **kwargs):
            serializer=self.get_serializer(data=request.data)
            if serializer.is_valid():
                  user=serializer.validated_data["user"]
                  if not user.is_verified:
                        return Response({"error": "User account is not verified."}, status=status.HTTP_403_FORBIDDEN)
                  login(request,user)
                  refresh_token=RefreshToken.for_user(user)
                  return Response({
                        'refresh':str(refresh_token),
                        'access':str(refresh_token.access_token),
                        'message':f'{user.username} Login successfully'
                  })
            return  Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
      




class LogoutView(APIView):
      permission_classes=[AllowAny]
      def post(self, request, *args,**kwargs):
            try:
                  refresh_token=request.data["refresh"]
                  token=RefreshToken(refresh_token)
                  token.blacklist()
                  return Response({"message": "Logout successfully."}, status=status.HTTP_200_OK)
            except Exception as e:
             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


            
   


      
class CurrentLoginUserView(APIView):
      def get(self, request, *args, **kwargs):
            user = request.user
            if user.is_authenticated:
                  serializer = UserSerializer(user)
                  return Response(serializer.data, status=status.HTTP_200_OK)
            return Response({"error": "User not authenticated."}, status=status.HTTP_401_UNAUTHORIZED)