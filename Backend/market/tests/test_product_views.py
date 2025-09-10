from  rest_framework.test import APITestCase

from django.urls import reverse
from rest_framework import status
from django.utils import timezone
from datetime import timedelta
from market.models import Product,Owner
from accounts.models import CustomUser





class TestProductView(APITestCase):
    def setUp(self):


        self.user=CustomUser.objects.create_user(
            username="testuser",
            first_name="test",
            last_name="user",
            email="test@test.com",
            role="farmer",
            password="123456",
            phone="08012345678",
        )
        self.user.save()

        self.owner=Owner.objects.create(
            user=self.user,
            farming_name="test farm",
            location="test location",
        )
        self.product=Product.objects.create(
            product_name="tomato",
            description="fresh tomato",
            price=100,  
            owner=self.owner,
            quantity=10,
            product_image="tomato.jpg",
            created_at=timezone.now(),

        )

        self.product_view_url =reverse('product-list')
        self.product_details=reverse('product-detail',kwargs={'product_id':self.product.id})



    def test_product_view(self):
        response=self.client.get(self.product_view_url,format='json')
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    
    def test_product_details(self):
         response=self.client.get(self.product_details,format='json')

         self.assertEqual(response.status_code, status.HTTP_200_OK) 
         self.assertEqual(response.data["id"], self.product.id)
         self.assertEqual(response.data["product_name"], self.product.product_name)       