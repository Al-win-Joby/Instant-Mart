from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import *

urlpatterns = [
    path('registerAdmin', RegisterAdminAPI.as_view()),
    path('registerStore', RegisterStoreAPI.as_view()),  
    path('registerUser', RegisterUserAPI.as_view()),    
    
    
    #path('login',LoginAPI.as_view()),
    # path('user',UserViews.as_view()),
    # path('logout',LogoutViews.as_view()),

    #path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/login',ThrottledTokenObtainPairView.as_view(), name='token_obtain_pair')

] 
  