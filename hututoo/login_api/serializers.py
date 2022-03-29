from dataclasses import field
from rest_framework import serializers
from .models import *



class VerifyUserOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()


class RegitsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ['id', 'email', 'is_verified']

class RegitserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'is_verified']


class RegitserSerializerTransaction(serializers.ModelSerializer):
    class Meta:
        model = RegisterUser
        fields = ['email']

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    # otp = serializers.CharField()
    # is_verified = serializers.BooleanField()
    # is_active = serializers.BooleanField()


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['user'] = RegitserSerializer(instance.user).data
        return rep
