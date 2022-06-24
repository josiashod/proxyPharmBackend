from django.db.models.query_utils import Q
from rest_framework import serializers
from rest_framework import validators
from rest_framework.validators import UniqueValidator

from xlib.utils import distance as get_distance
from .models import *
from django.conf import settings
import datetime

class LocateSerializer(serializers.Serializer):
    lat = serializers.FloatField()
    lng = serializers.FloatField()

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
    distance = serializers.SerializerMethodField('set_distance')

    on_call = serializers.SerializerMethodField('set_on_call')

    def set_distance(self, pharmacy):
        try:
            if hasattr(pharmacy, 'distance'):
                return float(pharmacy.distance)

            coord = self.context.get('coord')
            return get_distance(coord.get('lat'), coord.get('lng'), pharmacy.latitude, pharmacy.longitude)
        except:
            return None

    def set_on_call(self, pharmacy):
        now = datetime.datetime.now(datetime.timezone.utc)
        on_call_pharmacy = OnCallPharmacy.objects.filter(pharmacy= pharmacy).filter(Q(end_at__gte= now) & Q(start_at__lte= now))
        if on_call_pharmacy.exists():
            on_call_pharmacy = on_call_pharmacy.first()
            return {
                'start_at': on_call_pharmacy.start_at,
                'end_at': on_call_pharmacy.end_at
            }
        else:
            return None

    created_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT,required= False)
    updated_at = serializers.DateTimeField(format=settings.DATETIME_FORMAT,required= False)
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
            'distance',
            'on_call',
            'created_at',
            'updated_at',
            # 'deleted',
        ]

class SearchDrugByPharmacySerializer(serializers.Serializer):
    q = serializers.CharField(required= True)
    pharmacy_id = serializers.IntegerField(required= True)

    def validate_pharmacy_id(self, value):
        if not Pharmacy.objects.filter(id= value).exists():
            raise serializers.ValidationError("Pharmacy not found")
        return value

class DrugListSerializer(serializers.ListSerializer):
    def validate(self, attrs):
        if not Drug.objects.filter(id= attrs.get('id')).exists():
            raise serializers.ValidationError("Drug not exists")
        return super().validate(attrs)

class DrugSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only= True)
    name = serializers.CharField(max_length= 255)
    dose = serializers.CharField(max_length= 255, required= False)
    type = serializers.CharField(max_length= 255, required= False)
    chemical_composition = serializers.CharField(max_length= 255, read_only= True, required= False)
    class_of_drug = serializers.CharField(max_length= 255, read_only= True, required= False)
    quantity = serializers.SerializerMethodField('get_quantity')

    def get_quantity(self, drug):
        return drug.pharmacydrug_set.get(pharmacy__id= self.context.get('pharmacy')).quantity if self.context.get('pharmacy') else None

    class Meta:
        model = Drug
        list_serializer_class = DrugListSerializer
        fields = [
            'id',
            'name',
            'dose',
            'type',
            'chemical_composition',
            'class_of_drug',
            'quantity',
        ]
class PharmacyDetailSerializer(serializers.ModelSerializer):
    drugs = DrugSerializer(many= True, required= False)
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
            # 'distance',
            # 'on_call',
            'created_at',
            'updated_at',
            'drugs',
            # 'deleted',
        ]

class FindPharmaciesByDrugsSerializer(serializers.Serializer):
    drugs = serializers.ListField(child= DrugSerializer(), required= True)
