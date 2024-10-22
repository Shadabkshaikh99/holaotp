from rest_framework import serializers
from django.contrib.auth.models import User
from .models import OTP

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username']

class OTPSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = OTP
        fields = ['id', 'user', 'otp_code', 'expires_at', 'verified']
        read_only_fields = ['user', 'expires_at', 'verified']
