from django.core.management.base import BaseCommand, CommandError
from quest.models import *
from recruiter.models import *
import csv
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
import datetime
import random

class Command(BaseCommand):

    def handle(self,*args,**kwargs):

        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        candidati = CandidatoAzienda.objects.filter(giorno__gt=yesterday)
        for candidato in candidati:
            obj = candidato.candidato.id
            candidato = MyUser.objects.get(id =obj)
            previsione = round(random.uniform(0,1),2)
            if previsione > 0.25:
                esito = 1
            else:
                esito = 0
            importazione = Previsione(candidato= candidato, previsione= previsione, esito= esito)
            importazione.save()
