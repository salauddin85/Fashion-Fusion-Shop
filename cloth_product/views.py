from django.shortcuts import render
from rest_framework import viewsets
from .models import Product,Wishlist,Review
from .serialaizers import WishlistSerializer,ReviewSerializer,ProductSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework import status
from .constraints import SIZE
from rest_framework.views import APIView

class ProductViewset(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

   
    
    @action(detail=False, methods=['get'],url_path='sorted_by_size/(?P<size>[^/.]+)')
    def sorted_by_size(self, request,size):
        
        if any(size == s[0] for s in SIZE):
            print("Size in SIZE")
            
            products = Product.objects.filter(size=size)
        else:
            products = Product.objects.all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    

    
    @action(detail=False, methods=['get'])
    def sorted_by_price(self, request):
        sort_order = request.query_params.get('order', 'asc')
        if sort_order == 'asc':
            products = Product.objects.all().order_by('price')
        elif sort_order=='desc':
            products = Product.objects.all().order_by('-price')
        else:
            products = Product.objects.all()
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    

# clas

class WishlistViewset(viewsets.ModelViewSet):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Wishlist.objects.filter(user=user)
        return Wishlist.objects.none()

    def perform_create(self, serializer):
        user = self.request.user
        if not Wishlist.objects.filter(user=user).exists():
            serializer.save(user=user)
        else:
            pass

    @action(detail=False, methods=['post'], url_path='add_product/(?P<product_id>\d+)')#/d ??
    def add_product(self, request, product_id=None):
        user = request.user
        
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        
        wishlist.products.add(product)
        return Response({'status': 'Product added to wishlist.'}, status=status.HTTP_200_OK)


    @action(detail=False, methods=['post'], url_path='remove_product/(?P<product_id>\d+)')
    def remove_product(self, request, product_id=None):
        user = request.user
        wishlist, created = Wishlist.objects.get_or_create(user=user)
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product does not exist.'}, status=status.HTTP_404_NOT_FOUND)
        wishlist.products.remove(product)
        return Response({'status': 'Product removed from wishlist.'}, status=status.HTTP_200_OK)



class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user)