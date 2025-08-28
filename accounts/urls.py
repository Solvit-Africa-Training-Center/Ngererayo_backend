from django.urls import path,include
from .views import RegisterUserView
from rest_framework import routers



router=routers.DefaultRouter()
router.register('register',RegisterUserView,basename='register')

urlpatterns=[
    path('',include(router.urls))
    
]