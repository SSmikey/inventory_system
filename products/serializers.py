from rest_framework import serializers
from .models import Product, Supplier, Transaction

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        fields = ['id','name','sku','quantity','price','category','created_at','updated_at']

class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'quantity']  # เฉพาะ quantity

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_name', 'phone', 'email', 'address', 'created_at', 'updated_at']

class TransactionSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'product', 'product_name', 'transaction_type', 'quantity', 'note', 'created_at']