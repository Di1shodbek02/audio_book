from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import PasswordResetView, PasswordResetRequestView, \
    UserLict, UserUpdateGenericAPIView, LogoutAPIView
from .views import (RegistrationAPIView, ConfirmCodeApiView, GoogleLogin, callback_google, RedirectToGoogleAPIView,
                    FacebookLogin, RedirectToFacebookApiView, callback_facebook)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationAPIView.as_view(), name='registration-api'),
    path('confirm-code', ConfirmCodeApiView.as_view(), name='confirm-code'),
    path('forget-password/', PasswordResetRequestView.as_view(), name='forget_password'),
    path('reset-password/<str:uid>/<str:token>/', PasswordResetView.as_view(), name='reset_password'),
    path('update-user/', UserUpdateGenericAPIView.as_view(), name='user-update'),
    path('user-list', UserLict.as_view(), name='user-list'),
    path('log-out', LogoutAPIView.as_view(), name='log_out'),
    # Google
    path('google', GoogleLogin.as_view(), name='google_login'),
    path('google-login', RedirectToGoogleAPIView.as_view(), name='google_login2'),
    path('google/callback', callback_google, name='google_callback'),
    # Facebook
    path('facebook', FacebookLogin.as_view(), name='facebook'),
    path('facebook-login', RedirectToFacebookApiView.as_view(), name='facebook-login'),
    path('facebook/callback', callback_facebook, name='facebook_callback')
]
