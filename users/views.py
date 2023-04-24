from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
import jwt,datetime
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework import generics, permissions
#from knox.models import AuthToken
from .serializers import  *
from .permissions import isMAdmin
from django.contrib.gis.geos import Point

class RegisterAdminAPI(generics.GenericAPIView):
    serializer_class = AdminRegisterSerializer
    #permission_classes = [isMAdmin]
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   
        individual = serializer.save()              
        #individual_data = IndividualSerializer(individual, context=self.get_serializer_context()).data        
        return Response(serializer.data)    
        
class RegisterStoreAPI(generics.GenericAPIView):    
    serializer_class = StoreRegisterSerializer  
    permission_classes = [isMAdmin]
    def post(self,request, *args, **kwargs):
        print(request.data)
        Data=request.data    
        
        serializer = self.get_serializer(data=Data) 
        serializer.is_valid(raise_exception=True)    
        individual = serializer.save()
        return Response(serializer.data)
 
class RegisterUserAPI(generics.GenericAPIView):   
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def post(self,request, *args, **kwargs):
        Data=request.data
        serializers =self.get_serializer(data=Data)
        #serializers['is_user']=True
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)
 
#from django_ratelimit.decorators import ratelimitkey, ratelimit
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.throttling import UserRateThrottle,AnonRateThrottle
class ThrottledTokenObtainPairView(TokenObtainPairView):
    throttle_classes = [AnonRateThrottle]
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)