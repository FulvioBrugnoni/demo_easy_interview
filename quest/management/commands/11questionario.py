from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from quest.models import Questionario
import csv
from django.db.utils import IntegrityError

class Command(BaseCommand):
    BASEDIR = settings.BASE_DIR / 'csv'
    def handle(self,*args,**kwargs):

        with open(self.BASEDIR / 'Questionario.csv') as csv_file:
            csv_reader = csv.reader(csv_file,delimiter=',')
            counter = 0
            for row in csv_reader:
                self.stdout.write(f'Elemento {row[0]} letto')
                if counter ==0:
                    counter += 1
                    continue
                try:
                    questionario = Questionario(name=row[0])
                    questionario.save()
                    self.stdout.write(f'Elemento {row[0]} inserito')
                except IntegrityError:
                    # raise CommandError('Nome Ripetuto:'+row[0])
                    self.stderr.write(f'Elemento {row[0]} non inserito')
                    # pass
