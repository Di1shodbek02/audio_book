import os
import random

import requests
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.shortcuts import redirect
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from dotenv import load_dotenv
from passlib.context import CryptContext
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdminPermission
from .serializers import PasswordResetLoginSerializer, PasswordResetRequestSerializer, UpdateDestroyAccountSerializer, \
    UserListSerializer
from .serializers import RegisterSerializer, ConfirmCodeSerializer
from .tasks import send_email, send_forget_password

load_dotenv()

User = get_user_model()

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class RegistrationAPIView(CreateAPIView):
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


class PasswordResetRequestView(GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = f"http://192.168.1.15:8000/accounts/reset-password/{uid}/{token}/"
            send_forget_password.delay(email, reset_link)
            return Response({'success': 'Password reset link sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetLoginSerializer

    def post(self, request, uid, token):

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_password = serializer.validated_data['new_password']

            try:
                uid = force_str(urlsafe_base64_decode(uid))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                user = None
            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'success': 'Password reset successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLict(ListAPIView):
    permission_classes = (IsAdminPermission,)
    queryset = User.objects.all()

    serializer_class = UserListSerializer


class UserUpdateGenericAPIView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateDestroyAccountSerializer

    def post(self, request):
        user_id = request.user.id
        user = User.objects.get(id=user_id)
        serializer = self.get_serializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=204)



class RedirectToFacebookApiView(APIView):
    def get(self, request):
        facebook_redirect_uri = os.getenv('FACEBOOK_REDIRECT_URI')
        facebook_app_id = os.getenv('FACEBOOK_APP_ID')
        try:
            url = f'https://www.facebook.com/v9.0/dialog/oauth?client_id={facebook_app_id}&redirect_uri={facebook_redirect_uri}&scope=email,public_profile'
        except SocialApp.DoesNotExist:
            return Response({'success': False, 'message': 'Social does not exist'}, status=404)
        return redirect(url)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
    callback_url = "https://eff4-178-218-201-17.ngrok-free.app/accounts/facebook/callback_facebook"
    client_class = OAuth2Client


@api_view(['GET'])
def callback_facebook(request):
    """Callback function to handle the Facebook OAuth2 callback."""
    code = request.query_params.get('code')
    if not code:
        return Response({'error': 'Code parameter is missing.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        response = requests.get("https://graph.facebook.com/v9.0/oauth/access_token", params={
            'client_id': os.getenv('FACEBOOK_APP_ID'),
            'redirect_uri': os.getenv('FACEBOOK_REDIRECT_URI'),
            'client_secret': os.getenv('FACEBOOK_APP_SECRET'),
            'code': code,
        })

        response.raise_for_status()
        data = response.json()
        access_token = data.get('access_token')

        if access_token:
            user_info_response = requests.get("https://graph.facebook.com/me", params={
                'fields': 'id,name,email',
                'access_token': access_token,
            })
            user_info_response.raise_for_status()
            user_info = user_info_response.json()

            return Response({'access_token': access_token, 'user_info': user_info}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Access token not found.'}, status=status.HTTP_400_BAD_REQUEST)
    except requests.exceptions.RequestException as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Google sign-in
class RedirectToGoogleAPIView(APIView):

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
    callback_url = "https://c704-178-218-201-17.ngrok-free.app/accounts/google/callback"
    client_class = OAuth2Client


@api_view(['GET'])
def callback(request):
    """Callback"""
    code = request.GET.get('code')
    res = requests.post("https://c704-178-218-201-17.ngrok-free.app/accounts/google", data={'code': code}, timeout=30)
    callback_url = 'https://eff4-178-218-201-17.ngrok-free.app/accounts/google/callback'
    client_class = OAuth2Client


@api_view(["GET"])
def callback_google(request):
    code = request.GET.get("code")
    res = requests.post("https://eff4-178-218-201-17.ngrok-free.app/accounts/google", data={"code": code}, timeout=30)
    return Response(res.json())

