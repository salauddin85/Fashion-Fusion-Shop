# from django.urls import path,include
# from rest_framework.routers import DefaultRouter
# from .views import WishlistViewset,ReviewViewset,ProductViewset
# from .import views

# router = DefaultRouter()
# router.register('product', ProductViewset,basename='product')
# # router.register('wishlist', WishlistViewset, basename='wishlist')
# router.register('review', ReviewViewset, basename='review')


# urlpatterns = [
#     path('', include(router.urls)),
#     path('sorted_by_size/<str:size>/', ProductViewset.as_view({'get': 'sorted_by_size'}), name='sorted-by-size'),
#     path('sort_by_price/', ProductViewset.as_view({'get': 'sort_by_price'}), name='sort-by-price'),
#     path('add_product/<int:id>',WishlistViewset.as_view(),name='wishlist')


# ]



from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WishlistViewset, ReviewViewset, ProductViewset

router = DefaultRouter()
router.register('product', ProductViewset, basename='product')
router.register('wishlist', WishlistViewset, basename='wishlist')
router.register('review', ReviewViewset, basename='review')

#sorted by color not implemented

urlpatterns = [
    path('', include(router.urls)),
    path('sorted_by_size/<str:size>/', ProductViewset.as_view({'get': 'sorted_by_size'}), name='sorted-by-size'),
    path('sorted_by_category/<str:category>/', ProductViewset.as_view({'get': 'sorted_by_category'}), name='sorted-by-category'),
    path('sorted_by_sub_category/<str:category>/', ProductViewset.as_view({'get': 'sorted_by_sub_category'}), name='sorted-by-sub-category'),
    path('sorted_by_color/<str:color>/', ProductViewset.as_view({'get': 'sorted_by_color'}), name='sorted-by-color'),
    path('sorted_by_price/', ProductViewset.as_view({'get': 'sorted_by_price'}), name='sorted-by-price'),
    path('wishlist/add_product/<int:product_id>/', WishlistViewset.as_view({'post': 'add_product'}), name='add-product-to-wishlist'),
    path('wishlist/remove_product/<int:product_id>/', WishlistViewset.as_view({'post': 'remove_product'}), name='remove-product-from-wish'),
]
