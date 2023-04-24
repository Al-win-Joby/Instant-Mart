
from rest_framework import permissions

class isStore(permissions.BasePermission):
    def has_permission(self,request,view):
        if not request.user.is_authenticated:
            
            return False
        Mainadminpermission= bool(request.user and request.user.is_store and request.user.is_authenticated)
        return Mainadminpermission  

class isUser(permissions.BasePermission):
    def has_permission(self,request,view):
        if not request.user.is_authenticated:
            
            return False
        Mainadminpermission= bool(request.user and request.user.is_user and request.user.is_authenticated)
        return Mainadminpermission 