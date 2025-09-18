
from django.urls import path,include
from rest_framework import routers
from .consultant_view import ConsultantListView,FollowConsultantview,FollowConsultantPostView
from .paymeny_views import CreateCheckoutSession,stripe_webhook
from .placeorder import PlaceOrderView,GetOrdersView
from .RequestedFarmer import RequestTobeOwnerView
from .messaging_views import (ProductMessageView,
                              SendProductCommentsView,
                    SendProductMessageView,
                    DeleteProductMessageView,
                    EditProductMessageView,
                    GetProductCommentsView,
                    GetSendMessage,
                    GetMessageYouSent,
                    GetReplyMessage,
                    GetProductCommentsReplyView,
                    ReplyProductComments,
                    ReplayMessage)


from .views import (ProductView,
                    # OwnerView,
                    OwnerProductsView,
                    ProductListView,
                    AllProductOwnersView,
                    ProductDetailView,
                    OwnerDeleteProduct,
                    ProductView,
                    OwnerAddProduct,
                    # ApiLandingPage,
      CustomerSupportView,
                    TestimonialView,
                    DeleteItemFromcartView,
                    UpdateQuantityOnCartView,
                    OwnerEditProductView,CartView, AddToCartView)



router=routers.DefaultRouter()
router.register("products",ProductView,basename="products")
# router.register("owners",OwnerView,basename="owners")





urlpatterns=[
    path("",include(router.urls)),
    # path("",ApiLandingPage.as_view(),name="api-landing-page"),
    path("latest-products/",ProductView.as_view({'get':'list'}), name="latest-products"),
    path("all-products/",ProductListView.as_view(),name="product-list"),
    path("product/<int:product_id>/",ProductDetailView.as_view(), name="product-detail" ),
    path("Requested-owner/",RequestTobeOwnerView.as_view(), name ="request-owner"),
    path("owners/",AllProductOwnersView.as_view(), name="all-owners"),
    path("owner/add-product/",OwnerAddProduct.as_view(), name="owner-add-product"),
    path("owner/<int:owner_id>/products/",OwnerProductsView.as_view()),
path('owner-product/<int:product_id>/edit/', OwnerEditProductView.as_view(), name='owner-edit-product'),
path("owner-product/<int:product_id>/delete/", OwnerDeleteProduct.as_view(), name='owner-delete-product'),
path('cart/', CartView.as_view(), name='cart'),
path('cart_delete/<int:cart_item_id>/', DeleteItemFromcartView.as_view(), name='cart_delete'),

path('cart_add/', AddToCartView.as_view(), name='cart_add'),
path('cart_update/<int:cart_item_id>/', UpdateQuantityOnCartView.as_view(), name='cart_update'),

path("place-order/",PlaceOrderView.as_view(), name="place-order"),
path("get-orders/",GetOrdersView.as_view(), name="get-orders"),
path("product-message/<int:product_id>/",ProductMessageView.as_view(),name="product-messages"),
# path("product/<int:product_id>/messages/", ProductMessageView.as_view(), name="product-messages"),
path("product/<int:product_id>/messages/", ProductMessageView.as_view(), name="product-messages"),
path("messages/<int:product_id>/send/", SendProductMessageView.as_view(), name="send-message"),
path("messages/<int:product_id>/you-sent/", GetMessageYouSent.as_view(), name="you-sent-message"),
path("messages/<int:message_id>/edit/", EditProductMessageView.as_view(), name="edit-message"),
path("messages/<int:message_id>/delete/", DeleteProductMessageView.as_view(), name="delete-message"),
path("messages/<int:product_id>/", GetSendMessage.as_view(), name="get-send-message"),
path("messages/replies/<int:message_id>/", GetReplyMessage.as_view(), name="get-reply-message"),
path("messages/<int:message_id>/reply/", ReplayMessage.as_view(), name="reply-message"),
path("comments/<int:product_id>/send/", SendProductCommentsView.as_view(), name="send-comment"),
path("comments/<int:comment_id>/reply/", ReplyProductComments.as_view(), name="reply-comment"),
path("comments/<int:product_id>/", GetProductCommentsView.as_view(), name="get-comments"),
path("comments/replies/<int:comment_id>/", GetProductCommentsReplyView.as_view(), name="get-comment-replies"),
path("create-checkout-session/",CreateCheckoutSession.as_view(),name="create-checkout-session"),
path("stripe-webhook/",stripe_webhook,name="stripe-webhook"),
path("testimonials/",TestimonialView.as_view(),name="testimonials"),
path("customer-support/",CustomerSupportView.as_view(),name="customer-support"),
path("consultants/",ConsultantListView.as_view(),name="consultants"),
path("consultants/<int:consultant_id>/follow/",FollowConsultantview.as_view(),name="follow-consultant"),
path("consultants/following/post/",FollowConsultantPostView.as_view(),name="follow-consultant-post"),


]


