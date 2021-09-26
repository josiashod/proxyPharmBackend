from django.db import models

from authentication.models import AbstractClass

# Create your models here.
class Pharmacy(models.Model, AbstractClass):

    name = models.CharField(max_length= 255, unique= True)
    image = models.FilePathField(path="")
    thumbnail_image = models.FilePathField(path="", default="")
    phone = models.CharField(max_length= 255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    website = models.URLField(max_length= 255)
    longitude = models.FloatField(unique= True)
    latitude = models.FloatField(unique= True)
