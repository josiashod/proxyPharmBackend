from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
from pharmacy.serializers import PharmacySerializer

class OnCallPharmacySerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only= True)
    start_at = serializers.DateField(required= True)
    end_at = serializers.DateField(required= True)
    start_hour = serializers.TimeField(required= True)
    end_hour = serializers.TimeField(required= True)
    pharmacy = PharmacySerializer()

    class Meta:
        model = OnCallPharmacy
        fields = [
            'id',
            'start_at',
            'end_at',
            'start_hour',
            'end_hour',
            'pharmacy',
        ]