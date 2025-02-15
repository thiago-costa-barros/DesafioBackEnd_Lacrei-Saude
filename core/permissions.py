from rest_framework.permissions import BasePermission

class IsStaffUser(BasePermission):
    """
    Permite acesso apenas para usuários autenticados e que sejam staff.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.is_staff