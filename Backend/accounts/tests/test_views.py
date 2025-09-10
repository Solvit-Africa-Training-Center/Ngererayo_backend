from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from accounts.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken


class AuthTest(APITestCase):

    def setUp(self):
        # URLs
        self.register_url = reverse("register-list")
        self.login_url = reverse("login-list")
        self.verify_otp_url = reverse("verify_otp-list")
        self.token_refresh_url = reverse("token_refresh")
        self.current_user_url = reverse("current_user")
        self.logout_url=reverse("logout")

    
        self.user_data = {
            "username": "testuser",
            "first_name": "gihozo",
            "last_name": "ismail",
            "email": "admin@admin.com",
            "password": "Testpass123",
            "confirm_password": "Testpass123",
            "role": "buyer",
            "phone": "1234567890"
        }

    
        self.user = CustomUser.objects.create_user(
            username="Richard",
            first_name="Richard",
            last_name="Kamanzi",
            email="richard@gmail.com",
            password="kamanzi123",
            role="Buyer",
            phone="0987654321",
            otp="123456",
            is_verified=True
        )

    def test_user_registration(self):
        """Test user registration endpoint"""
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('message', response.data)
        self.assertEqual(response.data["message"], 'User registered successfully.')

    def test_verify_otp(self):
        """Test OTP verification endpoint"""
        response = self.client.post(self.verify_otp_url, {
            "email": "richard@gmail.com",
            "otp": "123456"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('OTP verified successfully.', response.data['message'])

    def test_login_user(self):
        response_login = self.client.post(self.login_url, {
            "email": "richard@gmail.com",
            "password": "kamanzi123"
        }, format='json')

        self.assertEqual(response_login.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_login.data)
        self.assertIn('refresh', response_login.data)
        self.assertIn('message', response_login.data)


        refresh_token = response_login.data['refresh']
        response_refresh = self.client.post(self.token_refresh_url, {
            'refresh': refresh_token
        }, format='json')

        self.assertEqual(response_refresh.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_refresh.data)
    def test_current_user(self):
        response=self.client.get(self.current_user_url,format='json')
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    def test_log_out(self):
        login_response =self.client.post(self.login_url,{
            "email":"richard@gmail.com",
            "password":"kamanzi123"
        }, format='json')
        self.assertEqual(login_response.status_code,status.HTTP_200_OK)
        self.assertIn('access',login_response.data)
        self.assertIn('refresh',login_response.data)

        access_token = login_response.data['access']
        refresh_token =login_response.data['refresh']


        self.client.credentials(HTTP_AUTHORIZATION='Bearer '+access_token)


        response_logout=self.client.post(self.logout_url,{
            'refresh':refresh_token
        },format='json')
        self.assertEqual(response_logout.status_code,status.HTTP_200_OK)
        self.assertIn('message',response_logout.data)
        self.assertEqual(response_logout.data['message'],'Logout successfully.')



