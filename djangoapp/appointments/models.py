from django.db import models
from django.conf import settings

# Create your models here.
class Appointment(models.Model):
    id = models.AutoField(primary_key=True, db_column="AppointmentId")
    health_professional = models.ForeignKey('professionals.HealthProfessional',null=False, on_delete=models.CASCADE, db_column="HealthProfessionalId")
    patient_name = models.CharField(max_length=255,null=False, db_column="PatientName")
    patient_phone = models.CharField(max_length=20, null=False, db_column="PatientPhone")
    patient_email = models.EmailField(max_length=100,null=False,  db_column="PatientEmail")
    appointment_date = models.DateField(null=False,db_column="AppointmentDate")
    appointment_time = models.TimeField(null=False,db_column="AppointmentTime")
    created_at = models.DateTimeField(auto_now_add=True, db_column="CreationDate")
    updated_at = models.DateTimeField(auto_now=True, db_column="UpdateDate")
    deleted_at = models.DateTimeField(null=True, blank=True, db_column="DeletionDate")
    creation_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='appointments_created', db_column="CreationUserId")
    update_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='appointments_updated', db_column="UpdateUserId")

    class Meta:
        db_table = "Appointment"
        unique_together = ("appointment_date", "appointment_time", "health_professional")
    
    def __str__(self):
        return f'Agendamento - {self.id}: \nProfissional: {self.health_professional}\nData: {self.appointment_date} {self.appointment_time}\nNome do Paciente: {self.patient_name}' 
