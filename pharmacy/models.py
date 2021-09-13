from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE, SafeDeleteModel
from authentication.models import AbstractClass

# Create your models here.
class Pharmacy(SafeDeleteModel, AbstractClass):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(max_length= 255)
    image = models.FilePathField(path="")
    thumbnail_image = models.FilePathField(path="", default="")
    phone = models.CharField(max_length= 255, null=True, blank=True, unique=True)
    email = models.EmailField(null=True, blank=True, unique=True)
    website = models.URLField(max_length= 255)
    longitude = models.FloatField()
    latitude = models.FloatField()

class OnCallPharmacy(SafeDeleteModel, AbstractClass):
    pharmacy = models.ForeignKey(to= Pharmacy, on_delete= models.DO_NOTHING)
    start_at = models.DateField()
    end_at = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()


class Pharmacist(SafeDeleteModel, AbstractClass):
    poste = models.CharField(max_length= 255)
    pharmacy = models.ForeignKey(to= Pharmacy, on_delete= models.DO_NOTHING)
