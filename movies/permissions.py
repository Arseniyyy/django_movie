from rest_framework import permissions
from rest_framework.request import Request

from movies.models import Actor


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    View-level permission to only allow staff users to edit objects.
    """

    def has_permission(self, request: Request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj: Actor):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
