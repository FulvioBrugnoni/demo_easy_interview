from .models import Previsione, CandidatoResidenza, Linguaconosciuta, Studio, CandidatoEsperienza, Anagrafica, MyUser, AlgoritmoRecruit, \
                    CandidatoParametro
from datetime import date, datetime


class RicercaCandidato:
    def __init__(self,params,user):
        self.params = params
        self.objects = Previsione.objects.all().order_by('-previsione')
        self.user = user

    def get_objects(self):
        self.filter_by_amm1()
        self.filter_by_amm2()
        self.filter_by_amm3()
        self.filter_by_amm4()
        self.filter_by_lingua()
        self.filter_by_studio()
        self.filter_by_esperienza()
#        self.filter_by_eta()
        self.filter_by_gender()
        self.filter_by_application()
        self.filter_by_email()
        self.filter_by_algoritmo()
        self.filter_by_nome_cognome()
        return self.objects

    def filter_by_amm1(self):
        if self.params.get('amm1','') != '':
            candidato_residenza = CandidatoResidenza.objects.filter(amm1 = self.params['amm1'])
            self.objects = self.objects.filter(candidato__id__in = candidato_residenza.values_list('candidato__id'))

    def filter_by_amm2(self):
        if self.params.get('amm2','') != '':
            candidato_residenza = CandidatoResidenza.objects.filter(amm2 = self.params['amm2'])
            self.objects = self.objects.filter(candidato__id__in = candidato_residenza.values_list('candidato__id'))

    def filter_by_amm3(self):
        if self.params.get('amm3','') != '':
            candidato_residenza = CandidatoResidenza.objects.filter(amm3 = self.params['amm3'])
            self.objects = self.objects.filter(candidato__id__in = candidato_residenza.values_list('candidato__id'))

    def filter_by_amm4(self):
        if self.params.get('amm4','') != '':
            candidato_residenza = CandidatoResidenza.objects.filter(amm4 = self.params['amm4'])
            self.objects = self.objects.filter(candidato__id__in = candidato_residenza.values_list('candidato__id'))

    def filter_by_lingua(self):
        if self.params.get('lingua','') != '':
            lingua_conosciuta = Linguaconosciuta.objects.filter(lingua = self.params['lingua'])
            self.objects = self.objects.filter(candidato__id__in = lingua_conosciuta.values_list('candidato__id'))
        if self.params.get('livello','') != '':
            livello = Linguaconosciuta.objects.filter(livello = self.params['livello'])
            self.objects = self.objects.filter(candidato__id__in = livello.values_list('candidato__id'))


    def filter_by_studio(self):
        if self.params.get('materia','') != '':
            materia = Studio.objects.filter(materia = self.params['materia'])
            self.objects = self.objects.filter(candidato__id__in = materia.values_list('candidato__id'))
        if self.params.get('titolo','') != '':
            titolo = Studio.objects.filter(titolo = self.params['titolo'])
            self.objects = self.objects.filter(candidato__id__in = titolo.values_list('candidato__id'))

    def filter_by_esperienza(self):
        if self.params.get('settore','') != '':
            settore = CandidatoEsperienza.objects.filter(settore = self.params['settore'])
            self.objects = self.objects.filter(candidato__id__in = settore.values_list('candidato__id'))
        if self.params.get('professione','') != '':
            professione = CandidatoEsperienza.objects.filter(professione = self.params['professione'])
            self.objects = self.objects.filter(candidato__id__in = professione.values_list('candidato__id'))

    def filter_by_gender(self):
        if self.params.get('gender','') != '':
            gender = Anagrafica.objects.filter(gender = self.params['gender'])
            self.objects = self.objects.filter(candidato__id__in = gender.values_list('candidato__id'))

    def filter_by_application(self):
        aziende = AlgoritmoRecruit.objects.filter(recruiter = self.user)
        set_aziende = set()
        for azienda in aziende:
            set_aziende.add(azienda.parametro.id)
        if self.params.get('application','') != '':
            if self.params.get('application','') == 'Y':
                application = CandidatoParametro.objects.filter(parametro__id__in = set_aziende)
            elif self.params.get('application','') == 'N':
                application = CandidatoParametro.objects.exclude(parametro__id__in  = set_aziende)
            self.objects = self.objects.filter(candidato__id__in = application.values_list('candidato__id'))

    def filter_by_email(self):
        if self.params.get('email','') != '':
            email = MyUser.objects.get(email = self.params['email'])
            self.objects = self.objects.filter(candidato = email)


    def filter_by_nome_cognome(self):
        if self.params.get('nome','') != '':
            nome = Anagrafica.objects.filter(nome = self.params['nome'])
            self.objects = self.objects.filter(candidato__id__in = nome.values_list('candidato__id'))
        if self.params.get('cognome','') != '':
            cognome = Anagrafica.objects.filter(cognome = self.params['cognome'])
            self.objects = self.objects.filter(candidato__id__in = cognome.values_list('candidato__id'))

    def filter_by_algoritmo(self):
        aziende = AlgoritmoRecruit.objects.filter(recruiter = self.user)
        set_algoritmo = set()
        for azienda in aziende:
            set_algoritmo.add(azienda.algoritmo)
        self.objects = self.objects.filter(algoritmo__in = set_algoritmo)

    def filter_by_eta(self):

        if self.params.get('min', '') != '':
            min = self.params['min']
        if self.params.get('max', '') != '':
            max = self.params['max']

            today = datetime.now()
            year_s = today.year - int(float(min)) - 1
            year_e = today.year - int(float(max))
            month = today.month
            day = today.day
            if day == 1:
                day = day
            else:
                day = day - 1
            end_date = date(year_e, month, day)
            start_date = date(year_s, month, day)
            eta = Anagrafica.objects.filter(data__range = [end_date, start_date])
            self.objects = self.objects.filter(candidato__id__in = eta.values_list('candidato__id'))
