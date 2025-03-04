from django.db import models
from django.conf import settings

class HealthProfessional(models.Model):
    id = models.AutoField(primary_key=True, db_column="HealthProfessionalId")
    full_name = models.CharField(max_length=255,null=False, db_column="TrandingName" ) 
    social_name = models.CharField(max_length=255, blank=True, null=True, db_column="SocialName")
    profession = models.ForeignKey('Profession', on_delete=models.SET_NULL, null=True, db_column="ProfessionId")
    zipcode = models.CharField(max_length=10,null=False, db_column="ZipCode") 
    adress_street = models.TextField(max_length=255, blank=True, null=True, db_column="AddressStreet")
    adress_neighborhood = models.TextField(max_length=255,blank=True, null=True, db_column="AddressNeighborhood")
    adress_number = models.CharField(max_length=10, blank=True, null=True, db_column="AddressNumber")
    city = models.CharField(max_length=100, db_column="City") 
    state = models.CharField(max_length=100, db_column="State")
    phone = models.CharField(max_length=20,null=False, db_column="Phone")
    email = models.EmailField(max_length=100,null=False, db_column="Email")
    taxnumber = models.CharField(max_length=20,unique=True,error_messages={"unique": "Um profissional com esse CPF já existe."}, db_column="TaxNumber")
    created_at = models.DateTimeField(auto_now_add=True, db_column="CreationDate")
    updated_at = models.DateTimeField(auto_now=True, db_column="UpdateDate")
    deleted_at = models.DateTimeField(null=True, blank=True, db_column="DeletionDate")
    creation_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='health_professionals_created', db_column="CreationUserId")
    update_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='health_professionals_updated', db_column="UpdateUserId")
       
    class Meta:
        db_table = "HealthProfessional"
    
    def __str__(self):
        profession_name = self.profession.name if self.profession else "Sem Profissão"
        
        if self.social_name:
            return f"{self.id} - {self.social_name} ({profession_name})"
        return f"{self.id} - {self.full_name} ({profession_name})"
    
class Profession(models.Model):
    id = models.AutoField(primary_key=True, db_column="ProfessionId")
    name = models.CharField(max_length=100, db_column="Name")
    description = models.TextField(max_length=255, db_column="Description")
    
    created_at = models.DateTimeField(auto_now_add=True, db_column="CreationDate")
    updated_at = models.DateTimeField(auto_now=True, db_column="UpdateDate")
    deleted_at = models.DateTimeField(null=True, blank=True, db_column="DeletionDate")
    creation_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='professions_created', db_column="CreationUserId")
    update_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='professions_updated', db_column="UpdateUserId")
    
    class Meta:
        db_table = "Profession"

    def __str__(self):
        return f'{self.id} - {self.name}'