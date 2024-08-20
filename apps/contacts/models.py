
from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.

User = get_user_model()

# Create your models here.
class Contact(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='contacts',db_constraint=False)
    name = models.CharField(max_length=500)
    phone_number = models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
