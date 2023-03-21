from rest_framework import permissions
from .models import Friendship,Question

class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsFriend(permissions.BasePermission):
    """
    Custom permission to only allow friends of owner to view object.
    """

    def has_object_permission(self, request, view, obj):
        flag=Friendship.objects.filter(from_user=request.user,to_user=obj.user)
        flag=flag and obj.visible_to_friends
        if not flag:
            return False
        else:
            return True