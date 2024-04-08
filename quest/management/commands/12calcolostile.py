from django.core.management.base import BaseCommand, CommandError
from quest.models import *
from recruiter.models import *
import csv
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime, date, timedelta
import random
import pytz
import numpy as np
from scipy.spatial import distance

class Command(BaseCommand):

    def handle(self,*args,**kwargs):

#Query iniziale da verificare le date corrette per la schedulazione

        today = datetime.now(pytz.utc)
        yesterday = today + timedelta(1)

        day_0 = datetime(year = yesterday.year, month=yesterday.month, day=yesterday.day, tzinfo=pytz.utc)
        day_1 = datetime(year = today.year, month=today.month, day=today.day, tzinfo=pytz.utc)

        candidati = CandidatoAzienda.objects.filter( giorno__range=[day_1, day_0])
        user = MyUser.objects.filter(candidatoazienda__in = candidati)
        print(user)
        for u in user:
#            risultati = Risposta.objects.filter(utente__in = u )

#Calcolo della dello stile di risposta

            risultati = Risposta.objects.filter(utente = u )
            print(u)
            count_1 = 0
            count_2 = 0
            count_3 = 0
            count_4 = 0
            count_5 = 0
            count_6 = 0
            count_7 = 0
            C = []
            for r in risultati:
                if int(r.valutazione) == 1:
                    count_1 +=1
                if int(r.valutazione) == 2:
                    count_2 +=1
                if int(r.valutazione) == 3:
                    count_3 +=1
                if int(r.valutazione) == 4:
                    count_4 +=1
                if int(r.valutazione) == 5:
                    count_5 +=1
                if int(r.valutazione) == 6:
                    count_6 +=1
                if int(r.valutazione) == 7:
                    count_7 +=1
        C.append(count_1)
        C.append(count_2)
        C.append(count_3)
        C.append(count_4)
        C.append(count_5)
        C.append(count_6)
        C.append(count_7)
        print(C)

#Calcolo della distanze euclidee e associazione della media

        stili_1 = [[0,3,0,0,3,0,0],[0,12,0,0,3,0,4],[0,10,0,0,3,0,6]]
        medie_1 = [1, 2, 3]
        D = []

        for s in stili_1:
            dist = distance.euclidean(s,C)
            D.append(dist)

        min_dist = np.argmin(D)
        print(min_dist)
        print(medie_1[min_dist])
