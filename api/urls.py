from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "api"

urlpatterns = [
    path(
        "products/", views.ProductListCreateAPIView.as_view(), name="product-listcraete"
    ),
    path(
        "products/<int:product_id>/",
        views.ProductRetrieveUpdateDestroyAPIView.as_view(),
        name="product-action",
    ),
    path("products/info/", views.ProductInfoAPIView.as_view(), name="product-info"),
]

router = DefaultRouter()
router.register("orders", views.OrderViewSet, basename="orders")
urlpatterns += router.urls
