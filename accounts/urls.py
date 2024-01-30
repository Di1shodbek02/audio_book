from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegistrationAPIView, ConfirmCodeApiView, PasswordResetView, PasswordResetRequestView, \
    UserUpdateGenericAPIView, UserDeleteGenericAPIView, UserLict

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationAPIView.as_view(), name='registration-api'),
    path('confirm-code', ConfirmCodeApiView.as_view(), name='confirm-code'),
    path('forget-password/', PasswordResetRequestView.as_view(), name='forget_password'),
    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
    path('update-user/<int:pk>', UserUpdateGenericAPIView.as_view(), name='user-update'),
    path('delete-user/<int:pk>', UserDeleteGenericAPIView.as_view(), name='user-delete'),
    path('user-list', UserLict.as_view(), name='user-list'),
]
