from django.urls import path

from . import views

app_name = "api"

urlpatterns = [
    path("products/", views.produce_list, name="product-list"),
    path("products/<int:pk>/", views.product_detail, name="product-detail"),
]
