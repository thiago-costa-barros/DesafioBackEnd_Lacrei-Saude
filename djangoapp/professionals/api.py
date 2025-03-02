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
                    success= True,
                    status_code= status.HTTP_201_CREATED,
                    message= "Profissional criado",
                    payload=payload)
                    , status.HTTP_201_CREATED)
            except Exception as e:
                error_details = {field: [str(err) for err in errors] for field, errors in e.detail.items()}
                return Response(ApiResponse(
                    success= False,
                    status_code= status.HTTP_400_BAD_REQUEST,
                    message="Erro ao criar profissional",
                    error=error_details)
                    , status.HTTP_400_BAD_REQUEST)
                
    def update(self, request, *args, **kwargs):
        with dbTransaction.atomic():
            try:
                instance = self.get_object()  # Obter instância existente

                # Atualizar TaxNumber se fornecido
                if 'taxnumber' in request.data and request.data['taxnumber']:
                    taxnumber_validate = isTaxNumberValid(request.data['taxnumber'])
                    if isinstance(taxnumber_validate, dict) and not taxnumber_validate.get('success', False):
                        return Response(taxnumber_validate, taxnumber_validate['status_code'])
                    request.data['taxnumber'] = re.sub("[^0-9]", '', request.data['taxnumber'])

                # Atualizar endereço se CEP fornecido
                if 'zipcode' in request.data and request.data['zipcode']:
                    zipcode_response = GetZipcode(request.data['zipcode'])
                    if not zipcode_response['success']:
                        return Response(zipcode_response, zipcode_response['status_code'])

                    request.data['zipcode'] = re.sub("[^0-9]", '', request.data['zipcode'])
                    zipcode_data = zipcode_response['data']

                    # Preencher os campos de endereço com os dados do CEP
                    request.data.update({
                        'adress_street': zipcode_data['logradouro'],
                        'adress_neighborhood': zipcode_data['bairro'],
                        'city': zipcode_data['localidade'],
                        'state': zipcode_data['uf']
                    })

                # Serializar e salvar
                serializer = self.get_serializer(instance, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                # Construir resposta formatada
                response_data = dict(serializer.data)
                response_data.pop('zipcode',None)
                response_data.pop('adress_street', None)
                response_data.pop('adress_neighborhood', None)
                response_data.pop('city', None)
                response_data.pop('state', None)
                response_data['adress'] = {
                    "zipcode": request.data.get("zipcode", instance.zipcode),
                    "street": request.data.get("adress_street", instance.adress_street),
                    "neighborhood": request.data.get("adress_neighborhood", instance.adress_neighborhood),
                    "city": request.data.get("city", instance.city),
                    "state": request.data.get("state", instance.state),
                }

                return Response(ApiResponse(
                    success=True,
                    status_code=status.HTTP_200_OK,
                    message="Profissional atualizado",
                    payload=response_data
                ), status=status.HTTP_200_OK)

            except KeyError as ke:
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message=f"Erro: Campo obrigatório ausente - {str(ke)}"
                ), status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                error_details = {field: [str(err) for err in errors] for field, errors in e.detail.items()}
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Erro ao atualizar profissional",
                    error=error_details
                ), status=status.HTTP_400_BAD_REQUEST)
        

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
                    success= True,
                    status_code= status.HTTP_201_CREATED,
                    message= "Profissão criada",
                    payload=serializer.data)
                    , status.HTTP_201_CREATED)
            except Exception as e:
                return Response(ApiResponse(
                    success= False,
                    status_code= status.HTTP_400_BAD_REQUEST,
                    message="Erro ao criar profissão",
                    error=str(e))
                    , status.HTTP_400_BAD_REQUEST)
