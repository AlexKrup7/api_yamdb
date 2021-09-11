from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import UserRole


class AdminPermissionOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.role == UserRole.ADMIN
            or request.user.is_superuser
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_superuser
                or request.auth and request.user.role == UserRole.ADMIN)


class ReviewPermission(BasePermission):
    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in SAFE_METHODS or
                obj.author == request.user or
                request.user.role in ['admin', 'moderator'])