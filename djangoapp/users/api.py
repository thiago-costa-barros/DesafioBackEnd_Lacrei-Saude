from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from core.utils import ApiResponse
from django.db import transaction as dbTransaction
from .models import User 
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':  
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        user_data = request.data.copy()
        with dbTransaction.atomic():  # Garantia de atomicidade
            try:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)  # Levanta erro automaticamente se inválido
                
                user = serializer.save()

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                refresh_token = str(refresh)

                user_data = serializer.data
                user_data['tokens'] = {
                    'access': access_token,
                    'refresh': refresh_token
                }

                return Response(ApiResponse(
                        success= True,
                        status_code= status.HTTP_201_CREATED,
                        message= "Usuário criado",
                        payload=user_data)
                        , status.HTTP_201_CREATED)

            except Exception as e:
                # Captura erros de validação específicos e resposta padronizada
                if isinstance(e, ValidationError):
                    error_details = serializer.errors  # Captura erros específicos do serializer
                else:
                    error_details = str(e)  # Outros erros inesperados
                return Response(ApiResponse(
                        success= False,
                        status_code= status.HTTP_400_BAD_REQUEST,
                        message="Erro ao criar usuário",
                        error=error_details,
                        payload=user_data)
                        , status.HTTP_400_BAD_REQUEST)
