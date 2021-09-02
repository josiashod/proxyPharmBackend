import re
from datetime import datetime, timezone

from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import *


class LoginSerializer(serializers.Serializer):
    """
    Serializer for login
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        """
        Validate login
        """
        username = attrs.get('username')
        password = attrs.get('password')

        if not username or not password:
            raise serializers.ValidationError('Username and password are required', code="Unauthorized")

        person = Person.objects.filter(Q(email= username) | Q(phone= username))
        user = User.objects.filter(username = username)

        if not person.exists() and not user.exists():
            raise serializers.ValidationError('This username does not exist', code="Unauthorized")
        
        if person.exists():
            person = person.first()
            username = User.objects.get(person= person).username
        elif user.exists():
            user = user.first()
            username = user.username

        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError('Invalid username or password', code="Unauthorized")

        attrs['user'] = user
        return super().validate(attrs)

class RegisterSerializer(serializers.Serializer):
    """
    Serializer for register
    """

    email = serializers.EmailField(
        required= False,
        validators=[UniqueValidator(queryset=Person.objects.all())],
    )

    phone = serializers.CharField(
        max_length=15,
        required= False,
        validators=[UniqueValidator(queryset=Person.objects.all())],
    )

    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)
    is_pharmacist = serializers.BooleanField(default=False, required= False)

    def validate_password(self, value):
        if re.findall(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", value):
            return value
        else:
            raise serializers.ValidationError('Password must contain at least one lowercase, one uppercase, one number and one special character.', code="badRequest")

    def validate(self, attrs):
        if not attrs.get('email') and not attrs.get('phone'):
            raise serializers.ValidationError('Either email or phone number is required.', code="badRequest")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop('password')

        if validated_data.get('email'):
            username = validated_data.get('email')
        elif validated_data.get('phone'):
            username = validated_data.get('phone')
        else:
            raise serializers.ValidationError('Either email or phone number is required.', code="badRequest")
        
        person = Person.objects.create(**validated_data)
        
        user = User(
            username= username,
            person= person,
            is_active= False,
        )
        user.set_password(password)
        user.save()
        
        return person, user

class TokenSerializer(serializers.ModelSerializer):
    """
    Serializer for token
    """

    class Meta:
        model = Token
        fields = ['digest']

    def validate_digest(self, value):
        token = Token.objects.filter(digest= value)

        if not token.exists():
            raise serializers.ValidationError('Invalid digest', code='InvalidDigest')
        
        token = token.first()

        if not token.expire_at >= datetime.now(tz= timezone.utc):
            raise serializers.ValidationError('Expired digest', code='ExpiredDigest')
        return value

    def save(self):
        token = Token.objects.get(digest= self.validated_data['digest'])

        token.digest = None
        token.confirmed_at = datetime.now(tz= timezone.utc)
        token.expire_at = None
        token.user.is_active = True
        token.user.save()
        token.save()
        return token

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(required=True)
    digest = serializers.CharField(required=True)

    def validate_digest(self, value):
        token = Token.objects.filter(digest= value)

        if not token.exists():
            raise serializers.ValidationError('Invalid digest', code='InvalidDigest')
        
        token = token.first()

        if not token.expire_at >= datetime.now(tz= timezone.utc):
            raise serializers.ValidationError('Expired digest', code='ExpiredDigest')
        return value

    def validate_password(self, value):
        if re.findall(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$", value):
            return value
        else:
            raise serializers.ValidationError('Password must contain at least one lowercase, one uppercase, one number and one special character.', code="badRequest")

    def save(self):
        token = Token.objects.get(digest= self.validated_data['digest'])

        token.digest = None
        token.expire_at = None
        token.user.set_password(self.validated_data['password'])
        token.user.save()

        return token

class CheckUserSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    first_name = serializers.CharField(required= False, read_only= True)
    last_name = serializers.CharField(required= False, read_only= True)
    email = serializers.EmailField(required= False, read_only= True)
    phone = serializers.CharField(required= False, read_only= True)
    is_user = serializers.BooleanField(required= False, read_only= True)
    is_pharmacist = serializers.BooleanField(required= False, read_only= True)

    def validate_username(self, value):
        person = Person.objects.filter(Q(email= value) | Q(phone= value))
        user = User.objects.filter(username = value)

        if not person.exists() and not user.exists():
            raise serializers.ValidationError('This username does not exist', code="Unauthorized")
        
        if person.exists():
            person = person.first()
            user = User.objects.get(person= person)
        elif user.exists():
            user = user.first()
            
        self.username = user.username
        self.first_name = user.person.first_name
        self.last_name = user.person.last_name
        self.phone = user.person.phone
        self.is_user = user.person.is_user
        self.is_pharmacist = user.person.is_pharmacist

        return user.username

    def validate(self, attrs):
        user = User.objects.get(username = attrs.get('username'))
            
        attrs['username'] = user.username
        attrs['first_name'] = user.person.first_name
        attrs['last_name'] = user.person.last_name
        attrs['phone'] = user.person.phone
        attrs['is_user'] = user.person.is_user
        attrs['is_pharmacist'] = user.person.is_pharmacist
        
        return super().validate(attrs)
