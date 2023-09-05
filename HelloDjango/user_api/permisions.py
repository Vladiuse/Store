from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.contrib.auth.models import Group

class IsOwnerPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user and request.user == obj.owner


class IsOwnerPermissionsSafe(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user == obj.owner


class IsEmployee(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_employee


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


class _IsGroupOrReadOnly(BasePermission):
    GROUP_NAME = ''

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        group = Group.objects.get(name=self.GROUP_NAME)
        return request.user.groups.contains(group)

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        group = Group.objects.get(name=self.GROUP_NAME)
        return request.user.groups.contains(group)


class IsModeratorOrReadOnly(_IsGroupOrReadOnly):
    GROUP_NAME = 'moderator'