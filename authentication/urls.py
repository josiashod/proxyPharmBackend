from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *

urlpatterns = [
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('check_user/', check_user, name="check_user"),
    path('confirmation/', set_user_active, name="confirmation"),
    path('change_password/', set_password, name="change_password"),
    path('token/password/', send_token, name='token_change_password'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]