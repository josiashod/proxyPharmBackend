from os import name
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
from .settings.views import *

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

    # settings
    path('settings/change_info/', change_info, name="settings.info"),
    path('settings/change_username/', change_username, name="settings.username"),
    path('settings/change_email/', change_email, name="settings.email"),
    path('settings/change_phone/', change_phone, name="settings.phone"),
    path('settings/change_password/', change_password, name="settings.password"),
    path('settings/change_profilepic/', ProfileImage.as_view(), name="settings.profile_picture"),
]