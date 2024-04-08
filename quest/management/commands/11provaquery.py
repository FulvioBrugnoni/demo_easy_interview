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

#        risposta = Risposta.objects.get(id=3)
#        print(risposta.domanda.domanda)
        risposte = Risposta.objects.filter(utente_id = 5)
#        print(len(risposte))
#        for risposta in risposte:
#            print(risposta.domanda.domanda)
        ultima_risposta = risposte.last()
        print(ultima_risposta.domanda.domanda)
