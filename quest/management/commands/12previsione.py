from django.core.management.base import BaseCommand, CommandError
from quest.models import *
from recruiter.models import *
import csv
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date, timedelta
import random
import pytz


class Command(BaseCommand):

    def handle(self,*args,**kwargs):

        today = datetime.now(pytz.utc)
        yesterday = today - timedelta(1)
        day_0 = datetime(year = yesterday.year, month=yesterday.month, day=yesterday.day, tzinfo=pytz.utc)
        day_1 = datetime(year = today.year, month=today.month, day=today.day, tzinfo=pytz.utc)
        azienda = AziendaLingua.objects.get(azienda = 'A1')
        candidati = CandidatoAzienda.objects.filter(giorno__range=[day_0, day_1], azienda = azienda)

        for candidato in candidati:
            obj = candidato.candidato.id
            candidato = MyUser.objects.get(id =obj)
            previsione = round(random.uniform(0,1),2)
            if previsione > 0.25:
                esito = 1
            else:
                esito = 0
            importazione = Previsione(candidato= candidato, previsione= previsione, esito= esito, algoritmo=1)
            importazione.save()

        day_90 = today - timedelta(90)
        day_90_1 = day_90 - timedelta(1)
        day_s_90 = datetime(year = day_90_1.year, month=day_90_1.month, day=day_90_1.day, tzinfo=pytz.utc)
        day_a_90 = datetime(year = day_90.year, month=day_90.month, day=day_90.day, tzinfo=pytz.utc)
        azienda = AziendaLingua.objects.get(azienda = 'A1')
        candidati = CandidatoAzienda.objects.filter(giorno__range=[day_s_90, day_a_90]).exclude(azienda =azienda)

        for candidato in candidati:
            obj = candidato.candidato.id
            candidato = MyUser.objects.get(id =obj)
            previsione = round(random.uniform(0,1),2)
            if previsione > 0.25:
                esito = 1
            else:
                esito = 0
            importazione = Previsione(candidato= candidato, previsione= previsione, esito= esito, algoritmo=1)
            importazione.save()
