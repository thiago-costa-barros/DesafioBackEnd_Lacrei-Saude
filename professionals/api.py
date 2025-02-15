from rest_framework.viewsets import ModelViewSet
from .models import HealthProfessional
from .serializers import HealthProfessionalSerializer


class ProfessionalViewSet(ModelViewSet):
    queryset = HealthProfessional.objects.all()
    serializer_class = HealthProfessionalSerializer

