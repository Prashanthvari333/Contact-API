from rest_framework import serializers

from apps.spam.models import SpamReport
from .models import User

class UserSerializer(serializers.ModelSerializer):
    spam_likelihood = serializers.SerializerMethodField()
    number_of_spam_reports  = serializers.SerializerMethodField()
    
    def get_number_of_spam_reports(self,obj):
        return SpamReport.objects.filter(phone_number=obj.phone_number).count()
    
    def get_spam_likelihood(self,obj):
        count = SpamReport.objects.filter(phone_number=obj.phone_number).count()
        if count==0:
             return "Not spam"
        elif (count<5):
            return "Likly spam"
        elif (count<10):
            return "Spam"
        else:
            return "Top spammer"
    
    class Meta:
        model = User
        fields = ['id','username', 'phone_number', 'email','spam_likelihood','number_of_spam_reports']
        extra_kwargs = {'email': {'required': False}}
    def create(self, validated_data):
        # Use the validated data to create a new User object
        return User.objects.create_user(**validated_data)