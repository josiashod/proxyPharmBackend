from django.db import models

from authentication.models import Person
from pharmacy.models import Pharmacy

# Create your models here.
class Pharmacist(models.Model):
    
    poste = models.CharField(max_length= 255)
    pharmacy = models.ForeignKey(to= Pharmacy, on_delete= models.DO_NOTHING)
    person = models.OneToOneField(to= Person, null= True, blank= True, on_delete= models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add= True)
    updated_at = models.DateTimeField(default= None, null= True)
