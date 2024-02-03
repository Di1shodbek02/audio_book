from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import PasswordResetView, PasswordResetRequestView, \
    UserLict, UserUpdateGenericAPIView, LogoutAPIView
from .views import RegistrationAPIView, ConfirmCodeApiView, GoogleLogin, callback, RedirectToGoogleApiView

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
    path('google', GoogleLogin.as_view(), name='google_login'),
    path('google-login', RedirectToGoogleApiView.as_view(), name='google_login2'),
    path('google/callback', callback, name='google_callback'),
]
