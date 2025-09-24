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
                          ProductDiscountSerializer,
                          CustomerSupportSerializer,
                          ProductMessageSerializer,
                          ProductImagesSerializer,
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
            product=Product.objects.all().prefetch_related('discounts').order_by(' created_at')[:6]
            serializer=ProductSerializer(product,many=True,context={"request":request})
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class ProductListView(APIView):
    def get(self, request):
        try:
            product=Product.objects.all().prefetch_related('discounts').order_by('-created_at')
            serializer=ProductSerializer(product,many=True,context={"request":request})
            return Response(serializer.data)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
class AddProductImagesView(APIView):
    def post(self, request, product_id):
        try:
            owner=Owner.objects.get(user=request.user)
        except Owner.DoesNotExist:
            return Response({"error":"Only owners can add product images"},status=status.HTTP_403_FORBIDDEN)
        product=get_object_or_404(Product, id=product_id, owner=owner)
        serializer=ProductImagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return  Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

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





class AssignDiscountToCustomerView(APIView):
    permission_classes=[permissions.IsAuthenticated]
    def post(self, request, product_id):
        try:
            product=Product.objects.get(id=product_id, owner__user=request.user)
    
        except Product.DoesNotExist:
            return Response("Product not found or not owned by you",status=status.HTTP_404_NOT_FOUND)
        customer_id=request.data.get('customer_id')
        amount=request.data.get('amount')
        discount_type=request.data.get('discount_type')
        if not customer_id or not amount or not discount_type:
            return Response({"error":"customer_id, amount, and discount_type are required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            customer=CustomUser.objects.get(id=customer_id)
        except CustomUser.DoesNotExist:
            return Response("Customer not found",status=status.HTTP_404_NOT_FOUND)
        discount, created=ProductDiscount.objects.update_or_create(
            product=product,
            customer=customer,
            defaults={
        'amount': Decimal(amount),
        'discount_type': discount_type,
        'owner': product.owner  
    }
        )
        serializer=ProductDiscountSerializer(discount)
        return Response(serializer.data,status=status.HTTP_201_CREATED)



class ProductOwnerGetDiscountsView(APIView):
    def get(self, request, product_id):
        try:
            owner=Owner.objects.get(user=request.user)
            product=Product.objects.get(id=product_id,owner=owner)
            discounts=ProductDiscount.objects.filter(product=product)
            serializer=ProductDiscountSerializer(discounts,many=True)
            return Response(serializer.data)
        except (Owner.DoesNotExist, Product.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)



class OwnerEditProductDiscounts(APIView):
    def put(self, request, product_id, customer_id):
        try:
            owner=Owner.objects.get(user=request.user)
            product=Product.objects.get(id=product_id,owner=owner)
            customer=CustomUser.objects.get(id=customer_id)
            discount=ProductDiscount.objects.get(product=product,customer=customer)
        except (Owner.DoesNotExist, Product.DoesNotExist, CustomUser.DoesNotExist, ProductDiscount.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer=ProductDiscountSerializer(discount,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




class ProductDiscountDelateView(APIView):
    def delete(self, request, product_id, customer_id):
        try:
            owner=Owner.objects.get(user=request.user)
            product=Product.objects.get(id=product_id,owner=owner)
            customer=CustomUser.objects.get(id=customer_id)
            discount=ProductDiscount.objects.get(product=product,customer=customer)
        except (Owner.DoesNotExist, Product.DoesNotExist, CustomUser.DoesNotExist, ProductDiscount.DoesNotExist):
            return Response(status=status.HTTP_404_NOT_FOUND)
        discount.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
        



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



