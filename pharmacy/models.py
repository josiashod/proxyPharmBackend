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
