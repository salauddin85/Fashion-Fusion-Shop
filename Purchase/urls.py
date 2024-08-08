from django.urls import path, include
from .views import PurchaseProductView
from rest_framework.routers import DefaultRouter
 

# router = DefaultRouter()
# router.register('list',PurchaseProductView, basename='purchase')
urlpatterns = [
    # path('', include(router.urls)),
    path("list/<int:id>",PurchaseProductView.as_view(),name='purchase')

] 