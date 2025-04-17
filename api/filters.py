import django_filters as filters

from .models import Product


class ProductFilter(filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["iexact", "icontains"],
            "price": ["exact", "gte", "lte", "range"],
        }
