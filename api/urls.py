from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("products/", views.produce_list, name="product-list"),
    path("products/<int:pk>/", views.product_detail, name="product-detail"),
    path("products/info/", views.product_info, name="product-info"),
    path("orders/", views.order_list, name="order-list"),
]
