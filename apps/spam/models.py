from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()

class SpamReport(models.Model):
    reported_by = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    report_date = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
