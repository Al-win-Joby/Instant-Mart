from django.shortcuts import render

# Create your views here.
from .serializers import CategorySerializer,ProductSerializer,StoreSerializer,UserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated,AllowAny
from .permissions import isStore,isUser
from .models import category,product,Type,Colour,Size
from django.core import serializers
from users.models import Store,User
from django.template.defaultfilters import slugify
#from geopy.distance import distance   
from django.contrib.gis.db.models.functions import Distance
from rest_framework import generics



class CategoryAPI(APIView):
    #permission_classes=[IsAuthenticated] 
    permission_classes = [isStore]
    def post(self,request):
        
        Data=request.data
        print(Data)
        serializer = CategorySerializer(data=Data)       
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:   
            return Response(serializer.errors)     
    
    def get(self,request):  
        list      =category.objects.all()
        serializer=CategorySerializer(list,many=True)         
        return Response(serializer.data)
    

class CategoryDetailsAPI(APIView):
    permission_classes=[isStore]
    def get(self,request,pk):
        cat=category.objects.get(id=pk)

        serializer= CategorySerializer(cat)
        #if serializer.is_valid(raise_exception=True):
        return Response(serializer.data) 
        
    def put(self,request,pk):
        
        cat=category.objects.get(id=pk)
        serializer=CategorySerializer(cat,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
 

class ProductAPI(APIView):
    permission_classes = [isStore]

    def get(self,request):
        Id= request.user.id
        storex=Store.objects.filter(user__id=Id).first()
        
        products    =product.objects.filter(store=storex)                
        serializer=ProductSerializer(products,many=True)
        return Response(serializer.data)


    def post(self,request):
 
        pk=request.user.id
        userobj=Store.objects.get(user=pk) 
        Data=request.data  
        print(userobj)   
        if 'Type' not in Data:
            Data['Type']=""
        
        if 'Size' not in Data:
            print("Keri")
            Data['Size']  =""
        
        if 'Colour' not in Data:
            Data['Colour']=""

        if userobj.product_set.filter(name=Data['name']).exists():                     
            Pproducts=userobj.product_set.filter(name=Data['name'])
            
            for p in Pproducts: 

                types=p.type.filter(type=Data['Type'])
                sizes=p.sizes.filter(size=Data['Size'])
                if  p.type.filter(type=Data['Type']).exists() and p.sizes.filter(size=Data['Size']).exists() and p.colour.filter(colour=Data['Colour']):
                    return Response("Product already exsist")
            
        if Data['Colour']=="":
            Data.pop("Colour")
        
        if Data['Size']=="":
            Data.pop("Size")

        if Data['Type']=="":
            Data.pop("Type")       

        if 'uploaded_images' not in Data:
            return Response({'Error':"Provide atleast one image"}) 
        elif 'MRP'not in Data or 'SellingPrice' not in Data:
            return Response({'Error':"Provid MRP and SellingPrice"},status=404)
        elif 'category' not in Data:
            return Response({'Error':'Select category'},status=404) 
        name=Data['name']
        # Data['slug']=slugify(name)
        # print("12")
        # print(Data['slug']) 
        Data['store']=pk    
        
        categories= category.objects.all()
        
        serializer = ProductSerializer(data=Data)
         
        if serializer.is_valid(raise_exception=True):           
            CategoryFound=False                         
            for cat in categories:                      
                if str(cat.id)==Data['category']:   
                    CategoryFound=True  
                    break 
        
        if CategoryFound==False:
            return Response("Invalid entry for category")
        
        serializer.save()
        return Response(serializer.data)


class ProductListinStoreAPI(APIView):
    permission_classes = [AllowAny]
    
    def get(self,request,pk):
        
        products=product.objects.filter(store=pk)
        print(products)
        serializers=ProductSerializer(products,many=True)
        return Response(serializers.data) 

from rest_framework import status
class  ShowProductAPI(APIView):
    permission_classes = [AllowAny]

    def get(self,request,pk,pslug):
        products=product.objects.filter(store=pk,slug=pslug)
        serializers=ProductSerializer(products,many=True)
        return Response(serializers.data) 

class ShowParticularProductAPIS(APIView):
    permission_classes = [isStore]
    def get(self,request,pid):
        storeid=request.user.id
        products=product.objects.filter(id=pid,store=storeid)

        if products:
            serializers=ProductSerializer(products,many=True)

            return Response(serializers.data)
        else:
            return Response("You do not have permission to access this product") 

 
    def put(self,request,pid):
        storeid=request.user.id
        
        products=product.objects.get(id=pid,store=storeid)
        serializer=ProductSerializer(products,data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            
            return Response(serializer.errors)

    def delete(self,request,pid):
        storeid=request.user.id
        if product.objects.filter(id=pid,store=storeid).exists():
            products=product.objects.get(id=pid,store=storeid)
            products.delete()
            return Response("Product deleted", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("No product with given ID")


class ShowIndividualProductAPI(APIView):
    permission_classes = [AllowAny]
    def get(self,request,pid):
        
        products=product.objects.filter(id=pid)
        serializers=ProductSerializer(products,many=True)
        return Response(serializers.data) 


class ShowfilteredProductAPI(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        Data=request.data

        try:
            max=Data['max']
        except:
            max=200000000000

        try: 
            min=Data['min']
        except:
            min=0
        #min=Data['min']
        if "search" not in Data:
            return Response("Search key not provided")
        
        if request.user.is_authenticated is False:
            products=product.objects.filter(name__icontains=Data['search']) 
            serializers=ProductSerializer(products,many=True) 

        else:
            loc=self.request.user.location
            prs= product.objects.annotate(distance=Distance('store__user__location',loc))
            prs=prs.filter(name__icontains=Data['search'],SellingPrice__gte=min,SellingPrice__lte=max).order_by('distance')[:5]
            serializers=ProductSerializer(prs,many=True) 

        return Response(serializers.data)


class ShowSearchedProductAPI(generics.ListAPIView):
    permission_classes=[AllowAny]
    serializer_class=ProductSerializer

    def get_queryset(self):        
        products = self.request.query_params.get('product',None)
        if self.request.user.is_authenticated is False:
            if cache.get(products):
                payload=cache.get(products)
                print("caching")
                return payload
            else:
                
                objs=product.objects.filter(name=products)  
                cache.set(products,objs)
            return objs #product.objects.filter(name=products)                

        else:            
            loc=self.request.user.location
            prs= product.objects.annotate(distance=Distance('store__user__location',loc))
            prs=prs.filter(name=products).order_by('distance')
            
            return prs

#######################
from django.core.cache import cache

class Trial(generics.ListAPIView):
    permission_classes=[AllowAny]
    serializer_class=ProductSerializer
    def get_queryset(self):  
        payload=[]     
        products = self.request.query_params.get('product',None)
        if cache.get(products):
            payload=cache.get(products)
            print("if")
            return payload
        else:

            objs=product.objects.filter(name=products)

            cache.set(products,objs)
        return product.objects.filter(name=products) 


  
class StoresAPI(APIView):
    permission_classes = [isUser]
        
    def get(self,request):
        loc=request.user.location
        query=User.objects.filter(location__distance_lte=(loc,10000),is_store=True).select_related('store')

        serializer=UserSerializer(query,many=True)        
        
        return Response(serializer.data)       




from chatapp.models import Conversation
import string
import random

import json
class SendMessage(APIView):
    permission_classes = [isUser]
    def get(self, request,pk):
        
        sender= request.user
        receiver= User.objects.get(id=pk)
        
        if not Conversation.objects.filter(sender=sender,receiver=receiver).exists():
            conversation = ''.join(random.choices(string.ascii_letters, k=10))

            Conversation.objects.create(sender=sender,receiver=receiver,room_name=conversation)
        else:
            obj=Conversation.objects.get(sender=sender,receiver=receiver)
            conversation=obj.room_name
        sender=serializers.serialize('json', [sender,],fields=('name',''))
        receiver= serializers.serialize('json',[receiver],fields=('name'))
        data = {
            'user1': json.loads(sender)[0]['fields'],
            'user2': json.loads(receiver)[0]['fields'],
            'roomname':conversation
        }
        return Response(data)
        

