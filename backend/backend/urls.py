from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import refresh_jwt_token

API_PREFIX = getattr(settings, "API_ROOT_URL_V1", 'api/v1/')

router = routers.DefaultRouter()

urlpatterns = [
    path("admin/", admin.site.urls),
    path(API_PREFIX+"auth/", include("users.urls")),
    path(API_PREFIX+"ecommerce/", include("ecommerce.urls")),
    path(API_PREFIX+"auth/token-refresh/", refresh_jwt_token),
    path(API_PREFIX, include(router.urls)),
]
