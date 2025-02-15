from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import HealthProfessional, Profession
from .serializers import HealthProfessionalSerializer, ProfessionSerializer
from core.permissions import IsStaffUser

class HealthProfessionalViewSet(viewsets.ModelViewSet):
    queryset = HealthProfessional.objects.all()
    serializer_class = HealthProfessionalSerializer
    permission_classes = [IsAuthenticated]  # Apenas autenticados podem acessar


class ProfessionViewSet(viewsets.ModelViewSet):
    queryset = Profession.objects.all()
    serializer_class = ProfessionSerializer
    permission_classes = [IsAuthenticated, IsStaffUser]