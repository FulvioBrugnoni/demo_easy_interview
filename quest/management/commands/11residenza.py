from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from quest.models import *
import csv
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

class Command(BaseCommand):
    BASEDIR = settings.BASE_DIR / 'csv'
    def handle(self,*args,**kwargs):

        with open(self.BASEDIR /'residenza.csv') as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=';')
            counter = 0
            y = 0
            for row in csv_reader:
                if counter ==0:
                    counter += 1
                    continue
                try:
                    importazione = Amm1(name=row[4])
                    importazione.save()
                except IntegrityError:
                    pass
                try:
                    amm1 = Amm1.objects.get(name=row[4])
                    importazione2 = Amm2(amm1=amm1 ,name=row[1])
                    importazione2.save()
                except IntegrityError:
                    pass
                try:
                    amm2 = Amm2.objects.get(name=row[1])
                    importazione3 = Amm3(amm2=amm2 ,name=row[2])
                    importazione3.save()
                except IntegrityError:
                    pass
                try:
                    amm3 = Amm3.objects.get(name=row[2])
                    importazione4 = Amm4(amm3=amm3 ,name=row[3])
                    importazione4.save()
                except IntegrityError:
                    pass

                y+=1
                if y % 1000 == 0:
                    print(y)
