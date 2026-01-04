from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import User

class IsSellerOrReadOnly(BasePermission): 
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS: 
            return True
        return bool(request.user and request.user.is_authenticated and (request.user.role == User.SELLER))
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS: 
            return True
        if request.method == 'DELETE': 
            return bool(obj.seller == request.user or request.user.is_staff)
        return bool(obj.seller == request.user)
    
    
class IsBuyerOrReadOnly(BasePermission): 
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS: 
            return True
        return bool(request.user and request.user.is_authenticated and (request.user.role == User.BUYER))
