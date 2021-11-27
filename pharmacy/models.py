from django.db import models


# Create your models here.
class Pharmacy(models.Model):

    name = models.CharField(max_length= 255, unique= True)
    image = models.FileField(default=None)
    thumbnail_image = models.FileField(default=None)
    phone = models.CharField(max_length= 255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    website = models.URLField(max_length= 255)
    longitude = models.FloatField(unique= True)
    latitude = models.FloatField(unique= True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(default= None, null= True)

class OnCallPharmacy(models.Model):
    
    pharmacy = models.ForeignKey(to= Pharmacy, on_delete= models.DO_NOTHING)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(default= None, null= True)

class Drug(models.Model):

    name = models.CharField(max_length= 255, unique= True)
    dose = models.CharField(max_length= 255, null=True, blank=True)
    type = models.CharField(max_length= 255, null=True, blank=True)
    chemical_composition = models.CharField(max_length= 255, null=True, blank=True)
    class_of_drug = models.CharField(max_length= 255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(default= None, null= True)

class PharmacyDrug(models.Model):
    
    pharmacy = models.ForeignKey(to= Pharmacy, on_delete= models.DO_NOTHING)
    drug = models.ForeignKey(to= Drug, on_delete= models.DO_NOTHING)
    quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(default= None, null= True)