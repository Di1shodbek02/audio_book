import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.cache import cache
from django.db.models import Q
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from passlib.context import CryptContext
from rest_framework import status
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsAdminPermission
from .serializers import PasswordResetSerializer, PasswordResetRequestSerializer, UpdateDestroyAccountSerializer, \
    RegisterSerializer, ConfirmCodeSerializer, UserListSerializer
from .tasks import send_email, send_forget_password

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
            reset_link = f"http://10.10.3.132:8000/accounts/reset-password/{uid}/{token}/"
            send_forget_password.delay(email, reset_link)
            return Response({'success': 'Password reset link sent'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(GenericAPIView):
    serializer_class = PasswordResetSerializer

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
        try:
            serializer = self.get_serializer(data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            return Response({'success': False, 'message': str(e)}, status=400)
        return Response({'success': True})


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.data.get('refresh')
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(status=204)
