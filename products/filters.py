import django_filters
from .models import Product, Transaction


class ProductFilter(django_filters.FilterSet):
    # filter ด้วยชื่อ product
    name = django_filters.CharFilter(field_name="name", lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['name']


class TransactionFilter(django_filters.FilterSet):
    product = django_filters.CharFilter(field_name="product__id", lookup_expr='exact')
    transaction_type = django_filters.CharFilter(field_name="transaction_type", lookup_expr='exact')
    date_from = django_filters.DateFilter(field_name="created_at", lookup_expr='date__gte')
    date_to = django_filters.DateFilter(field_name="created_at", lookup_expr='date__lte')

    class Meta:
        model = Transaction
        fields = ['product', 'transaction_type', 'date_from', 'date_to']
