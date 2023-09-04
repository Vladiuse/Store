from rest_framework.permissions import BasePermission, SAFE_METHODS


class InGroupPermission(BasePermission):
    group_name = ''

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.groups.filter(name=self.group_name).exists()

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return request.user.groups.filter(name=self.group_name).exists()

class IsModeratorGroupPermission(InGroupPermission):
    group_name = 'moderator'

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
