from rest_framework.permissions import BasePermission


class IsSuperAdmin(BasePermission):
    """
    Custom permission to allow access only to SuperAdmin users.
    Checks that:
    - User is authenticated
    - User object exists
    - User has is_superuser = True
    Used to protect sensitive SuperAdmin-only endpoints.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and getattr(request.user, 'is_superuser', False))
