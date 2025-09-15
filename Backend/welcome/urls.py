from django.urls import path

from .views import ApiLandingPageView

urlpatterns=[
    path('',ApiLandingPageView.as_view(),name='api-landing-page')
]