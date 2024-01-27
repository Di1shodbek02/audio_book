from rest_framework import serializers

from .models import User


# class RegisterSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField(write_only=True)
#     confirmation_code = serializers.CharField(read_only=True)

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
