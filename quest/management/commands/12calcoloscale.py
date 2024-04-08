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
        R = [1]
        for u in user:
#            risultati = Risposta.objects.filter(utente__in = u )
            risultati = Risposta.objects.filter(utente = u )
            print(u)

            for r in risultati:
                R.append((r.valutazione))
            O = int(R[1])+int(R[2])

            importazione = Scala(candidato= u,
            imagination = +int(R[118])+int(R[25])-int(R[37])-int(R[146]) ,
            artisticinterests = +int(R[1])+int(R[150])+int(R[76])+int(R[67]) ,
            emotionality = +int(R[157])+int(R[86])+int(R[88])+int(R[96]) ,
            adventurousness = +int(R[6])+int(R[79])-int(R[58])+int(R[83]) ,
            intellect = +int(R[45])+int(R[145])-int(R[38])+int(R[154]) ,
            liberalism = +int(R[163])+int(R[41])+int(R[111])-int(R[161]) ,
            rabbia = +int(R[8])+int(R[109])-int(R[57])-int(R[84]) ,
            aggressivita = +int(R[125])+int(R[36])+int(R[49])+int(R[121]) ,
            impulsivita = +int(R[9])+int(R[160])+int(R[54])+int(R[139]) ,
            depression = +int(R[78])+int(R[70])-int(R[133])-int(R[62])+int(R[32])-int(R[91])-int(R[171])-int(R[48]) ,
            selfconsciousness = +int(R[50])+int(R[33])+int(R[136])+int(R[52]) ,
            vulnerability = +int(R[7])-int(R[141])+int(R[51])+int(R[43])-int(R[14])-int(R[158])-int(R[28]) ,
            ansia = +int(R[59])+int(R[117])+int(R[85])+int(R[35]) ,
            dipendenza = +int(R[30])+int(R[77])+int(R[114])+int(R[66]) ,
            autoefficacia = +int(R[169])+int(R[74])+int(R[127])+int(R[97]) ,
            orientamentorisultato = +int(R[123])+int(R[168])+int(R[34])+int(R[12]) ,
            autodisciplina = +int(R[92])-int(R[105])+int(R[68])+int(R[95]) ,
            personalitaproattiva = +int(R[151])+int(R[56])+int(R[159])+int(R[135]) ,
            ordine = +int(R[149])+int(R[130])+int(R[100])+int(R[116]) ,
            sensodovere = +int(R[22])+int(R[63])+int(R[42])-int(R[80]) ,
            cauteladelibera = +int(R[65])+int(R[53])+int(R[21])+int(R[119]) ,
            fiduciaaltri = -int(R[104])-int(R[165])-int(R[73])-int(R[3]) ,
            altruismo = +int(R[13])+int(R[27])+int(R[20])+int(R[47]) ,
            empatia = -int(R[132])+int(R[137])+int(R[99])-int(R[113]) ,
            simpatia = +int(R[120])-int(R[61])+int(R[87])+int(R[13]) ,
            cooperazione = +int(R[152])-int(R[40])+int(R[39])-int(R[46]) ,
            modestia = -int(R[101])-int(R[60])-int(R[89])-int(R[16]) ,
            onesta = -int(R[81])-int(R[98])-int(R[138])-int(R[102])-int(R[131])-int(R[143])+int(R[122])+int(R[93]) ,
            gregarieta = -int(R[75])+int(R[148])+int(R[94])-int(R[55])-int(R[2])-int(R[82]) ,
            ricercasensazioni = +int(R[164])+int(R[144])+int(R[162])+int(R[5]) ,
            assertivita = -int(R[17])-int(R[26])-int(R[71])-int(R[112])+int(R[11])-int(R[142]) ,
            livelloattivita = -int(R[72])-int(R[126])+int(R[18])+int(R[4]) ,
            emozionipositive = +int(R[129])+int(R[31])+int(R[140])+int(R[170]) ,
            capacitagestireemozionipositive = +int(R[107])+int(R[69])+int(R[44])+int(R[128]) ,
            intelligenzaemotiva = -int(R[153])+int(R[110])+int(R[147])+int(R[23]) ,
            desiderabilitasociale = +int(R[103])+int(R[24])+int(R[124])+int(R[15]) ,
            percezionecontrollogeneraleesterno = +int(R[116])+int(R[19])-int(R[29])-int(R[115]) ,
            percezionecontrollogeneraleinterno = -int(R[155])-int(R[44])+int(R[156])+int(R[108]) ,
            orientamentoapprend = +int(R[106])+int(R[134])+int(R[90])+int(R[10]) )

            importazione.save()
            print(O)
