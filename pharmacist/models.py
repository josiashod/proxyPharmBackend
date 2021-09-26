from django.db import models

from authentication.models import AbstractClass, Person
from pharmacy.models import Pharmacy

# Create your models here.
class Pharmacist(models.Model, AbstractClass):
    
    poste = models.CharField(max_length= 255)
    pharmacy = models.ForeignKey(to= Pharmacy, on_delete= models.DO_NOTHING)
    person = models.OneToOneField(to= Person, null= True, blank= True, on_delete= models.DO_NOTHING)

