from django.db import models

from pharmacy.models import Pharmacy

# Create your models here.
class OnCallPharmacy(models.Model):
    
    pharmacy = models.ForeignKey(to= Pharmacy, on_delete= models.DO_NOTHING)
    start_at = models.DateField()
    end_at = models.DateField()
    start_hour = models.TimeField()
    end_hour = models.TimeField()
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(default= None, null= True)