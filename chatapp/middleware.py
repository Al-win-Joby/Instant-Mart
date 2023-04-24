# myapp/middleware.py

from channels.auth import AuthMiddlewareStack
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from jwt import decode, InvalidTokenError
from auth.settings import SECRET_KEY
from users.models import User
@database_sync_to_async
def get_user(scope,id):
    # Retrieve the user object from the Django ORM based on the WebSocket scope
    print(id)
    return User.objects.get(id=id)

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        try:
            # Extract the JWT token from the WebSocket scope
            token = scope["query_string"].decode().split("=")[1]
            print(token)
            # Verify the token and decode its payload
            payload = decode(token, SECRET_KEY, algorithms=["HS256"])
            
            # Retrieve the user object based on the payload
            user = await get_user(scope, payload["user_id"])
            # Add the user object to the WebSocket scope
            scope["user"] = user
            
            
        except (InvalidTokenError, KeyError):
            # If the token is invalid or missing, set the user to AnonymousUser
            scope["user"] = AnonymousUser()
        return await self.inner(scope, receive, send)


