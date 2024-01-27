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

        confirmation_code = self.generate_confirmation_code()

        cache.set(email, confirmation_code, timeout=300)

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
        password = request.data.get('password')
        username = request.data.get('username')

        cached_confirm_code = cache.get(email)
        if confirm_code == cached_confirm_code:
            user, created = User.objects.get_or_create(email=email)

            if created:
                user.set_password(password)
                user.username = username
                user.save()
                return Response({'message': True})
            else:
                return Response({'message': 'User already exists.'})

        return Response({'message': 'The entered code is not valid!'})
