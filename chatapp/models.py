from django.db import models
from users.models import User

# Create your models here.


class Conversation(models.Model):
     sender    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')        
     receiver  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')   
     room_name = models.CharField(max_length=1200)


class Messages(models.Model):
     
     sender    = models.ForeignKey(User, on_delete=models.CASCADE)             
     conversation= models.ForeignKey(Conversation, on_delete=models.CASCADE)
     message   = models.CharField(max_length=1200)
     timestamp = models.DateTimeField(auto_now_add=True)
     is_read   = models.BooleanField(default=False)   #BooleanFeild(default=False)
       
     
     def __str__(self):
           return self.message
     class Meta:
           ordering = ('timestamp',) 