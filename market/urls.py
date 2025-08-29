from django.urls import path, include
from .views import CartView, AddToCartView
from rest_framework import routers

router = routers.DefaultRouter()
# router.register("cart", CartView, basename='cart')
# router.register("cart_add", AddToCartView, basename='cart_add')

urlpatterns = [
    path('', include(router.urls)),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart_add/', AddToCartView.as_view(), name='cart_add'),
]