from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """ User serializer """
    class Meta:
        # Fields to serialize
        model = User
        fields = ['id', 'username', 'email', 'password']
        
        
class LoginSerializer(serializers.Serializer):
    """ Login serializer to receive username and password """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
    