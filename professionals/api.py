from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.response import Response
from django.db import transaction as dbTransaction
from core.utils import ApiResponse
from .models import HealthProfessional, Profession
from .serializers import HealthProfessionalSerializer, ProfessionSerializer
from core.permissions import IsStaffUser  # Importando a permissão personalizada

class HealthProfessionalViewSet(ModelViewSet):
    queryset = HealthProfessional.objects.all()
    serializer_class = HealthProfessionalSerializer

    def get_permissions(self):
        """Apenas usuários autenticados podem acessar"""
        return [permissions.IsAuthenticated()]


class ProfessionViewSet(ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer

    def get_permissions(self):
        """Apenas usuários autenticados e staff podem acessar"""
        return [permissions.IsAuthenticated(), IsStaffUser()]
    
    def create(self, request, *args, **kwargs):
        with dbTransaction.atomic():
            try:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(ApiResponse(
                    sucess= True,
                    status_code= status.HTTP_201_CREATED,
                    message= "Profissão criada",
                    payload=serializer.data)
                    , status.HTTP_201_CREATED)
            except Exception as e:
                return Response(ApiResponse(
                    sucess= False,
                    status_code= status.HTTP_400_BAD_REQUEST,
                    message="Erro ao criar profissão",
                    error=str(e))
                    , status.HTTP_400_BAD_REQUEST)
