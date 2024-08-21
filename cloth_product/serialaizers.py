from rest_framework import serializers
from .models import Product,Wishlist,Review
from django.contrib.auth.models import User
from .constraints import STAR_CHOICES,SIZE

from rest_framework import serializers
from .models import Product

# class ProductSerializer(serializers.ModelSerializer):

    # class Meta:
    #     model = Product
    #     fields = ['id', 'name', 'sub_category', 'image', 'price', 'description']



class ProductSerializer(serializers.ModelSerializer):
    # sub_category = serializers.CharField(source='sub_category.name')

    # size = serializers.MultipleChoiceField(choices = SIZE)
    # size = serializers.ListField(child=serializers.ChoiceField(choices=SIZE))

    class Meta:
        
        model = Product
        # fields = '__all__'

        fields = ['id','name','sub_category','image','price','quantity','description','size']




class WishlistSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = Wishlist
        fields = ['id', 'user', 'products']


class ReviewSerializer(serializers.ModelSerializer):
    # user_name = serializers.CharField(source='user.get_full_name', read_only=True)

    class Meta:
        model = Review
        fields ='__all__'
