# serializers.py
from rest_framework import serializers
from .models import PurchaseModel

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseModel
        fields = ['']
        # fields = ['product']
        