from rest_framework.permissions import SAFE_METHODS, BasePermission

from users.models import UserRole


class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and (
                request.user.role == UserRole.ADMIN
                or request.user.is_superuser)
        )

    def has_object_permission(self, request, view, obj):
        return True


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated and (
                request.user.role == UserRole.ADMIN
                or request.user.is_superuser)
        )


class IsOwnerOrModeratorOrAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (obj.owner == request.user
                or (request.user.role in (UserRole.ADMIN, UserRole.MODERATOR)
                    or request.user.is_superuser))
