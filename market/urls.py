
from django.urls import path,include
from rest_framework import routers

from .views import (ProductView,
                    OwnerView,
                    OwnerProductsView,
                    ProductListView,
                    ProductDetailView,
                    OwnerDeleteProduct,
                    OwnerEditProductView,CartView, AddToCartView)



router=routers.DefaultRouter()
router.register("products",ProductView,basename="products")
router.register("owners",OwnerView,basename="owners")





urlpatterns=[
    path("",include(router.urls)),
    path("all-products/",ProductListView.as_view()),
    path("product/<int:product_id>/",ProductDetailView.as_view()),
    path("owner/<int:owner_id>/products/",OwnerProductsView.as_view()),
path('owner-product/<int:product_id>/edit/', OwnerEditProductView.as_view(), name='owner-edit-product'),
path("owner-product/<int:product_id>/delete/", OwnerDeleteProduct.as_view(), name='owner-delete-product'),
path('cart/', CartView.as_view(), name='cart'),
path('cart_add/', AddToCartView.as_view(), name='cart_add')
]


