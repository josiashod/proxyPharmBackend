from django.db import models

from authentication.models import AbstractClass
from pharmacy.models import Pharmacy

# Create your models here.
class OnCallPharmacy(models.Model, AbstractClass):
    
    pharmacy = models.ForeignKey(to= Pharmacy, on_delete= models.DO_NOTHING)
    start_at = models.DateField()
    end_at = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()
