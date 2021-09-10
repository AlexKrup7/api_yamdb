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
