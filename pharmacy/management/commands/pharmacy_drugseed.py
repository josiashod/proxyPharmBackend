import random
from datetime import datetime, timedelta, timezone

from django.core.management.base import BaseCommand, CommandError
from pharmacy.models import Drug, Pharmacy, PharmacyDrug

class Command(BaseCommand):
    help = """This command feed the oncallpharmacy
    example: command path
    """ 

    def handle(self, *args, **options):
        for pharmacy in Pharmacy.objects.all():
            drugs = random.sample(list(Drug.objects.all()), 15)
            for drug in drugs:
                PharmacyDrug.objects.create(
                    pharmacy= pharmacy,
                    drug= drug,
                    quantity= random.randrange(10,20)
                )

            self.stdout.write(self.style.SUCCESS('The pharmacy "%s" has been feeded in drug' % pharmacy.name))

