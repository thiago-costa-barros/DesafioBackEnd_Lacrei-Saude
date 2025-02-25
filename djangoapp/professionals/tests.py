from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken  # Importar para gerar o token
from users.models import User
from .models import Profession, HealthProfessional

class ProfessionModelTest(APITestCase):
    def setUp(self):
        User.objects.all().delete()
        Profession.objects.all().delete()
        
        # Criando um usuário admin
        self.user_data = {
            "username": "testAdminUser01",
            "password": "123456",
            "email": "admin@email.com",
            "first_name": "Admin",
            "last_name": "User"
        }
        self.admin_user = User.objects.create_superuser(**self.user_data)

        # Gerar token de acesso para o admin
        self.token = str(AccessToken.for_user(self.admin_user))

        # Definir cabeçalhos da requisição com o token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        # Criar uma profissão
        self.profession_data = {
            "name": "Profissão 01",
            "description": "Descrição da Profissão 01"
        }
        self.profession = Profession.objects.create(**self.profession_data)
        
        self.health_professional_data = {
            "full_name": "Profissional 01",
            "social_name": "Profissional 01",
            "profession": self.profession,
            "zipcode": "12345-678",
            "adress_street": "Rua Exemplo",
            "adress_neighborhood": "Bairro Exemplo",
            "city": "Cidade Exemplo",
            "state": "Estado Exemplo",
            "phone": "123456789",
            "email": "test@email.com"
        }
        self.health_professional = HealthProfessional.objects.create(**self.health_professional_data)

    def test_create_profession(self):
        # Verificar se o usuário admin foi criado corretamente
        self.assertIsNotNone(self.admin_user)
        self.assertTrue(self.admin_user.is_superuser)
        self.assertTrue(self.admin_user.is_staff)

        # Verificar profession criado
        profession = Profession.objects.get(name='Profissão 01')
        self.assertIsNotNone(profession)
        self.assertEqual(profession.description, 'Descrição da Profissão 01')
        
        # Verificar health professional criado
        health_professional = HealthProfessional.objects.get(full_name='Profissional 01')
        self.assertIsNotNone(health_professional)
        self.assertEqual(health_professional.profession.id, self.profession.id)
        self.assertEqual(health_professional.profession.name, 'Profissão 01')
