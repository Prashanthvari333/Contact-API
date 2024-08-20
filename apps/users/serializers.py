from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password', 'phone_number', 'email']
        extra_kwargs = {'email': {'required': False}}