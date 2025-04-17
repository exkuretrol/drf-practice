from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, Product
from .serializers import (
    OrderSerializer,
    ProductInfoSerializer,
    ProductSerializer,
)


class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"
    lookup_field = "id"


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


@api_view(["GET"])
def product_info(request):
    products = Product.objects.all()
    counts = len(products)
    max_price = products.aggregate(max_price=Max("price"))["max_price"]
    serializer = ProductInfoSerializer(
        {
            "products": products,
            "counts": counts,
            "max_price": max_price,
        }
    )
    return Response(serializer.data)
