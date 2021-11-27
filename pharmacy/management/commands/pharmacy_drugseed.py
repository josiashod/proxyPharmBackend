import random
from datetime import datetime, timedelta, timezone

from django.core.management.base import BaseCommand, CommandError
from pharmacy.models import OnCallPharmacy, Pharmacy

class Command(BaseCommand):
    help = """This command feed the oncallpharmacy
    example: command path
    """ 

    def handle(self, *args, **options):
        pharmacies = list(Pharmacy.objects.all())
        random_pharmacies = random.sample(pharmacies, (len(pharmacies) // 10))
        dt = datetime.now(timezone.utc)
        dt = dt.replace(tzinfo= timezone.utc)
        end_at = dt + timedelta(weeks= 2)
        for pharmacy in random_pharmacies:
            OnCallPharmacy.objects.create(
                pharmacy= pharmacy,
                start_at= dt,
                end_at= dt
            )

            self.stdout.write(self.style.SUCCESS('The pharmacy "%s" has been registered' % pharmacy.name))

