from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):
    """Only CabZy admin team can access these endpoints."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_cab_admin
    
    