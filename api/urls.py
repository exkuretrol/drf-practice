from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("products/", views.ProductListAPIView.as_view(), name="product-list"),
    path(
        "products/<int:product_id>/",
        views.ProductDetailAPIView.as_view(),
        name="product-detail",
    ),
    path("products/info/", views.product_info, name="product-info"),
    path("orders/", views.OrderListAPIView.as_view(), name="order-list"),
]
