from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser is True:
            return True
        return request.user == obj.author


class IsModeratorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser is True:
            return True
        return request.user.is_authenticated and request.user.is_moderator


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_superuser is True:
            return True
        return (request.user.is_authenticated and request.user.is_admin)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser is True:
            return True
        return (request.user.is_authenticated and request.user.is_admin)


class IsAuthenticatedThenPostAllow(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser is True:
            return True
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST' and request.user.is_authenticated:
            return True
        return (
            request.user.is_admin
            or request.user.is_moderator
            or request.user == obj.author
        )
