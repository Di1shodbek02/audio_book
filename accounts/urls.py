from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (RegistrationAPIView, ConfirmCodeApiView, GoogleLogin, callback, RedirectToGoogleApiView,
                    FacebookLogin, RedirectToFacebookApiView, callback_facebook)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationAPIView.as_view(), name='registration-api'),
    path('confirm-code', ConfirmCodeApiView.as_view(), name='confirm-code'),
    # Google
    path('google', GoogleLogin.as_view(), name='google_login'),
    path('google-login', RedirectToGoogleApiView.as_view(), name='google_login2'),
    path('google/callback', callback, name='google_callback'),
    # Facebook
    path('facebook', FacebookLogin.as_view(), name='facebook'),
    path('facebook-login', RedirectToFacebookApiView.as_view(), name='facebook-login'),
    path('facebook/callback', callback_facebook, name='facebook_callback')
]
