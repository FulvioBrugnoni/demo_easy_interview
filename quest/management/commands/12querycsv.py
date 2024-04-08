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

        print('ciao')
        utenti = MyUser.objects.all()
        with open ("/tmp/utenti.csv", "w") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for c in utenti:
                writer.writerow([c.id,c.email])
