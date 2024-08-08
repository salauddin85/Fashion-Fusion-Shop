from rest_framework.routers import DefaultRouter
from django.urls import path, include
from  .views import  UserRegistrationApiView,UserLoginApiView,activate,UserLogoutView
router = DefaultRouter() # amader router
from .import views

urlpatterns = [
   
    path('register/', UserRegistrationApiView.as_view(), name='register'),
    path('login/', UserLoginApiView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('active/<uid64>/<token>/', views.activate, name = 'activate'),
   
]
