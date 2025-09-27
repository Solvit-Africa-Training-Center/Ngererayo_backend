
from django.urls import path,include
from rest_framework import routers
from .consultant_view import (ConsultantListView,
                              RequestTobeConsultantView,
                              ConsultantAddPostView,
                              ConsultantEditPostView,
                              ConsultantDeletePostView,
                              ConsultantPostsView,
                              PostView,
                              ConsultantAllFollwers,
                              FollowConsultantview,FollowConsultantPostView)

from .placeorder import PlaceOrderView,GetOrdersView,OwnerOrdersView
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
                    GetAllUserWhoSendMessage,
                    ReplayMessage)


from .views import (ProductView,
                    # OwnerView,
                    OwnerProductsView,
                    ProductListView,
                    AllProductOwnersView,
                    ProductOwnerGetDiscountsView,
                    ProductDetailView,
                    AddProductImagesView,
                    OwnerDeleteProduct,
                    ProductView,
                    OwnerAddProduct,
                    AssignDiscountToCustomerView,
                    OwnerEditProductDiscounts,
                    ProductDiscountDelateView,
                    # ApiLandingPage,
      CustomerSupportView,
                    TestimonialView,
                    
                    OwnerEditProductView, )

from .paymeny_views import CreatePaymentView,stripe_webhook
from .comments_views import (SendCommentView,
                             CommentsRepliesView,
                             GetCommentsView,
                             GetOneCommentView,
                             DeleteYourCommentView,
                             EditYourCommentView,
                             ProductOwnerDeleteCommentView
                             )


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
path("owner-product/<int:product_id>/images/", AddProductImagesView.as_view(), name='add-product-images'),
path("products/<int:product_id>/assign-discount/", AssignDiscountToCustomerView.as_view(), name="assign-discount-to-customer"),
path("products/<int:product_id>/discounts/",ProductOwnerGetDiscountsView.as_view(), name="product-discounts"),
path("products/<int:product_id>/discounts/<int:customer_id>/delete/", ProductDiscountDelateView.as_view(), name="product-discount-delete"),
path("owner-product/<int:product_id>/discounts/<int:customer_id>/edit/", OwnerEditProductDiscounts.as_view(), name="owner-edit-product-discounts"),
path("place-order/",PlaceOrderView.as_view(), name="place-order"),
path("get-orders/",GetOrdersView.as_view(), name="get-orders"),
path("owner/orders/",OwnerOrdersView.as_view(), name="owner-orders"),
path("product-message/<int:product_id>/",ProductMessageView.as_view(),name="product-messages"),
# path("product/<int:product_id>/messages/", ProductMessageView.as_view(), name="product-messages"),
path("product/<int:product_id>/messages/", ProductMessageView.as_view(), name="product-messages"),
path("messages/<int:product_id>/send/", SendProductMessageView.as_view(), name="send-message"),
path("messages/<int:product_id>/all-users/",  GetAllUserWhoSendMessage.as_view(), name="all-users"),
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
path("testimonials/",TestimonialView.as_view(),name="testimonials"),
path("customer-support/",CustomerSupportView.as_view(),name="customer-support"),
path("consultants/",ConsultantListView.as_view(),name="consultants"),
path("consultants/<int:consultant_id>/followers/",ConsultantAllFollwers.as_view(),name="all-follwers"),
path("consultants/posts/",PostView.as_view(),name="all-posts"),
path("consultants/<int:consultant_id>/follow/",FollowConsultantview.as_view(),name="follow-consultant"),
path("consultants/following/post/",FollowConsultantPostView.as_view(),name="follow-consultant-post"),
path("requst-consultant/",RequestTobeConsultantView.as_view(), name="request-consultant"),
path("consultants/add-post/",ConsultantAddPostView.as_view(), name="consultant-add-post"),
path("consultants/<int:consultant_id>/posts/",ConsultantPostsView.as_view(), name="consultant-posts"),
path("consultants/posts/<int:post_id>/edit/",ConsultantEditPostView.as_view(), name="consultant-edit-post"),
path("consultants/posts/<int:post_id>/delete/",ConsultantDeletePostView.as_view(), name="consultant-delete-post"),
path("comments/<int:product_id>/",SendCommentView.as_view(), name="comments"),
path("comments/<int:comment_id>/reply/",CommentsRepliesView.as_view(), name="replies"),
path("comments/<int:product_id>/",GetCommentsView.as_view(), name="get-comments"),
path("comments/one/<int:comment_id>/",GetOneCommentView.as_view(), name="get-one-comment"),
path("comments/<int:comment_id>/delete/", DeleteYourCommentView.as_view(), name="delete-your-comment"),
path("comments/<int:comment_id>/edit/", EditYourCommentView.as_view(), name="edit-your-comment"),
path("comments/<int:comment_id>/owner-delete/", ProductOwnerDeleteCommentView.as_view(), name="product-owner-delete-comment"),


path("payment/<int:order_id>/pay/",CreatePaymentView.as_view(),name="create-payment"),
path("stripe-webhook/",stripe_webhook,name="stripe-webhook"),

]


