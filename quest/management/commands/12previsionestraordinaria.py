from django.core.management.base import BaseCommand, CommandError
from quest.models import *
from recruiter.models import *
import csv
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    BASEDIR = '/Users/fulvio/Desktop/virtual/vr/csv/'
    def handle(self,*args,**kwargs):

        with open(self.BASEDIR+'previsionestraordinaria.csv') as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            counter = 0

            for row in csv_reader:
                self.stdout.write(f'Elemento {row[0]} letto')
                if counter ==0:
                    counter += 1
                    continue
                try:
                    candidato = Candidato.objects.get(id =row[0])
                except ObjectDoesNotExist:
                    self.stderr.write(f'Elemento {row[0]} non presente nel db')
                    continue
                try:
                    algoritmo = Algoritmo.objects.get(id =row[1])
                except ObjectDoesNotExist:
                    self.stderr.write(f'Elemento {row[1]} non presente nel db')
                    continue
                try:
                    importazione = PrevisioneStraordinaria(candidato=candidato, algoritmo=algoritmo, previsione=row[2], esito=row[3])
                    importazione.save()
                    self.stdout.write(f'Elemento {importazione.id} inserito')
                except IntegrityError:
                    self.stderr.write(f'Elemento già presente')
