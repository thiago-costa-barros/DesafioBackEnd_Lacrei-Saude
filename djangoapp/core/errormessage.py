from rest_framework.views import exception_handler
from rest_framework import status
from core.utils import ApiResponse  # Função que criamos para formatar as respostas

def custom_exception_handler(exc, context):
    """
    Custom Exception Handler para padronizar respostas de erro
    """
    response = exception_handler(exc, context)

    if response is not None:
        # Mapeamento de status codes para mensagens personalizadas
        status_messages = {
            400: "Erro de validação",
            401: "Erro de autenticação",
            403: "Erro de permissão",
            404: "Recurso não encontrado",
            405: "Método não permitido",
            500: "Erro interno do servidor"
        }

        status_code = response.status_code
        default_message = status_messages.get(status_code, "Erro desconhecido")
        error_detail = response.data.get("detail", "Ocorreu um erro inesperado.")

        response.data = ApiResponse(
            success=False,
            status_code=status_code,
            message=default_message,
            error=error_detail
        )

    return response
