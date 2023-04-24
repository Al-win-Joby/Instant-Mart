
from rest_framework import permissions

class isMAdmin(permissions.BasePermission):
    def has_permission(self,request,view):
        if not request.user.is_authenticated:
            
            return False
        Mainadminpermission= bool(request.user and request.user.is_admin and request.user.is_authenticated)
        return Mainadminpermission  