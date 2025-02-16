from rest_framework import serializers
from .models import HealthProfessional, Profession
from django.conf import settings

class HealthProfessionalSerializer(serializers.ModelSerializer):
    creation_user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = HealthProfessional
        fields = ['id','creation_user_id','update_user_id','full_name','social_name','email','profession','phone','taxnumber','zipcode','adress_street','adress_neighborhood','city','state'] 
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    
        
class ProfessionSerializer(serializers.ModelSerializer):
    creation_user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    update_user_id = serializers.HiddenField(default=serializers.CurrentUserDefault())
    
    class Meta:
        model = Profession
        fields = ['id','creation_user_id','update_user_id', 'name', 'description']
        
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    