from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('login/', login, name="login"),
    path('login/google/', google_login, name="google_login"),
    path('login/facebook/', facebook_login, name="facebook_login"),
    path('register/', register, name="register"),
    path('check_user/', check_user, name="check_user"),
    path('confirmation/', set_user_active, name="confirmation"),
    path('change_password/', set_password, name="change_password"),
    path('token/send/', send_token, name='send_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]