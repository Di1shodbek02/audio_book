
from rest_framework import generics, status
from rest_framework.response import Response
from .serializers import RegisterSerializer, ConfirmCodeSerializer
from django.core.cache import cache
from django.core.mail import send_mail
from rest_framework.generics import GenericAPIView
import random


class RegistrationAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def generate_confirmation_code(self):
        return random.randrange(10000, 99999)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        confirmation_code = self.generate_confirmation_code()

        cache.set(email, confirmation_code, timeout=300)  # 5 minutes timeout

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

        cached_confirm_code = cache.get(email)
        if confirm_code == cached_confirm_code:
            return Response({'message': True})

