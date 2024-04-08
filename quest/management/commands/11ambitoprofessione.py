from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from quest.models import *
import csv
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    BASEDIR = settings.BASE_DIR / 'csv'
    def handle(self,*args,**kwargs):

        with open(self.BASEDIR /'IndustriaAmbito.csv') as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=';')
            counter = 0

            for row in csv_reader:
                if counter ==0:
                    counter += 1
                    continue
                try:
                    lingua = Lingua.objects.get(id=row[0])
                    importazione2 = Settore(lingua=lingua ,name=row[1])
                    importazione2.save()
                    self.stdout.write(f'Settore {row[1]} salvato')
                except IntegrityError:
                    pass
                try:
                    lingua = Lingua.objects.get(id=row[0])
                    settore = Settore.objects.get(name=row[1])
                    importazione3 = Professione(lingua=lingua ,settore=settore,name=row[2] )
                    importazione3.save()
                    self.stdout.write(f'Professione {row[1]} salvato')
                except IntegrityError:
                    pass
