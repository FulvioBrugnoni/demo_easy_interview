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

        elementi = Risposta.objects.all()
        utenti = []
        for elemento in elementi:
                utenti.append(elemento.utente)
        utenti = list(set(utenti))
        for utente in utenti:
            risposte = Risposta.objects.filter(utente = utente)
            if len(risposte) < 171:
                print(utente)
                rimanenti= 171 - len(risposte)
                print(rimanenti)
                ultima_risposta = risposte.last()
                ultima_domanda = ultima_risposta.domanda.id
                print(ultima_domanda)
                for i in range(rimanenti):
                    id = ultima_domanda +i
                    domanda = QuestionarioDomanda.objects.get(id =id)
                    inserimento = Risposta(utente = utente, domanda=domanda, valutazione=1)
                    try:
                        inserimento.save()
                        self.stdout.write(f'Nuovo Inserimento')
                    except IntegrityError:
                        self.stderr.write(f'Elemento già presente o non esistente')
