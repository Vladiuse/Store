from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Employee
from django.contrib.auth.models import Group


class CreateEditBookPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_staff


class DeleteBookPermissions(BasePermission):

    def has_permission(self, request, view):
        if not request.method == 'DELETE':
            return True
        return bool(request.user and request.user.is_superuser)


class IsOwnerPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user and request.user == obj.owner


class _IsGroupPermissions(BasePermission):
    GROUP_NAME = ''

    def has_object_permission(self, request, view, obj):
        group = Group.objects.get(name=self.GROUP_NAME)
        return request.user.groups.contains(group)


class IsModeratorPermissions(_IsGroupPermissions):
    GROUP_NAME = 'moderator'

class IsManagerPermissions(_IsGroupPermissions):
    GROUP_NAME = 'manager'

class IsSellerPermissions(_IsGroupPermissions):
    GROUP_NAME = 'seller'
