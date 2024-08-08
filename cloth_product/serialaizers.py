from rest_framework import serializers
from .models import Product,Wishlist,Review
from django.contrib.auth.models import User
from .constraints import STAR_CHOICES,SIZE

class ProductSerializer(serializers.ModelSerializer):
    # size = serializers.MultipleChoiceField(choices = SIZE)
    # size = serializers.ListField(child=serializers.ChoiceField(choices=SIZE))

    class Meta:
        
        model = Product
        # fields = '__all__'

        fields = ['id','name','category','image','price','quantity','description','size']




class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(many=False)
    products = ProductSerializer(many=True, read_only=True)
    class Meta:
        model = Wishlist
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields ='__all__'