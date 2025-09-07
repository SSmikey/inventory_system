from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum
from rest_framework.decorators import api_view, permission_classes
from django.utils.dateparse import parse_date
from django.db.models.functions import TruncDay, TruncMonth
from .models import Product, Supplier, Transaction
from .serializers import (
    ProductSerializer,
    ProductStockSerializer,
    SupplierSerializer,
    TransactionSerializer
)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated], url_path='update_stock')
    def update_stock(self, request, pk=None):
        product = self.get_object()
        old_quantity = product.quantity
        serializer = ProductStockSerializer(product, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            new_quantity = serializer.validated_data.get('quantity', product.quantity)

            if new_quantity > old_quantity:
                transaction_type = 'inbound'
                qty_changed = new_quantity - old_quantity
            else:
                transaction_type = 'outbound'
                qty_changed = old_quantity - new_quantity

            if qty_changed > 0:
                Transaction.objects.create(
                    product=product,
                    transaction_type=transaction_type,
                    quantity=qty_changed,
                    note="Auto log from stock update"
                )

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by('-created_at')
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-created_at')
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        product_id = self.request.query_params.get('product')
        transaction_type = self.request.query_params.get('transaction_type')
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')

        if product_id:
            queryset = queryset.filter(product__id=product_id)
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        if date_from:
            queryset = queryset.filter(created_at__date__gte=parse_date(date_from))
        if date_to:
            queryset = queryset.filter(created_at__date__lte=parse_date(date_to))

        return queryset


    @action(detail=False, methods=['get'], url_path='report')
    def report(self, request):
        period = request.query_params.get('period', 'day')
        product_id = request.query_params.get('product')
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')

        qs = Transaction.objects.all()

        if product_id:
            qs = qs.filter(product__id=product_id)
        if date_from:
            qs = qs.filter(created_at__date__gte=parse_date(date_from))
        if date_to:
            qs = qs.filter(created_at__date__lte=parse_date(date_to))

        if period == 'month':
            qs = qs.annotate(period=TruncMonth('created_at'))
        else:
            qs = qs.annotate(period=TruncDay('created_at'))

        report = qs.values('period', 'transaction_type').annotate(total_qty=Sum('quantity')).order_by('period')

        # restructure data ให้เป็น friendly format
        data = {}
        for r in report:
            p = r['period'].strftime('%Y-%m-%d') if period == 'day' else r['period'].strftime('%Y-%m')
            if p not in data:
                data[p] = {'inbound': 0, 'outbound': 0}
            data[p][r['transaction_type']] = r['total_qty']

        return Response(data)