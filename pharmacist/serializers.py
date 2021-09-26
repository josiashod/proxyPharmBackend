from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *
from pharmacy.serializers import PharmacySerializer

class PharmacistSerializer(serializers.ModelSerializer):

    id = serializers.IntegerField(read_only= True)
    poste = serializers.CharField(max_length= 100, required= True)
    pharmacy = PharmacistSerializer()
    
    class Meta:
        model = Pharmacist
        fields = [
            'id',
            'poste',
            'pharmacy',
        ]
