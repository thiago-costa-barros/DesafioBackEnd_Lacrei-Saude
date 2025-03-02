from rest_framework.viewsets import ModelViewSet
from rest_framework.serializers import ValidationError
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
from django.utils.html import escape

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

        try:
            health_professional = escape(request.data.get("health_professional",""))
            #Check if health_professional is a string
            if not health_professional.isdigit():
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Erro no formato do profissional",
                    error="O ID do profissional deve ser um número inteiro."
                ), status=status.HTTP_400_BAD_REQUEST)

            health_professional = int(health_professional)  # Converte para inteiro após validação

            # Verifique aqui se o HealthProfessional realmente existe
            if not HealthProfessional.objects.filter(id=health_professional).exists():
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="Profissional não encontrado.",
                    error=f"Não foi encontrado um profissional com Id {health_professional}."
                ), status=status.HTTP_404_NOT_FOUND)
            
            appointment_date = escape(request.data.get("appointment_date", "").strip())
            appointment_time = escape(request.data.get("appointment_time", "").strip())
            
            if not health_professional or not appointment_date or not appointment_time:
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Dados inválidos: Campos obrigatórios ausentes.",
                    error="Preencha todos os campos corretamente."
                ), status=status.HTTP_400_BAD_REQUEST)
            try:
                appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
            except ValueError:
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Formato de data inválido",
                    error="A data deve estar no formato YYYY-MM-DD."
                ), status=status.HTTP_400_BAD_REQUEST)
            
            appointment_time = datetime.strptime(appointment_time, "%H:%M:%S").time()
            
        except ValueError as e:
            return Response(ApiResponse(
                success=False,
                status_code=status.HTTP_400_BAD_REQUEST,
                message="Erro no formato do horário.",
                error=str(e)
                ),status=status.HTTP_400_BAD_REQUEST
            )
                
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
                appointment = serializer.save(health_professional_id=request.data.get('health_professional'))

                # Construção da resposta correta
                response_data = dict(serializer.data)

                health_professional_obj = get_object_or_404(HealthProfessional, id=appointment.health_professional_id)
                profession_obj = get_object_or_404(Profession, id=health_professional_obj.profession_id)

                response_data['health_professional'] = {
                    "id": health_professional_obj.id,
                    "name": health_professional_obj.full_name,
                    "specialty": profession_obj.name
                }

                return Response(ApiResponse(
                    success=True,
                    status_code=status.HTTP_201_CREATED,
                    message="Agendamento Realizado",
                    payload=response_data
                ), status=status.HTTP_201_CREATED)
                
            except ValidationError as e:
                dbTransaction.set_rollback(True)
                error_details = {field: [str(err) for err in errors] for field, errors in e.detail.items()}
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    message="Erro de validação",
                    error=error_details
                ), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
            except IntegrityError as e:
                dbTransaction.set_rollback(True)
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Erro ao criar agendamento",
                    error=str(e)
                ), status=status.HTTP_400_BAD_REQUEST)
            
            except TypeError as e:
                dbTransaction.set_rollback(True)
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Erro ao criar agendamento",
                    error=str(e)
                ), status=status.HTTP_400_BAD_REQUEST)
                
            except Exception as e:
                dbTransaction.set_rollback(True)
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Erro ao criar agendamento",
                    error=str(e)
                ), status=status.HTTP_400_BAD_REQUEST)
    def update(self, request, *args, **kwargs):
        appointment_id = kwargs.get("pk")  # Obtém o ID do agendamento
        try:
            appointment = get_object_or_404(Appointment, id=appointment_id)
        except Exception:
            return Response(ApiResponse(
                success=False,
                status_code=status.HTTP_404_NOT_FOUND,
                message="Agendamento não encontrado",
                error=f"Não foi encontrado um agendamento com ID {appointment_id}."
            ), status=status.HTTP_404_NOT_FOUND)

        health_professional = request.data.get("health_professional")
        appointment_date = request.data.get("appointment_date")
        appointment_time = request.data.get("appointment_time")
        patient_name = request.data.get("patient_name")
        patient_phone = request.data.get("patient_phone")
        patient_email = request.data.get("patient_email")

        # Validações apenas se os campos foram passados
        if health_professional is not None:
            health_professional = escape(health_professional)
            if not health_professional.isdigit():
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Erro no formato do profissional",
                    error="O ID do profissional deve ser um número inteiro."
                ), status=status.HTTP_400_BAD_REQUEST)

            health_professional = int(health_professional)
            if not HealthProfessional.objects.filter(id=health_professional).exists():
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_404_NOT_FOUND,
                    message="Profissional não encontrado.",
                    error=f"Não foi encontrado um profissional com Id {health_professional}."
                ), status=status.HTTP_404_NOT_FOUND)

        if appointment_date is not None:
            appointment_date = escape(appointment_date.strip())
            try:
                appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
            except ValueError:
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Formato de data inválido",
                    error="A data deve estar no formato YYYY-MM-DD."
                ), status=status.HTTP_400_BAD_REQUEST)

        if appointment_time is not None:
            appointment_time = escape(appointment_time.strip())
            try:
                appointment_time = datetime.strptime(appointment_time, "%H:%M:%S").time()
            except ValueError:
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Erro no formato do horário.",
                    error="O horário deve estar no formato HH:MM:SS."
                ), status=status.HTTP_400_BAD_REQUEST)

        # Verifica se já existe um agendamento para o novo horário
        if health_professional or appointment_date or appointment_time:
            existing_appointment = Appointment.objects.filter(
                health_professional=health_professional if health_professional else appointment.health_professional_id,
                appointment_date=appointment_date if appointment_date else appointment.appointment_date,
                appointment_time=appointment_time if appointment_time else appointment.appointment_time
            ).exclude(id=appointment.id).exists()

            if existing_appointment:
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Horário inválido",
                    error="Já existe um agendamento neste horário."
                ), status=status.HTTP_400_BAD_REQUEST)

        with dbTransaction.atomic():
            try:
                # Atualiza apenas os campos que foram passados na requisição
                if health_professional is not None:
                    appointment.health_professional_id = health_professional
                if appointment_date is not None:
                    appointment.appointment_date = appointment_date
                if appointment_time is not None:
                    appointment.appointment_time = appointment_time
                if patient_name is not None:
                    appointment.patient_name = patient_name.strip()
                if patient_phone is not None:
                    appointment.patient_phone = patient_phone.strip()
                if patient_email is not None:
                    appointment.patient_email = patient_email.strip()

                appointment.save()

                # Construção da resposta correta
                response_data = {
                    "id": appointment.id,
                    "appointment_date": appointment.appointment_date.strftime("%Y-%m-%d"),
                    "appointment_time": appointment.appointment_time.strftime("%H:%M:%S"),
                    "patient": {
                        "patient_name": appointment.patient_name,
                        "patient_phone": appointment.patient_phone,
                        "patient_email": appointment.patient_email
                    }
                }

                health_professional_obj = get_object_or_404(HealthProfessional, id=appointment.health_professional_id)
                profession_obj = get_object_or_404(Profession, id=health_professional_obj.profession_id)

                response_data['health_professional'] = {
                    "id": health_professional_obj.id,
                    "name": health_professional_obj.full_name,
                    "specialty": profession_obj.name
                }

                return Response(ApiResponse(
                    success=True,
                    status_code=status.HTTP_200_OK,
                    message="Agendamento atualizado com sucesso",
                    payload=response_data
                ), status=status.HTTP_200_OK)

            except IntegrityError as e:
                dbTransaction.set_rollback(True)
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Erro ao atualizar agendamento",
                    error=str(e)
                ), status=status.HTTP_400_BAD_REQUEST)

            except Exception as e:
                dbTransaction.set_rollback(True)
                return Response(ApiResponse(
                    success=False,
                    status_code=status.HTTP_400_BAD_REQUEST,
                    message="Erro ao atualizar agendamento",
                    error=str(e)
                ), status=status.HTTP_400_BAD_REQUEST)
