from django.urls import path

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
    path("orders/", views.OrderListAPIView.as_view(), name="order-list"),
    path("user-orders/", views.UserOrderListAPIView.as_view(), name="user-order-list"),
]
