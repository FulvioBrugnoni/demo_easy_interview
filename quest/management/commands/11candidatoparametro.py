from django.core.management.base import BaseCommand, CommandError
from quest.models import *
from recruiter.models import *
import csv
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    BASEDIR = '/Users/fulvio/Desktop/virtual11/vr/csv/'
    def handle(self,*args,**kwargs):

        with open(self.BASEDIR+'candidatoazienda.csv') as csv_file:
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
                    parametro = AziendaLingua.objects.get(id =row[1])
                except ObjectDoesNotExist:
                    self.stderr.write(f'Elemento {row[0]} non presente nel db')
                    continue
                try:
                    importazione = CandidatoParametro(candidato=candidato, parametro = parametro)
                    importazione.save()
                    self.stdout.write(f'Elemento {importazione.id} inserito')
                except IntegrityError:
                    self.stderr.write(f'Elemento già presente')
