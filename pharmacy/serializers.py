from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
from django.conf import settings

class PharmacySerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only= True)
    name = serializers.CharField(
        required= True,
        validators=[UniqueValidator(queryset=Pharmacy.objects.all())]
    )
    image = serializers.CharField(required= False)
    thumbnail_image = serializers.CharField(required= False)
    phone = serializers.CharField(required= False)
    email = serializers.EmailField(required= False)
    website = serializers.URLField(required= False)
    longitude = serializers.FloatField(
        required= True,
        validators=[UniqueValidator(
            queryset=Pharmacy.objects.all(),
            message="This pharmacy is already registered"
        )]
    )
    latitude = serializers.FloatField(
        required= True,
        validators=[UniqueValidator(
            queryset=Pharmacy.objects.all(),
            message="This pharmacy is already registered"
        )]
    )

    # created_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT,required= False)
    # updated_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT,required= False)
    # deleted = serializers.DateTimeField(format=settings.DATETIME_FORMAT, required= False)

    class Meta:
        model = Pharmacy
        fields = [
            'id',
            'name',
            'image',
            'thumbnail_image',
            'phone',
            'email',
            'website',
            'longitude',
            'latitude',
            # 'created_at',
            # 'updated_at',
            # 'deleted',
        ]
