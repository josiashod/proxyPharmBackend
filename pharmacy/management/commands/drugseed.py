from django.core.management.base import BaseCommand, CommandError
from pharmacy.models import Drug, Pharmacy
import json

class Command(BaseCommand):
    help = """This command feed the drug
    example: command path
    """

    def add_arguments(self, parser):
        parser.add_argument('file', type=str)

    def handle(self, *args, **options):
        f = open(options['file'])
        drugs = json.load(f)
        
        for drug in drugs:
            if Drug.objects.filter(name=drug['designation'].capitalize()).exists():
                self.stdout.write(self.style.WARNING('The drug "%s" already exist' % drug['designation']))
                pass
            else:
                Drug.objects.create(
                    name= drug['designation'].capitalize(),
                    dose= drug['dosage'],
                    type= drug['forme'],
                    chemical_composition= drug['nomFrancais'],
                    class_of_drug= drug['classeTherapeutique']
                )
                self.stdout.write(self.style.SUCCESS('The drug "%s" has been created' % drug['designation']))
        f.close()