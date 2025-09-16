from django.urls import path,include
from .views import (RegisterUserView,
                    LoginView,
                    ResendOtpView,
                    ForgotPasswordView,
                    ResetPasswordView,
                    CurrentLoginUserView,
                    VerifyOtpView,LogoutView)
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)



router=routers.DefaultRouter()
router.register('register',RegisterUserView,basename='register')
router.register('login',LoginView,basename='login')
router.register("verify-otp",VerifyOtpView,basename="verify_otp")

urlpatterns=[
    path('',include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('current-user/',CurrentLoginUserView.as_view(),name='current_user'),
    path('resend-otp/',ResendOtpView.as_view(),name='resend_otp'),
    path("forgot-password/",ForgotPasswordView.as_view(),name="forgot_password"),
    path("reset-password/",ResetPasswordView.as_view(),name="reset_password"),
    
]