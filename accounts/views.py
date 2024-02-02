import os
import random
import requests
from django.core.cache import cache
from django.shortcuts import redirect
from django.core.mail import send_mail
from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView

from allauth.socialaccount.models import SocialApp
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dotenv import load_dotenv

from .serializers import RegisterSerializer, ConfirmCodeSerializer

load_dotenv()
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


class RedirectToGoogleApiView(APIView):
    def get(self, request):
        google_redirect_uri = os.getenv('GOOGLE_REDIRECT_URL')
        try:
            google_client_id = SocialApp.objects.get(provider='google').client_id
        except SocialApp.DoesNotExist:
            return Response({'success': False, 'message': 'SocialApp does not exist'}, status=404)
        url = f'https://accounts.google.com/o/oauth2/v2/auth?redirect_uri={google_redirect_uri}&prompt=consent&response_type=code&client_id={google_client_id}&scope=openid email profile&access_type=offline'

        return redirect(url)


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = "https://c744-178-218-201-17.ngrok-free.app/accounts/google/callback"
    client_class = OAuth2Client


@api_view(['GET'])
def callback(request):
    """Callback"""
    code = request.GET.get('code')
    res = requests.post("https://c744-178-218-201-17.ngrok-free.app/accounts/google", data={'code': code}, timeout=30)
    return Response(res.json())
