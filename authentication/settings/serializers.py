import re
from datetime import datetime, timedelta, timezone
from django.contrib.sites.models import Site
from django.conf import settings
from django.contrib.auth import authenticate
from django.core import mail
from django.db.models import Q
from rest_framework import serializers
from xlib.utils import mailer, send_message
from django.core.files.storage import default_storage
from ..models import *
from django.conf import settings
import os


class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    digest = serializers.CharField(required=True)


    def validate_password(self, value):
        if re.findall(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", value):
            return value
        else:
            raise serializers.ValidationError('Password must contain at least one lowercase, one uppercase, one number and one special character.', code="badRequest")


class UserInfoSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)

    def save(self, **kwargs):
        dt = datetime.now(timezone.utc)
        dt = dt.replace(tzinfo= timezone.utc)

        current_user = self.context['request'].user
        person = current_user.person

        first_name = self.validated_data.get('first_name')
        last_name = self.validated_data.get('last_name')
        person.first_name = first_name
        person.last_name = last_name
        
        person.updated_at = dt
        current_user.updated_at = dt

        current_user.save()
        person.save()


class ChangeEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required= True)

    def validate_email(self, value):
        current_user = self.context['request'].user
        p = Person.objects.filter(email= value)
        if p.exists():
            p = p.first()
            if p != current_user.person:
                raise serializers.ValidationError('This email is already used', code="AlreadyUsed")

        return value
       

    def save(self, **kwargs):

        dt = datetime.now(timezone.utc)
        dt = dt.replace(tzinfo= timezone.utc)

        current_user = self.context['request'].user
        person = current_user.person
        person.email = self.validated_data['email']
        current_user.is_active = False

        person.updated_at = dt
        current_user.updated_at = dt

        current_user.save()
        person.save()

        # creation of an comfirmation token
        t, _ = Token.objects.get_or_create(user= current_user)
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

class ChangeUsernameSerializer(serializers.Serializer):
    username = serializers.CharField(required= True)

    def validate_username(self, value):
        current_user = self.context['request'].user
        u = User.objects.filter(username= value)
        if u.exists():
            u = u.first()
            if u != current_user:
                raise serializers.ValidationError('This username is already used', code="AlreadyUsed")

        return value
       

    def save(self, **kwargs):

        dt = datetime.now(timezone.utc)
        dt = dt.replace(tzinfo= timezone.utc)

        current_user = self.context['request'].user
        person = current_user.person
        current_user.username = self.validated_data['username']
        current_user.is_active = False

        person.updated_at = dt
        current_user.updated_at = dt

        current_user.save()
        person.save()

        # creation of an comfirmation token
        t, _ = Token.objects.get_or_create(user= current_user)
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

class ChangePhoneSerializer(serializers.Serializer):
    phone = serializers.CharField(required= True)

    def validate_phone(self, value):
        current_user = self.context['request'].user
        p = Person.objects.filter(phone= value)
        if p.exists():
            p = p.first()
            if p != current_user.person:
                raise serializers.ValidationError('This phone is already used', code="AlreadyUsed")
                
        return value

    def save(self, **kwargs):
        dt = datetime.now(timezone.utc)
        dt = dt.replace(tzinfo= timezone.utc)

        current_user = self.context['request'].user
        person = current_user.person
        person.phone = self.validated_data['phone']
        current_user.is_active = False

        person.updated_at = dt
        current_user.updated_at = dt

        current_user.save()
        person.save()

        # creation of an comfirmation token
        t, _ = Token.objects.get_or_create(user= current_user)
        t.digest = t.generate_digest()
        t.expire_at = dt + timedelta(minutes= 5)
        t.save()

        # sending message
        # send_message(person.phone, f"Account: {t.token} est le code de vérification")

class UploadImageFileSerializer(serializers.Serializer):
    image = serializers.FileField(required= True)
    class Meta:
        fields = ['image']
    
    def save(self, **kwargs):
        path = settings.MEDIA_ROOT+ "images/users/"

        dt = datetime.now(timezone.utc)
        dt = dt.replace(tzinfo= timezone.utc)

        request = self.context['request']
        current_user = request.user
        person = current_user.person

        image = self.validated_data['image']
        _, extension = os.path.splitext(image.name)

        filename = str(current_user.pk) + extension

        try:
            open(path)
        except:
            os.mkdir(path)
            pass

        with default_storage.open(path + filename, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)

            destination.close()  # File should be closed only after all chunks are added

        person.image = "images/users/" + filename

        person.updated_at = dt
        current_user.updated_at = dt

        current_user.save()
        person.save()
