from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

class User(AbstractUser):
    
    username = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=12, unique=True)
    email = models.EmailField(blank=True, null=True)
    password = models.CharField(max_length=120)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Add this field
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    objects = UserManager()
    
    @property
    def is_superuser(self):
        return self.is_admin
    
    def validate_password(self,password):
        return self.password == password
