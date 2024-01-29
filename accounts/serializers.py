from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'birth_date']


class ConfirmCodeSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirm_code = serializers.IntegerField()


class UpdateDestroyAccount(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['avatar', 'first_name', 'last_name', 'email', 'phone_number', 'password']


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField()


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirm_code = serializers.IntegerField()