
from django.urls import path,include
from rest_framework import routers
from .messaging_views import (ProductMessageView,
                    SendProductMessageView,
                    ReplayMessage)

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
path('cart_add/', AddToCartView.as_view(), name='cart_add'),
path("product-message/<int:product_id>/",ProductMessageView.as_view(),name="product-messages"),
path("product/<int:product_id>/messages/", ProductMessageView.as_view(), name="product-messages"),
path("messages/<int:product_id>/send/", SendProductMessageView.as_view(), name="send-message"),
path("messages/<int:message_id>/reply/", ReplayMessage.as_view(), name="reply-message"),
]


