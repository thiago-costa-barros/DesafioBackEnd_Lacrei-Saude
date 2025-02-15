from rest_framework import serializers
from .models import HealthProfessional

class HealthProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProfessional
        fields = ['id', 'full_name', 'social_name', 'email', 'profession','zipcode'] 