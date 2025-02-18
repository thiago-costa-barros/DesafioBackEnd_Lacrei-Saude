from rest_framework.viewsets import ModelViewSet
from .models import Appointment
from .serializers import AppointmentSerializer
from rest_framework import status, permissions
from core.permissions import IsOwnerOrSuperUser
from rest_framework.response import Response
from core.utils import ApiResponse
from django.db import IntegrityError, transaction as dbTransaction
from django.shortcuts import get_object_or_404
from professionals.models import HealthProfessional, Profession
from datetime import datetime

class AppointmentModelViewSet(ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    
    def get_permissions(self):
        """Apenas usuários autenticados podem acessar"""
        return [permissions.IsAuthenticated(),IsOwnerOrSuperUser()]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return Appointment.objects.all()
        return Appointment.objects.filter(creation_user_id=self.request.user)
    
    def create(self, request, *args, **kwargs):
        
        health_professional = request.data.get("health_professional")
        appointment_date = request.data.get("appointment_date")
        appointment_time  = request.data["appointment_time"]
        appointment_time = datetime.strptime(appointment_time, "%H:%M:%S").time()
        print("Tipo de appointment_time:", type(appointment_time))
        print("Valor de appointment_time:", appointment_time)
        existing_appointment = Appointment.objects.filter(
            health_professional=health_professional,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).exists()
        if existing_appointment:
            return Response(ApiResponse(
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Horário inválido",
                error="Já existe um agendamento neste horário."
            ), status=status.HTTP_400_BAD_REQUEST)
            
        with dbTransaction.atomic():
            try:
                # Usar o serializer para salvar o HealthProfessional
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                
                response_data = dict(serializer.data)
                                
                health_professional_id = response_data.get('health_professional')
                health_professional_obj = get_object_or_404(HealthProfessional, id=health_professional_id)

                
                profession_id = health_professional_obj.profession_id
                profession_obj = get_object_or_404(Profession, id=profession_id)

                
                response_data['health_professional'] = {
                    "id": health_professional_obj.id,
                    "name": health_professional_obj.full_name,
                    "specialty": profession_obj.name  
                }
                
                payload = response_data

                return Response(ApiResponse(
                    success= True,
                    status_code= status.HTTP_201_CREATED,
                    message= "Profissional criado",
                    payload=payload)
                    , status.HTTP_201_CREATED)
            except Exception as e:
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Erro ao criar agendamento",
                    error=str(e)
                ), status=status.HTTP_400_BAD_REQUEST)