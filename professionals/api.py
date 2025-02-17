import re
from rest_framework.viewsets import ModelViewSet
from rest_framework import status, permissions
from rest_framework.response import Response
from django.db import transaction as dbTransaction
from core.utils import ApiResponse
from .models import HealthProfessional, Profession
from .serializers import HealthProfessionalSerializer, ProfessionSerializer
from core.permissions import IsStaffUser, IsOwnerOrSuperUser
from integrationsystem.external_apis.zipcode import GetZipcode
from .validator import isTaxNumberValid

class HealthProfessionalViewSet(ModelViewSet):
    queryset = HealthProfessional.objects.all()
    serializer_class = HealthProfessionalSerializer

    def get_permissions(self):
        """Apenas usuários autenticados podem acessar"""
        return [permissions.IsAuthenticated(),IsOwnerOrSuperUser()]
    
    def get_queryset(self):
        """Superusuário vê tudo, usuários comuns só veem seus próprios registros"""
        if self.request.user.is_superuser:
            return HealthProfessional.objects.all()
        return HealthProfessional.objects.filter(creation_user_id=self.request.user)
    
    def create(self, request, *args, **kwargs):
        with dbTransaction.atomic():
            try:
                
                taxnumber_validate = isTaxNumberValid(request.data['taxnumber'])
                if isinstance(taxnumber_validate, dict) and not taxnumber_validate.get('success', False):
                    return Response(taxnumber_validate, taxnumber_validate['status_code'])
                request.data['taxnumber'] = re.sub("[^0-9]",'',request.data['taxnumber'])
                
                zipcode_response = GetZipcode(request.data['zipcode'])
                if not zipcode_response['success']:
                    return Response(zipcode_response, zipcode_response['status_code'])
                request.data['zipcode'] = re.sub("[^0-9]",'',request.data['zipcode'])

            
                zipcode_data = zipcode_response['data']
                
                # Passar as informações do CEP para os campos de endereço
                request.data['adress_street'] = zipcode_data['logradouro']
                request.data['adress_neighborhood'] = zipcode_data['bairro']
                request.data['city'] = zipcode_data['localidade']
                request.data['state'] = zipcode_data['uf']
                
                # Usar o serializer para salvar o HealthProfessional
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                
                response_data = dict(serializer.data)
                
                response_data.pop('zipcode',None)
                response_data.pop('adress_street', None)
                response_data.pop('adress_neighborhood', None)
                response_data.pop('city', None)
                response_data.pop('state', None)
                response_data['adress'] = {
                    "zipcode":zipcode_data['cep'],
                    "street": zipcode_data['logradouro'],
                    "neighborhood": zipcode_data['bairro'],
                    "city": zipcode_data['localidade'],
                    "state": zipcode_data['uf']
                }
                payload = response_data
                return Response(ApiResponse(
                    sucess= True,
                    status_code= status.HTTP_201_CREATED,
                    message= "Profissional criado",
                    payload=payload)
                    , status.HTTP_201_CREATED)
            except Exception as e:
                return Response(ApiResponse(
                    sucess= False,
                    status_code= status.HTTP_400_BAD_REQUEST,
                    message="Erro ao criar profissional",
                    error=str(e))
                    , status.HTTP_400_BAD_REQUEST)

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
