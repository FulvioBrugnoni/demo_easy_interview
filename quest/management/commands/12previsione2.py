from django.core.management.base import BaseCommand, CommandError
from quest.models import *
from recruiter.models import *
import csv
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date, timedelta
import random
import pytz

def hello():
    print('Hello')

class Command(BaseCommand):

    def handle(self,*args,**kwargs):

        today = datetime.now(pytz.utc)
        yesterday = today + timedelta(1)

        day_0 = datetime(year = yesterday.year, month=yesterday.month, day=yesterday.day, tzinfo=pytz.utc)
        day_1 = datetime(year = today.year, month=today.month, day=today.day, tzinfo=pytz.utc)
        azienda_esclusa = AziendaLingua.objects.get(azienda = 'A1')
        aziende = AziendaConsenso.objects.filter(consenso=1).exclude(azienda=azienda_esclusa).values_list('azienda', flat=True)
        candidati = CandidatoConsenso.objects.filter(consenso="YES").values_list('candidato', flat=True)
        print(candidati)
        print(aziende)
        candidati = CandidatoAzienda.objects.filter( giorno__range=[day_1, day_0],azienda__in = aziende, candidato__in = candidati )
        print(candidati)
        print(aziende)
        hello()


        for candidato in candidati:
            obj = candidato.candidato.id
            candidato = MyUser.objects.get(id =obj)
            previsione = round(random.uniform(0,1),2)
            if previsione > 0.25:
                esito = 1
            else:
                esito = 0
            importazione = Previsione(candidato= candidato, previsione= previsione, esito= esito, algoritmo=1)
            print(importazione)
            importazione.save()
