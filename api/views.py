from django.db.models import Max
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .filters import InStockFilterBackend, OrderFilter, ProductFilter
from .models import Order, Product
from .serializers import (
    OrderCreateUpdateSerializer,
    OrderSerializer,
    ProductInfoSerializer,
    ProductSerializer,
)


class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.order_by("pk")
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
    pagination_class.page_size = 5
    pagination_class.page_size_query_param = "size"
    pagination_class.max_page_size = 100

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


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related("items__product")
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["create", "update"]:
            return OrderCreateUpdateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
