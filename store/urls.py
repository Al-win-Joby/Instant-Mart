from django.contrib import admin
from django.urls import path,include


from .views import *
urlpatterns = [
    path('admin/category/', CategoryAPI.as_view()),
    path('admin/category/<int:pk>/',CategoryDetailsAPI.as_view()), 
    path('product/',ProductAPI.as_view()),
    path('',StoresAPI.as_view()),

    path('<int:pk>/',ProductListinStoreAPI.as_view()),
    path('<int:pk>/<str:pslug>',ShowProductAPI.as_view()),   #store, product slug 
    
    path('Sproduct/<int:pid>',ShowParticularProductAPIS.as_view()),
    path('product/<int:pid>',ShowIndividualProductAPI.as_view()), 

    path('products/',ShowSearchedProductAPI.as_view()),
    path('trial',Trial.as_view()), 

    path('products/filter',ShowfilteredProductAPI.as_view()),
    path('<int:pk>/message/',SendMessage.as_view()),
    
]  
    
    
 
    
