from rest_framework import serializers
from .models import Appointment
from professionals.models import HealthProfessional, Profession
from django.conf import settings
from datetime import datetime, date, time

class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['name']

class HealthProfessionalSerializer(serializers.ModelSerializer):
    profession = ProfessionSerializer(read_only=True)
    class Meta:
        model = HealthProfessional
        fields = ['id', 'full_name', 'profession', 'phone', 'email']

class PatientSerializer(serializers.Serializer):
    patient_name = serializers.CharField()
    patient_phone = serializers.CharField()
    patient_email = serializers.EmailField()

class AppointmentSerializer(serializers.ModelSerializer):
    creation_user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    patient = PatientSerializer(source='*', read_only=True)
    health_professional = serializers.PrimaryKeyRelatedField(queryset=HealthProfessional.objects.all(), write_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'health_professional', 'patient', 'patient_name', 'patient_phone', 'patient_email','appointment_date', 'appointment_time', 'creation_user_id', 'update_user_id']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Aqui você pode remover os campos individuais
        representation.pop('patient_name', None)
        representation.pop('patient_phone', None)
        representation.pop('patient_email', None)
        
        representation['health_professional'] = HealthProfessionalSerializer(instance.health_professional).data
        
        # O campo 'patient' já estará configurado
        return representation
    
    def validate_appointment_date(self, appointment_date):
        """Valida se a data do agendamento não está no passado."""
        today = date.today()
        try:
            if isinstance(appointment_date, str):
                appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
        except ValueError:
            raise serializers.ValidationError("A data deve estar no formato YYYY-MM-DD.")
        
        if appointment_date < today:
            raise serializers.ValidationError("A data do agendamento não pode estar no passado.")
        return appointment_date
    
    def validate_appointment_time(self, appointment_time):
        """Valida se o horário está dentro do intervalo permitido e se não está no passado para hoje."""
        now_time = datetime.now().time()
        
        if not (time(8, 0, 0) <= appointment_time <= time(19, 0, 0)):
            raise serializers.ValidationError("O horário deve estar entre 08:00 e 19:00.")
        
        request_data = self.initial_data  # Pegamos os dados da requisição
        appointment_date = request_data.get("appointment_date")
        
        if appointment_date:
            try:
                appointment_date = datetime.strptime(appointment_date, "%Y-%m-%d").date()
                if appointment_date == date.today() and appointment_time <= now_time:
                    raise serializers.ValidationError("O horário do agendamento não pode estar no passado.")
            except ValueError:
                raise serializers.ValidationError("Formato de data inválido. Use o formato YYYY-MM-DD.")

        return appointment_time
    
    def update(self, instance, validated_data):
        """Validação e lógica para atualização do agendamento"""
        try:
            # Verificando se o horário foi alterado
            new_appointment_time = validated_data.get('appointment_time', instance.appointment_time)
            print(f"Novo horário de agendamento: {new_appointment_time}")  # Adicionando debug para verificação do horário

            # Verificando se o horário está dentro do intervalo permitido
            if not (time(8, 0, 0) <= new_appointment_time <= time(19, 0, 0)):
                print(f"Erro: {new_appointment_time} não está dentro do intervalo permitido.")
                raise serializers.ValidationError("O horário deve estar entre 08:00 e 19:00.")
            
            # Verificando se já existe um agendamento para o mesmo horário no mesmo dia
            existing_appointment = Appointment.objects.filter(
                health_professional=instance.health_professional,
                appointment_date=instance.appointment_date,
                appointment_time=new_appointment_time
            ).exclude(id=instance.id)  # Exclui o próprio agendamento sendo atualizado

            if existing_appointment.exists():
                print(f"Erro: Já existe um agendamento neste horário para o profissional.")
                raise serializers.ValidationError("Já existe um agendamento neste horário.")

            # Se todas as validações passarem, faz o update normalmente
            print(f"Atualizando agendamento com o horário: {new_appointment_time}")
            return super().update(instance, validated_data)
        
        except Exception as e:
            print(f"Erro ao tentar atualizar: {str(e)}")  # Exibindo o erro completo
            raise serializers.ValidationError(f"Erro inesperado ao tentar atualizar o agendamento: {str(e)}")