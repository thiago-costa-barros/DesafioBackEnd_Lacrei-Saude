from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsStaffUser(BasePermission):
    """
    Permite acesso apenas para usuários autenticados e que sejam staff.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:  
            return request.user.is_authenticated  
        return request.user.is_authenticated and request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        """Permissão para métodos específicos em um objeto"""
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated  # Qualquer um pode visualizar
        
        if request.user.is_staff:
            return True  # Staff pode tudo
    
class IsOwnerOrSuperUser(BasePermission):
    """
    Permite que apenas o criador do objeto ou um superusuário possa editar ou excluir.
    Outros usuários podem apenas visualizar.
    """
    
    def has_permission(self, request, view):
        """Verifica se o usuário está autenticado e permite requisições GET e POST."""
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        """Permissão para métodos específicos em um objeto"""
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated  # Qualquer um pode visualizar
        
        if request.user.is_superuser:
            return True  # Superuser pode tudo
        
        return obj.creation_user_id == request.user  # Apenas o criador pode editar ou excluir