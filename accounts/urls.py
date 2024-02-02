from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegistrationAPIView, ConfirmCodeApiView, GoogleLogin, callback, RedirectToGoogleApiView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationAPIView.as_view(), name='registration-api'),
    path('confirm-code', ConfirmCodeApiView.as_view(), name='confirm-code'),

    path('google', GoogleLogin.as_view(), name='google_login'),
    path('google-login', RedirectToGoogleApiView.as_view(), name='google_login2'),
    path('google/callback', callback, name='google_callback'),
]
# https://accounts.google.com/o/oauth2/v2/auth?redirect_uri=http://localhost:8000/accounts/google/callback&prompt=consent&response_type=token&client_id=41419922659-o40vgdpk5jd87q93ll4r26b3jk9pcnnb.apps.googleusercontent.com&scope=openid%20email%20profile
