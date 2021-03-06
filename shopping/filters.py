import django_filters
from django_filters import FilterSet, OrderingFilter, RangeFilter

from .models import Product, Store

class ProductFilter(FilterSet):
    order_by = OrderingFilter(
        fields=(
            ('created', 'created'),
            ('price', 'price')
        )
    )
    price = RangeFilter() # price_min & price_max

    class Meta:
        model = Product
        fields = {
            'name': ['iexact', 'icontains'],
            'store__id': ['exact'],
        }

class StoreFilter(FilterSet):
    order_by = OrderingFilter(
        fields=(
            ('created', 'created')
        )
    )

    class Meta:
        model = Store
        fields = {
            'id': ['iexact'],
            'name': ['iexact', 'icontains'],
            'user__id': ['iexact']
        }
