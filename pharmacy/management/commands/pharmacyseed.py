from django.core.management.base import BaseCommand, CommandError
from pharmacy.models import Pharmacy
import json

image_url = "https://awss3bucket-aladecouvertedubenin.s3.eu-central-1.amazonaws.com/1622718034622-pharmacie.jpg"
thumbnail_image_url = "https://awss3bucket-aladecouvertedubenin.s3.eu-central-1.amazonaws.com/1622718035947-thumbnail_pharmacie.jpg"

class Command(BaseCommand):
    help = """This command feed the pharmacy
    example: command path
    """

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        f = open(options['file'])
        pharmacies = json.load(f)
        for pharmacy in pharmacies:
            phone = pharmacy['tel'] if 'tel' in pharmacy.keys() else None
            try:
                if 'pharmacie' in pharmacy['name'].lower():
                    Pharmacy.objects.create(
                        name= pharmacy['name'].capitalize(),
                        image= image_url,
                        thumbnail_image= thumbnail_image_url,
                        phone= phone,
                        website= "",
                        longitude = pharmacy['longitude'],
                        latitude = pharmacy['latitude']
                    )
                    self.stdout.write(self.style.SUCCESS('Successfully created pharmacy "%s"' % pharmacy['name']))
            except:
                self.stdout.write(self.style.WARNING('The pharmacy "%s" already exist' % pharmacy['name']))
                pass
        
        f.close()