from django.urls import path

from ecommerce.views import ProductsViewSet, OrderViewSet

urlpatterns = [
    path("products", ProductsViewSet.as_view({'get': 'list'})),
    path("order", OrderViewSet.as_view()),
]
