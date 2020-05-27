from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOWnerOrReadOnly(BasePermission):
    message = 'UNAUTHORIZED!'

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.username == request.user.username