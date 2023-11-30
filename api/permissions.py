from rest_framework.permissions import BasePermission


class NotAuthenticated(BasePermission):
    def has_permission(self, request, view) -> bool:
        result = not bool(request.user and request.user.is_authenticated)
        return result
