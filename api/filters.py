import django_filters as filters
from rest_framework.filters import BaseFilterBackend

from .models import Product


class InStockFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.exclude(stock=0)


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["iexact", "icontains"],
            "price": ["exact", "gte", "lte", "range"],
        }
