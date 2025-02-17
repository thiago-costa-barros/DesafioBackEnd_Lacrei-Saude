from django.db import models

# Create your models here.
class Appointment(models.Model):
    
    def __str__(self):
        return 'Agendamento'
