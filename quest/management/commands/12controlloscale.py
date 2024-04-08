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
        yesterday = today + timedelta(1)

        day_0 = datetime(year = yesterday.year, month=yesterday.month, day=yesterday.day, tzinfo=pytz.utc)
        day_1 = datetime(year = today.year, month=today.month, day=today.day, tzinfo=pytz.utc)

        candidati = CandidatoAzienda.objects.filter( giorno__range=[day_1, day_0])
        user = MyUser.objects.filter(candidatoazienda__in = candidati)
        print(user)
        user = 102
        scale = Scala.objects.get(candidato = user)
        print(scale.candidato)
        print('imagination=',  scale.imagination)
        print('artisticinterests=',  scale.artisticinterests)
        print('emotionality=',  scale.emotionality)
        print('adventurousness=',  scale.adventurousness)
        print('intellect=',  scale.intellect)
        print('liberalism=',  scale.liberalism)
        print('rabbia=',  scale.rabbia)
        print('aggressivita=',  scale.aggressivita)
        print('depression=',  scale.depression)
        print('selfconsciousness=',  scale.selfconsciousness)
        print('vulnerability=',  scale.vulnerability)
        print('ansia=',  scale.ansia)
        print('dipendenza=',  scale.dipendenza)
        print('autoefficacia=',  scale.autoefficacia)
        print('orientamentorisultato=',  scale.orientamentorisultato)
        print('autodisciplina=',  scale.autodisciplina)
        print('personalitaproattiva=',  scale.personalitaproattiva)
        print('ordine=',  scale.ordine)
        print('sensodovere=',  scale.sensodovere)
        print('cauteladelibera=',  scale.cauteladelibera)
        print('fiduciaaltri=',  scale.fiduciaaltri)
        print('altruismo=',  scale.altruismo)
        print('empatia=',  scale.empatia)
        print('simpatia=',  scale.simpatia)
        print('cooperazione=',  scale.cooperazione)
        print('modestia=',  scale.modestia)
        print('onesta=',  scale.onesta)
        print('gregarieta=',  scale.gregarieta)
        print('ricercasensazioni=',  scale.ricercasensazioni)
        print('assertivita=',  scale.assertivita)
        print('livelloattivita=',  scale.livelloattivita)
        print('emozionipositive=',  scale.emozionipositive)
        print('capacitagestireemozionipositive=',  scale.capacitagestireemozionipositive)
        print('intelligenzaemotiva=',  scale.intelligenzaemotiva)
        print('desiderabilitasociale=',  scale.desiderabilitasociale)
        print('percezionecontrollogeneraleesterno=',  scale.percezionecontrollogeneraleesterno)
        print('percezionecontrollogeneraleinterno=',  scale.percezionecontrollogeneraleinterno)
        print('orientamentoapprend=',  scale.orientamentoapprend)
