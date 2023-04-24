import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated,AllowAny
from .middleware import *
from . models import Messages,Conversation
#from channels.exceptions import WebSocketError
class ChatConsumer(WebsocketConsumer):
    
    def connect(self):                    
        self.user = self.scope['user']
        if self.user.is_authenticated:
            
            self.room_name = self.scope["url_route"]["kwargs"]["room_name"]            
            
            self.room_group_name = "chat_%s" % self.room_name

            # Join room group
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )

            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        # Leave room group
        self.user = self.scope['user']

        if self.user.is_authenticated:
            
            async_to_sync(self.channel_layer.group_discard)(
                self.room_group_name, self.channel_name
            )
        else:            
            pass  
 

    # Receive message from WebSocket
    def receive(self, text_data): 
        sender=self.scope['user']
        room=self.room_name
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]  
        con=Conversation.objects.get(room_name=room)
        Messages.objects.create(sender=sender,conversation=con,message=message) 
                            
        # Send message to room group                
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name, {"type": "chat_message", "message": message}
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]
        # Send message to WebSocket
        self.send(text_data=json.dumps({"message" : message})) 

        

    