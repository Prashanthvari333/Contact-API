from rest_framework import serializers
from .models import SpamReport

class SpamReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpamReport
        fields = ['id', 'phone_number', 'timestamp']