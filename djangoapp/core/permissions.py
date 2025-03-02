from rest_framework.permissions import BasePermission,SAFE_METHODS

class IsStaffUser(BasePermission):
    """
    Permite acesso apenas para usuários autenticados e que sejam staff.
    """

    def has_permission(self, request, view):
        """
            Verifica se o usuário está autenticado e permite requisições GET e POST.
            Para métodos GET, basta estar autenticado.
            Para demais métodos, precisa ser is_staff true
        """
        if request.method in SAFE_METHODS:  
            return request.user.is_authenticated  
        return request.user.is_authenticated and request.user.is_staff
    
    def has_object_permission(self, request, view, obj):
        """
            Permissão para métodos específicos em um objeto
            Para métodos GET, basta estar autenticado.
            Para demais métodos, precisa ser is_staff true
        """
        if request.method in SAFE_METHODS:
            return request.user.is_authenticated  
        
        if request.user.is_staff:
            return True 

class IsOwnerOrSuperUser(BasePermission):
    """
    Permite que apenas o criador do objeto ou um superusuário possa editar ou excluir.
    Outros usuários podem apenas visualizar e criar novos registros.
    """

    def has_permission(self, request, view):
        """
        Permite que usuários autenticados acessem:
        - POST: Qualquer usuário autenticado pode criar.
        - GET: Permitido apenas para visualizar os próprios registros.
        - PUT, PATCH, DELETE: Somente superusuários ou donos do objeto.
        """
        if request.method == "POST" or request.method in SAFE_METHODS:
            return request.user.is_authenticated  # Qualquer usuário autenticado pode criar ou visualizar

        return True

    def has_object_permission(self, request, view, obj):
        """
        - GET: Somente o dono ou superusuário pode visualizar.
        - PUT, PATCH, DELETE: Apenas se for superusuário ou dono do objeto.
        """
        return request.user.is_superuser or obj.creation_user_id == request.user

