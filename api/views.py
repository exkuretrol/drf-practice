from django.db.models import Max
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Order, Product
from .serializers import (
    OrderSerializer,
    ProductInfoSerializer,
    ProductSerializer,
)


@api_view(["GET"])
def produce_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    serializer = ProductSerializer(product)
    return Response(serializer.data)


@api_view(["GET"])
def product_info(request):
    products = Product.objects.all()
    counts = products.count()
    max_price = products.aggregate(max_price=Max("price"))["max_price"]

    serializer = ProductInfoSerializer(
        {"products": products, "counts": counts, "max_price": max_price}
    )
    return Response(serializer.data)


@api_view(["GET"])
def order_list(request):
    order = Order.objects.all()
    serializer = OrderSerializer(order, many=True)
    return Response(serializer.data)
