from django.core.management.base import BaseCommand, CommandError
from quest.models import *
from recruiter.models import *
import csv
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    BASEDIR = '/Users/fulvio/Desktop/virtual/vr/csv/'
    def handle(self,*args,**kwargs):

        with open(self.BASEDIR+'.csv') as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            counter = 0

            for row in csv_reader:
                self.stdout.write(f'Elemento {row[0]} letto')
                if counter ==0:
                    counter += 1
                    continue
                try:
                    questionario = Questionario.objects.get(id =row[0])
                except ObjectDoesNotExist:
                    self.stderr.write(f'Elemento {row[0]} non presente nel db')
                    continue
                try:
                    domanda = Domanda.objects.get(id =row[1])
                except ObjectDoesNotExist:
                    self.stderr.write(f'Elemento {row[1]} non presente nel db')
                    continue
                try:
                    importazione = QuestionarioDomanda(questionario=questionario,domanda=domanda,posizione=row[2])
                    importazione.save()
                    self.stdout.write(f'Elemento {importazione.id} inserito')
                except IntegrityError:
                    self.stderr.write(f'Elemento già presente')
