from django.core.management.base import BaseCommand, CommandError
from quest.models import *
from recruiter.models import *
import csv
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    BASEDIR = '/Users/fulvio/Desktop/virtual2/vr/csv/'
    def handle(self,*args,**kwargs):

        with open(self.BASEDIR+'Candidato.csv') as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            counter = 0

            for row in csv_reader:
                self.stdout.write(f'Elemento {row[0]} letto')
                if counter ==0:
                    counter += 1
                    continue
                try:
                    importazione = Candidato(user=row[0])
                    importazione.save()
                    self.stdout.write(f'Elemento {importazione.id} inserito')
                except IntegrityError:
                    self.stderr.write(f'Elemento già presente')
