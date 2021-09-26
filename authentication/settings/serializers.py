import re
from datetime import datetime, timedelta, timezone

from django.conf import settings
from django.contrib.auth import authenticate
from django.core import mail
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.validators import UniqueValidator
from xlib.utils import mailer, send_message

from ..models import *


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    digest = serializers.CharField(required=True)


    def validate_password(self, value):
        if re.findall(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", value):
            return value
        else:
            raise serializers.ValidationError('Password must contain at least one lowercase, one uppercase, one number and one special character.', code="badRequest")


class UserInfoSerializer(serializers.Serializer):
    current_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def save(self, **kwargs):
        person = self.validated_data.get('current_user').person
        first_name = self.validated_data.get('first_name')
        last_name = self.validated_data.get('last_name')
        person.first_name = first_name
        person.last_name = last_name
        person.save()


class ChangeEmailSerializer(serializers.Serializer):
    current_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    email = serializers.EmailField(required= True)

    def validate_email(self, value):
        current_user = self.validated_data.get('current_user')
        p = Person.objects.filter(email= value)
        if p.exists():
            p = p.first()
            if p != current_user.person:
                raise serializers.ValidationError('This email is already used', code="Unactivate")

        return value
       

    def save(self, **kwargs):
        current_user = self.validated_data.get('current_user')
        person = current_user.person
        person.email = self.validated_data['email']
        current_user.is_active = False
        current_user.save()

        # creation of an comfirmation token
        t, _ = Token.objects.get_or_create(user= current_user)
        dt = datetime.now(timezone.utc)
        dt = dt.replace(tzinfo= timezone.utc)
        t.digest = t.generate_digest()
        t.expire_at = dt + timedelta(minutes= 5)
        t.save()

        # sending email
        mailer(
            None,
            t,
            "Confirmer votre nouveau mail",
            person.email,
        )

        person.save()


class ChangePhoneSerializer(serializers.Serializer):
    current_user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    phone = serializers.CharField(required= True)

    def validate_phone(self, value):
        current_user = self.validated_data.get('current_user')
        p = Person.objects.filter(phone= value)
        if p.exists():
            p = p.first()
            if p != current_user.person:
                raise serializers.ValidationError('This phone is already used', code="Unactivate")
                
        return value

    def save(self, **kwargs):
        current_user = self.validated_data.get('current_user')
        person = current_user.person
        person.phone = self.validated_data['phone']
        current_user.is_active = False
        current_user.save()

        # creation of an comfirmation token
        t, _ = Token.objects.get_or_create(user= current_user)
        dt = datetime.now(timezone.utc)
        dt = dt.replace(tzinfo= timezone.utc)
        t.digest = t.generate_digest()
        t.expire_at = dt + timedelta(minutes= 5)
        t.save()

        # sending message
        send_message(person.phone, f"Account: {t.token} est le code de vérification")

        person.save()