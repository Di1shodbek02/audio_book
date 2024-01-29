from django.contrib.auth import get_user_model
from passlib.context import CryptContext
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ConfirmCodeSerializer, ForgetPasswordSerializer, ResetPasswordSerializer
from django.core.cache import cache
from rest_framework.generics import GenericAPIView
import random

from .tasks import send_email

User = get_user_model()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def generate_confirmation_code(self):
        return random.randrange(10000, 99999)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        birth_date = serializer.validated_data['birth_date']

        confirmation_code = self.generate_confirmation_code()

        cache_data = {
            'username': username,
            'password': password,
            'birth_date': birth_date,
            'confirmation_code': confirmation_code
        }
        cache.set(email, cache_data, timeout=300)

        send_email.delay(email, confirmation_code)
        return Response({'confirmation_code': confirmation_code}, status=status.HTTP_201_CREATED)


class ConfirmCodeApiView(GenericAPIView):
    serializer_class = ConfirmCodeSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        confirm_code = request.data.get('confirm_code')
        cached_data = cache.get(email)

        if cached_data and confirm_code == cached_data['confirmation_code']:
            username = cached_data['username']
            password = cached_data['password']
            birth_date = cached_data['birth_date']

            if User.objects.filter(email=email).exists():
                return Response({'success': False, 'message': 'This email already exists!'}, status=400)
            else:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    username=username,
                    birth_date=birth_date,
                )
                return Response({'success': True})
        else:
            return Response({'message': 'The entered code is not valid!'}, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordApiView(GenericAPIView):
    serializer_class = ForgetPasswordSerializer

    def generate_confirmation_code(self):
        return random.randrange(10000, 99999)

    def post(self, request):
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        confirmation_code = self.generate_confirmation_code()
        data = {'confirmation_code': confirmation_code,
                'new_password': new_password
                }
        cache.set(email, data, timeout=300)
        send_email.delay(email, confirmation_code)

        return Response({'confirmation_code': confirmation_code}, status=status.HTTP_200_OK)


class ResetPasswordApiView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        email = request.data.get('email')
        confirm_code = request.data.get('confirm_code')

        cached_data = cache.get(email)
        if cached_data.get('confirmation_code') == confirm_code:
            user = User.objects.get(email=email)
            password = pwd_context.hash(cached_data.get('new_password'))
            user.set_password(password)
            user.save()
            return Response({'success': True}, status=status.HTTP_200_OK)
        return Response({'message': 'Confirm code is not valid!'})
