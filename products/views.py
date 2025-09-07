from rest_framework.decorators import action
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

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
