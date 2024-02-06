from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import User


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'birth_date']


class ConfirmCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirm_code = serializers.IntegerField()


class UpdateDestroyAccountSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'phone_number']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetLoginSerializer(serializers.Serializer):
    new_password = serializers.CharField()


class UserInfo(ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar')


class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
