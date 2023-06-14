from rest_framework.permissions import BasePermission, SAFE_METHODS


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

class OwnerPermissions(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user and request.user == obj.owner
