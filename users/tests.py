from rest_framework.test import APITestCase
from users.models import User

class UserModelTest(APITestCase):
    def setUp(self):
        User.objects.all().delete()
        
        self.user_data = {
            "username": "testUser01",
            "password": "654123",
            "email": "testUser01@email.com",
            "first_name":"testUser01",
            "last_name":"testUser01"
        }
        
        self.supuser_data = {
            "username": "testAdminUser01",
            "password": "654123",
            "email": "testAdminUser01@email.com",
            "first_name":"testAdminUser01",
            "last_name":"testAdminUser01"
        }
        
        self.user = User.objects.create_user(**self.user_data)
        
        self.superuser = User.objects.create_superuser(**self.supuser_data)
        
    def test_create_user(self):
            user = User.objects.get(username='testUser01')
            
            self.assertFalse(user.is_superuser)
            self.assertFalse(user.is_staff)
            
    def test_create_admin_user(self):

            user_admin = User.objects.get(username='testAdminUser01')
            
            self.assertIsNotNone(user_admin)
            self.assertTrue(user_admin.is_superuser)
            self.assertTrue(user_admin.is_staff)
            
            
