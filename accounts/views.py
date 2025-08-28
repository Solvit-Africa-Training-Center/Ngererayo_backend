from django.shortcuts import render
from rest_framework import viewsets,generics,status
from rest_framework.response import Response
from .serializers import RegisterUserSerializer
from .models import CustomUser


# Create your views here.

class RegisterUserView(viewsets.ModelViewSet):
      queryset=CustomUser.objects.all()
      serializer_class=RegisterUserSerializer
      def create(self, request,*args,**kwargs):
            serializer=self.get_serializer(data=request.data)
            if serializer.is_valid():
                  serializer.save()
                  return Response({"message": "User registered successfully."}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
