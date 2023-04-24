from django.db import models
from users.models import User,Store
from django.template.defaultfilters import slugify
# Create your models here.
class category(models.Model):
    name        =models.CharField(max_length=200,unique=True)
    description =models.CharField(max_length=200)
    image       =models.ImageField(upload_to ='photos/category')
    #store       =models.ForeignKey(Store,on_delete=models.CASCADE)
    

class product(models.Model):
    name        =   models.CharField(max_length=200)
    #slugg       = models.CharField(max_length=200)
    slug        = models.CharField(max_length=80, blank=False, null=False)
    #image       =   models.ImageField(upload_to ='photos/category')
    category    =   models.ForeignKey(category,on_delete=models.CASCADE)
    MRP         =   models.IntegerField()
    SellingPrice=   models.IntegerField(default=0)
    stock       =   models.IntegerField()
    store       =   models.ForeignKey(Store,on_delete=models.CASCADE)
    description =   models.TextField(max_length=200,blank=True)

    def save(self, *args, **kwargs):        
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
class productsImage(models.Model):
    products=models.ForeignKey(product,on_delete=models.CASCADE, related_name='images')
    image  = models.ImageField(upload_to ='photos/category') 

class Size(models.Model):
    products    =   models.ForeignKey(product,on_delete=models.CASCADE, related_name='sizes')
    size        =   models.CharField(max_length=200)

class Colour(models.Model):
    products=models.ForeignKey(product,on_delete=models.CASCADE, related_name='colour')
    colour        =   models.CharField(max_length=200)

class Type(models.Model):
    products    =models.ForeignKey(product,on_delete=models.CASCADE, related_name='type')
    type        =   models.CharField(max_length=200)



