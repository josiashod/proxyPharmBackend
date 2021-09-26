import time
from datetime import datetime, timedelta, timezone

from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from xlib.utils import mailer, send_message

from .models import *
from .serializers import *

# Create your views here.

@api_view(['POST'])
def login(request):
    l_serializer = LoginSerializer(data= request.data)
    l_serializer.is_valid(raise_exception= True)

    user = l_serializer.validated_data['user']
    refresh = RefreshToken.for_user(user)

    return Response({
        'type': 'Bearer',
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh),
        'access_token_expire_in': time.mktime((datetime.utcnow() + getattr(settings, 'SIMPLE_JWT').get('ACCESS_TOKEN_LIFETIME')).timetuple()),
        'refresh_token_expire_in': time.mktime((datetime.utcnow() + getattr(settings, 'SIMPLE_JWT').get('REFRESH_TOKEN_LIFETIME')).timetuple()),
    })

@api_view(['POST'])
def google_login(request):
    serializer = GoogleSocialAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data['auth_token']

    return Response(data)

@api_view(['POST'])
def facebook_login(request):
    serializer = FacebookSocialAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.data['auth_token']

    return Response(data)

@api_view(['POST'])
def register(request):
    r = RegisterSerializer(data= request.data)

    r.is_valid(raise_exception= True)

    person, user = r.create(r.data)

    dt = datetime.now(timezone.utc)
    dt = dt.replace(tzinfo= timezone.utc)

    t, _ = Token.objects.get_or_create(user= user)
    t.digest = t.generate_digest()
    t.expire_at = dt + timedelta(minutes= 5)
    t.save()

    # if person.email:
    #     mailer(
    #         'emails/token.html',
    #         t,
    #         "Bienvenu sr proxyPhram",
    #         person.email,
    #     )

    # elif person.phone:
    #     send_message(person.phone, "test")

    return Response({
        "token": str(t.digest) + " expires in 5 minutes",
        "message": "You have been successfully registered. Please check your email.",
    }, status=201)

@api_view(['POST'])
def set_user_active(request):
    t = TokenSerializer(data= request.data)

    t.is_valid(raise_exception= True)
    t.save()

    # if person.email:
    #     mailer(
    #         'emails/verify_email.html',
    #         t,
    #         "Bienvenu sr proxyPhram",
    #         person.email,
    #     )

    # elif person.phone:
    #     send_message(person.phone, "test")

    return Response({"token": "fais"})

@api_view(['POST'])
def send_token(request):
    if not request.data['username']:
        return Response({
            "username": [
                "The username field is required"
            ]
        }, status= 400)
    
    person = Person.objects.filter(Q(email= request.data['username']) | Q(phone= request.data['username']))

    if not person.exists():
        return Response({
            "username": [
                "The username does not exist"
            ]
        }, status= 400)
        
    person = person.first()

    dt = datetime.now(timezone.utc)
    dt = dt.replace(tzinfo= timezone.utc)

    t, _ = Token.objects.get_or_create(user= User.objects.get(person= person))
    # t = t.first()
    t.digest = t.generate_digest()
    t.expire_at = dt + timedelta(minutes= 5)
    t.save()

    # if person.email:
    #     mailer(
    #         'emails/token.html',
    #         t,
    #         "Bienvenu sr proxyPhram",
    #         person.email,
    #     )

    # elif person.phone:
    #     send_message(person.phone, "test")

    return Response({
        "token": str(t.digest) + " expires in 5 minutes",
        "message": "Please check your email.",
    })

@api_view(['POST'])
def set_password(request):
    password_serializer = ChangePasswordSerializer(data= request.data)
    password_serializer.is_valid(raise_exception= True)
    password_serializer.save()

    return Response({"token": "fais"})

@api_view(['POST'])
def check_user(request):
    u = CheckUserSerializer(data= request.data)
    u.is_valid(raise_exception= True)
    # u.is_valid()
    return Response(u.validated_data)
