from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        fields = ['id','name','sku','quantity','price','category','created_at','updated_at']

class ProductStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'quantity']  # เฉพาะ quantity