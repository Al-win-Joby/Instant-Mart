from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models

class User(AbstractUser):
    name    = models.CharField(max_length=100)
    email   = models.EmailField(max_length=254, unique=True)
    phone   = models.IntegerField(blank=True)
    password= models.CharField(max_length=100)
    username =models.CharField(max_length=100,blank=True,unique=False) 
    is_user = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_store = models.BooleanField(default=False)
    location= models.PointField(null=True)
    
    USERNAME_FIELD ='email'
    REQUIRED_FIELDS=['username','phone'] 

class Store(models.Model):
    user                   = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    store_name             = models.CharField(max_length=100)


class Admin(models.Model):
    user                   = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
