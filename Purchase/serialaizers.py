# serializers.py
from rest_framework import serializers
from .models import PurchaseModel,PurchaseCartModel

from cloth_product.serialaizers import ProductSerializer
class PurchaseSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = PurchaseModel
        fields = ['']
        # fields = ['product']
   
class PurchaseCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseCartModel
        fields = ['']

class PurchaseProductSerialaizer(serializers.ModelSerializer):
    product = ProductSerializer( read_only=True)

    class Meta:
        model = PurchaseModel
        fields =['id', 'user', 'product']
