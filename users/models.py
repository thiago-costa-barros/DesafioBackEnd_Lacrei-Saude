from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.AutoField(primary_key=True, db_column="UserId")
    username = models.CharField(max_length=150, unique=True, db_column="Username")
    email = models.EmailField(unique=True, db_column="Email")
    first_name = models.CharField(max_length=30, db_column="FirstName")
    last_name = models.CharField(max_length=150, db_column="LastName")
    date_joined = models.DateTimeField(auto_now_add=True, db_column="DateJoined")
    is_active = models.BooleanField(default=True, db_column="IsActive")
    is_staff = models.BooleanField(default=False, db_column="IsStaff")
    is_superuser = models.BooleanField(default=False, db_column="IsSuperUser")
    password = models.CharField(max_length=128, db_column="Password")
    last_login = models.DateTimeField(null=True, blank=True, db_column="LastLogin")

    class Meta:
        db_table = "User"

    def __str__(self):
        return self.username
