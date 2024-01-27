from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ConfirmCodeSerializer
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework.generics import GenericAPIView
import random

User = get_user_model()


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

        confirmation_code = self.generate_confirmation_code()

        cache_data = {
            'username': username,
            'password': password,
            'confirmation_code': confirmation_code
        }
        cache.set(email, cache_data, timeout=300)

        send_mail(
            'Registration Confirmation Code',
            f'Your confirmation code is: {confirmation_code}',
            'from@example.com',
            [email],
            fail_silently=False,
        )
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

            if User.objects.filter(email=email).exists():
                return Response({'success': False, 'message': 'This email already exists!'}, status=400)
            else:
                user = User.objects.create_user(
                    email=email,
                    password=password,
                    username=username,
                )
                return Response({'success': True})
        else:
            return Response({'message': 'The entered code is not valid!'}, status=status.HTTP_400_BAD_REQUEST)
