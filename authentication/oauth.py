import random
import time
from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Person, User

def register_social_user(email, first_name, last_name, image):
    user = User.objects.filter(person__email= email)

    if user.exists():

        user = user.first()
        refresh = RefreshToken.for_user(user)
        # authenticate(
        #     email=email, password=getattr(settings, 'SOCIAL_SECRET'))

        return {
            'type': 'Bearer',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'access_token_expire_in': time.mktime((datetime.utcnow() + getattr(settings, 'SIMPLE_JWT').get('ACCESS_TOKEN_LIFETIME')).timetuple()),
            'refresh_token_expire_in': time.mktime((datetime.utcnow() + getattr(settings, 'SIMPLE_JWT').get('REFRESH_TOKEN_LIFETIME')).timetuple()),
        }

    else:

        data = {
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'image': image
        }
        person = Person.objects.create(**data)

        user = User.objects.create(username= person.email, person= person)
        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)

        # new_user = authenticate(
        #     email=email, password=getattr(settings, 'SOCIAL_SECRET'))

        return {
            'type': 'Bearer',
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'access_token_expire_in': time.mktime((datetime.utcnow() + getattr(settings, 'SIMPLE_JWT').get('ACCESS_TOKEN_LIFETIME')).timetuple()),
            'refresh_token_expire_in': time.mktime((datetime.utcnow() + getattr(settings, 'SIMPLE_JWT').get('REFRESH_TOKEN_LIFETIME')).timetuple()),
        }
