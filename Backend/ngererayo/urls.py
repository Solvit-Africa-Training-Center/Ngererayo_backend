"""
URL configuration for ngererayo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view as swagger_get_schema_view
from  django.conf import settings
from django.conf.urls.static import static
admin.site.site_header="Ngererayo Admin"
admin.site.site_title="Ngererayo Admin Portal"

schema_view=swagger_get_schema_view(
    openapi.Info(
        title="All Ngererayo Api's documentation",
        default_version='v1',
        description="Ngerarayo project api's key full documentation"
    ),public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')),
    path('',include('welcome.urls')),
    path("market/",include("market.urls")),
    path("swagger/",schema_view.with_ui('swagger',cache_timeout=0),name='schema-swagger-ui'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


