from rest_framework import serializers
from .models import HealthProfessional, Profession

class HealthProfessionalSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProfessional
        fields = ['id','full_name','social_name','email','profession','phone','taxnumber','zipcode','adress_street','adress_neighborhood','city','state'] 
        
class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ['id', 'name', 'description']