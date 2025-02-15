from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.response import Response
from django.db import transaction as dbTransaction
from .models import User 
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':  
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
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

                return Response(
                    {
                        "sucess": True,
                        "statusCode": status.HTTP_201_CREATED,
                        "message": "Usuário criado",
                        "payload":user_data
                        }, status=status.HTTP_201_CREATED)

            except Exception as e:
                return Response(
                    {
                        "sucess": False,
                        "statusCode": status.HTTP_400_BAD_REQUEST,
                        "message": "Erro ao criar usuário",
                        "error": str(e),
                        "payload":user_data
                        }, status=status.HTTP_400_BAD_REQUEST)
