from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from quest.models import *
from recruiter.models import *
import csv
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    BASEDIR = settings.BASE_DIR / 'csv'
    def handle(self,*args,**kwargs):

        with open(self.BASEDIR /'Professione.csv') as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            counter = 0

            for row in csv_reader:
                self.stdout.write(f'Elemento {row[0]} letto')
                if counter ==0:
                    counter += 1
                    continue
                try:
                    lingua = Lingua.objects.get(id =row[1])
                except ObjectDoesNotExist:
                    self.stderr.write(f'Elemento {row[0]} non presente nel db')
                    continue
                try:
                    settore = Settore.objects.get(id =row[2])
                except ObjectDoesNotExist:
                    self.stderr.write(f'Elemento {row[1]} non presente nel db')
                    continue
                try:
                    importazione = Professione(settore=settore,lingua=lingua,name=row[0])
                    importazione.save()
                    self.stdout.write(f'Elemento {importazione.id} inserito')
                except IntegrityError:
                    self.stderr.write(f'Elemento già presente')
