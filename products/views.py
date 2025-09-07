from rest_framework.decorators import action
from rest_framework import viewsets
from .models import Product, Supplier
from .serializers import ProductSerializer, ProductStockSerializer, SupplierSerializer
from rest_framework.permissions import IsAuthenticated


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_stock(self, request, pk=None):
        product = self.get_object()
        serializer = ProductStockSerializer(
            product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        # <-- ต้อง login ก่อน
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all().order_by('-created_at')
    serializer_class = SupplierSerializer
    permission_classes = [IsAuthenticated]