from rest_framework.permissions import BasePermission

class RolePermission(BasePermission):
    allowed_roles = set()

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.auth.get("role") in self.allowed_roles
