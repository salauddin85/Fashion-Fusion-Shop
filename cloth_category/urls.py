from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import CategoryApiView
router = DefaultRouter()

router.register('list',CategoryApiView, basename='category')

urlpatterns = [
    path('', include(router.urls)),
    # path('list/', CategoryApiView.as_view(), name='category-list'),

]