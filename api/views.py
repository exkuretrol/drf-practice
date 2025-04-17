from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import InStockFilterBackend, ProductFilter
from .models import Order, Product
from .serializers import (
    OrderSerializer,
    ProductInfoSerializer,
    ProductSerializer,
)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = (
        InStockFilterBackend,
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    )

    # starts with = means exact match
    search_fields = ["=name", "description"]
    ordering_fields = ["name", "price"]
    pagination_class = PageNumberPagination
    pagination_class.page_size = 2
    pagination_class.page_query_param = "p"
    pagination_class.page_size_query_param = "size"
    pagination_class.max_page_size = 100

    # pagination_class = LimitOffsetPagination
    # pagination_class.default_limit = 2

    def get_permissions(self):
        self.permission_classes = [AllowAny]

        if self.request.method == "POST":
            self.permission_classes = (IsAdminUser,)

        return super().get_permissions()


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = "product_id"
    lookup_field = "id"

    def get_permissions(self):
        self.permission_classes = [AllowAny]

        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            self.permission_classes = (IsAdminUser,)

        return super().get_permissions()


class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(user=self.request.user)


class ProductInfoAPIView(APIView):

    def get(self, request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer(
            {
                "products": products,
                "counts": len(products),
                "max_price": products.aggregate(max_price=Max("price"))["max_price"],
            }
        )
        return Response(serializer.data)
