from django.shortcuts import render
from django.views import View
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework import viewsets,status,generics
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

from .serializers import (ProductSerializer,
                          OwnerSerialzer,
                          CustomerSupportSerializer,
                          ProductMessageSerializer,
                          TestimonialsSerializer,
                          )
from .models import *






class AllProductOwnersView(APIView):
    def get(self, request):
        count = Owner.objects.count()
        return Response({"owners_count": count})



class ProductView(APIView):
    permission_classes=[AllowAny]
    def get(self, request):
        try:
            product=Product.objects.all().order_by(' created_at')[:6]
            serializer=ProductSerializer(product,many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ProductListView(APIView):
    def get(self, request):
        try:
            product=Product.objects.all()
            serializer=ProductSerializer(product,many=True)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        


class ProductDetailView(APIView):
    def get(self, request,product_id):
        try:
            product=Product.objects.get(id=product_id)
            serializer=ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        





class ProductView(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[permissions.IsAuthenticated]

    def perform_create(self, serialzier):
        owner=Owner.objects.get(user=self.request.user)
        serialzier.save(owner=owner)


class OwnerAddProduct(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request,*args,**kwargs):
        try:
            owner=Owner.objects.get(user=request.user)
        except Owner.DoesNotExist:
            return Response({"error":"Only owners can add products"},status=status.HTTP_403_FORBIDDEN)
        serializer=ProductSerializer(data=request.data)
        if  serializer.is_valid():
            product=serializer.save(owner=owner)
            return Response(ProductSerializer(product).data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
        




class OwnerProductsView(generics.ListAPIView):
    serializer_class=ProductSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        owner_id=self.kwargs['owner_id']
        return Product.objects.filter(owner__id=owner_id)




class OwnerEditProductView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self, product_id,user):
        try:
              owner=Owner.objects.get(user=user)
              return Product.objects.get(id=product_id,owner=owner)
        except (Owner.DoesNotExist, Product.DoesNotExist):
              return None


    def get(self, request,product_id):
        try:
            product=Product.objects.get(id=product_id)
            if not product:
                return Response({"product not found": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer=ProductSerializer(product)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def put(self, request,product_id):
        try:
            product=Product.objects.get(id=product_id)
            if not product:
                return Response({"product not found": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer=ProductSerializer(product,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        




class OwnerDeleteProduct(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def get_object(self, product_id,user):
        try:
            owner=Owner.objects.get(user=user)
            return Product.objects.get(id=product_id,owner=owner)
        except (Owner.DoesNotExist, Product.DoesNotExist):
            return None

    def get(self, request,product_id):
        try:
            prouct=Product.objects.get(id=product_id)
            if not prouct:
                return Response({"product not found": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            serializer=ProductSerializer(prouct)
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, product_id):
        try:
            product=Product.objects.get(id=product_id)
            if not product:
                return Response({"product not found": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)






    # .............Testimonial view .........................





class TestimonialView(APIView):
    def get(self,request):
        testimonials=Testimonials.objects.all().order_by('-created_at')[:3]
        serializer=TestimonialsSerializer(testimonials,many=True)
        return Response(serializer.data)




class CustomerSupportView(APIView):
    def post(self, request):
        serializer=CustomerSupportSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



