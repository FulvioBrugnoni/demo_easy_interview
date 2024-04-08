from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
import pytz

class MyUserManager(BaseUserManager):
    user_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """

        email = self.normalize_email(email)
#        username = email
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.ruolo = 1
        user.save(using=self._db)
        return user

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

class MyUser(AbstractUser):
    def is_recruiter(self):
#        return self.groups.filter(name='recruiter').exists()
        return self.ruolo==self.RECRUITER
    RECRUITER = 1
    STUDENTE = 2
    RUOLI = [(RECRUITER ,'recruiter'),
             (STUDENTE,'studente')]

    STATO_REGANA = 1
    STATO_REGSTUDI = 2
    STATI = [(STATO_REGANA,'RegistrazioneAnagraficaStep'),
             (STATO_REGSTUDI,'EsperienzeStudiStep'),
             ]

    ruolo = models.PositiveSmallIntegerField(choices=RUOLI)
    username = models.CharField(null = True, blank= True, max_length=256 )
    email= models.EmailField('Email', unique =True)
    stato = models.PositiveSmallIntegerField(choices=STATI,default =STATO_REGANA)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

#    objects = models.Manager()
    objects = MyUserManager()

    def __str__(self):
        return self.email


class GestioneInserimento(models.Model):

    passo_corrente = models.CharField(max_length=50)
    passo_destra = models.CharField(max_length=50)
    passo_sinistra = models.CharField(max_length=50)
    slide = models.IntegerField()

    class Meta:
            db_table ='gestione_inserimenti'
            verbose_name ='gestione_inserimenti'
            verbose_name_plural ='gestioni_inserimenti'
    def __str__(self):
        return self.passo_corrente

class Lingua(models.Model):

    lingua = models.CharField(max_length=25)

    class Meta:
            db_table ='lingua'
            verbose_name ='lingua'
            verbose_name_plural ='lingue'


    def __str__(self):
        return self.lingua



class Questionario(models.Model):

    name = models.CharField(max_length=25, unique=True)

    class Meta:
            db_table ='questionario'
            verbose_name ='questionario'
            verbose_name_plural ='questionari'
    def __str__(self):
        return self.name


class Domanda(models.Model):

    chiave= models.CharField(max_length=6, unique=True)
    testo = models.CharField(max_length=250, unique=True)

    class Meta:
            db_table ='domanda'
            verbose_name ='domanda'
            verbose_name_plural ='domande'
    def __str__(self):
        return self.chiave

class QuestionarioDomanda(models.Model):

    questionario= models.ForeignKey(Questionario, on_delete=models.PROTECT)
    domanda = models.ForeignKey(Domanda, on_delete=models.PROTECT)
    posizione =models.PositiveSmallIntegerField()

    class Meta:
            db_table ='questionario_domanda'
            verbose_name ='questionario_domanda'
            verbose_name_plural ='questionari_domanda'

            unique_together = [['questionario','domanda'],['questionario','posizione'],]

    def __str__(self):
        return f"{self.questionario.name}-{self.domanda.chiave} "

class Candidato(models.Model):

    user= models.CharField(max_length=15)

    class Meta:
            db_table ='candidato'
            verbose_name ='candidato'
            verbose_name_plural ='candidati'
    def __str__(self):
        return self.user

class Anagrafica(models.Model):

    candidato = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    nome = models.CharField(max_length=25)
    cognome = models.CharField(max_length=25)
    telefono = models.CharField(max_length=10)
    data = models.DateField()
    gender = models.CharField(max_length=1)

    class Meta:
            db_table ='anagrafica'
            verbose_name ='anagrafica'
            verbose_name_plural ='anagrafiche'

            ordering = ('pk',)
    def __str__(self):
        return self.nome

class Materia(models.Model):
    lingua = models.ForeignKey(Lingua, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Titolo(models.Model):
    lingua = models.ForeignKey(Lingua, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name



class Studio(models.Model):
    candidato = models.ForeignKey(MyUser, on_delete=models.PROTECT, null=True, blank=True)
    materia = models.ForeignKey(Materia, on_delete=models.PROTECT, null=True, blank=True)
    titolo = models.ForeignKey(Titolo, on_delete=models.PROTECT, null=True, blank=True)

    class Meta:
            db_table ='studio'
            verbose_name ='studio'
            verbose_name_plural ='studio'
    def __str__(self):
        return self.candidato


class Settore(models.Model):
    name = models.CharField(max_length=60, unique=True)
    lingua = models.ForeignKey(Lingua, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name


class Professione(models.Model):
    settore = models.ForeignKey(Settore, on_delete=models.CASCADE, null=True, blank=True)
    lingua = models.ForeignKey(Lingua, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class CandidatoEsperienza(models.Model):
    candidato = models.ForeignKey(MyUser, on_delete=models.PROTECT, null=True, blank=True)
    settore = models.ForeignKey(Settore, on_delete=models.SET_NULL, blank=True, null=True)
    professione = models.ForeignKey(Professione, on_delete=models.SET_NULL, blank=True, null=True)

#    def __str__(self):
#        return self.name


class Amm1(models.Model):
    name = models.CharField(max_length=50, unique=True)
#    lingua = models.ForeignKey(Lingua, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Amm2(models.Model):
    amm1 = models.ForeignKey(Amm1, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class Amm3(models.Model):
    amm2 = models.ForeignKey(Amm2, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name

class Amm4(models.Model):
    amm3 = models.ForeignKey(Amm3, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique=True)

    class Meta:
        ordering = ['name']
    def __str__(self):
        return self.name


class CandidatoResidenza(models.Model):
    candidato = models.ForeignKey(MyUser, on_delete=models.PROTECT, null=True, blank=True)
    amm1 = models.ForeignKey(Amm1, on_delete=models.SET_NULL, blank=True, null=True)
    amm2 = models.ForeignKey(Amm2, on_delete=models.SET_NULL, blank=True, null=True)
    amm3 = models.ForeignKey(Amm3, on_delete=models.SET_NULL, blank=True, null=True)
    amm4 = models.ForeignKey(Amm4, on_delete=models.SET_NULL, blank=True, null=True)

#    def __str__(self):
#        return self.candidato.email


class Lang(models.Model):
    lingua = models.ForeignKey(Lingua, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Livello(models.Model):
    lingua = models.ForeignKey(Lingua, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name



class Linguaconosciuta(models.Model):

    candidato = models.ForeignKey(MyUser, on_delete=models.PROTECT, null=True, blank=True)
    lingua = models.ForeignKey(Lang, on_delete=models.SET_NULL, blank=True, null=True)
    livello = models.ForeignKey(Livello, on_delete=models.SET_NULL, blank=True, null=True)

    class Meta:
            db_table ='lingua_conosciuta'
            verbose_name ='lingua_conosciuta'
            verbose_name_plural ='lingue_conosciuta'
#    def __str__(self):
#        return self.candidato


ANS_CHOICES = (
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
    ("6", "6"),
    ("7", "7"),
)

class Risposta(models.Model):

    utente= models.ForeignKey(MyUser, on_delete=models.PROTECT)
    domanda = models.ForeignKey(QuestionarioDomanda, on_delete=models.PROTECT)
    valutazione =models.CharField(max_length=1,choices=ANS_CHOICES)

    class Meta:
            db_table ='risposta'
            verbose_name ='risposta'
            verbose_name_plural ='risposte'

            unique_together = [['utente','domanda'],]

    def __str__(self):
        return self.utente




class AziendaLingua(models.Model):

    azienda = models.CharField(max_length=25, unique=True)
    lingua = models.ForeignKey(Lingua, on_delete=models.PROTECT)


    class Meta:
            db_table ='azienda'
            verbose_name ='azienda'
            verbose_name_plural ='aziende'

            unique_together = [['azienda','lingua'],]

    def __str__(self):
        return f'{self.azienda}, {self.lingua}'

class CandidatoAzienda(models.Model):

    candidato = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    azienda = models.ForeignKey(AziendaLingua, on_delete=models.PROTECT)
    giorno = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
            db_table ='candidato_azienda'
            verbose_name ='candidato_azienda'
            verbose_name_plural ='candidato_aziende'

    def __str__(self):
        return f'{self.candidato}, {self.azienda}'

class Testo(models.Model):

    testo = models.CharField(max_length=500)
    slide = models.CharField(max_length=25)
    posizione = models.CharField(max_length=25)
    lingua = models.ForeignKey(Lingua, on_delete=models.PROTECT)

    class Meta:
            db_table ='testo'
            verbose_name ='testo'
            verbose_name_plural ='testi'

    def __str__(self):
        return self.testo

class CandidatoParametro(models.Model):

    candidato = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    parametro = models.ForeignKey(AziendaLingua, on_delete=models.PROTECT)
    giorno = models.DateTimeField(default=datetime.now, blank=True)


    class Meta:
            db_table ='candidato_parametro'
            verbose_name ='candidato_parametro'
            verbose_name_plural ='candidato_parametri'
    def __str__(self):
        return f'{self.candidato}, {self.parametro}'


class AlgoritmoRecruit(models.Model):

    recruiter = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    algoritmo = models.CharField(max_length=5)
    parametro = models.ForeignKey(AziendaLingua, on_delete=models.PROTECT)

    class Meta:
            db_table ='algoritmo_recruit'
            verbose_name ='algoritmo_recruit'
            verbose_name_plural ='algoritmi_recruit'


    def __str__(self):
        return f"{self.recruiter}-{self.algoritmo}-{self.parametro.id} "


class Previsione(models.Model):

    candidato= models.ForeignKey(MyUser, on_delete=models.PROTECT)
    previsione =models.DecimalField( max_digits = 5, decimal_places = 2)
#    esito = models.BooleanField()
    esito = models.CharField(max_length=2)
    algoritmo = models.CharField(max_length=5)

    class Meta:
            db_table ='previsione_corrente'
            verbose_name ='previsione_corrente'
            verbose_name_plural ='previsioni_corrente'


    def __str__(self):
        return f"{self.candidato}-{self.previsione} "

class CandidatoConsenso(models.Model):

    candidato= models.ForeignKey(MyUser, on_delete=models.PROTECT)
    consenso = models.CharField(max_length=5)


    class Meta:
            db_table ='candidato_consenso'
            verbose_name ='candidato_consenso'
            verbose_name_plural ='candidati_consenso'


    def __str__(self):
        return f"{self.candidato}-{self.consenso} "


class AziendaConsenso(models.Model):

    azienda= models.ForeignKey(AziendaLingua, on_delete=models.PROTECT)
    consenso = models.CharField(max_length=5)


    class Meta:
            db_table ='azienda_consenso'
            verbose_name ='azienda_consenso'
            verbose_name_plural ='aziende_consenso'


    def __str__(self):
        return f"{self.azienda}-{self.consenso} "


class PrevisioneControllo(models.Model):

    candidato= models.ForeignKey(MyUser, on_delete=models.PROTECT)
    parametro= models.ForeignKey(AziendaLingua, on_delete=models.PROTECT)
    algoritmo = models.CharField(max_length=5)
    giorno = models.DateTimeField(default=datetime.now, blank=True)

    class Meta:
            db_table ='previsione_controllo'
            verbose_name ='previsione_controllo'
            verbose_name_plural ='previsioni_controllo'


    def __str__(self):
        return f"{self.candidato}-{self.parametro} "


class Scala(models.Model):

    candidato= models.ForeignKey(MyUser, on_delete=models.PROTECT)
    imagination= models.IntegerField()
    artisticinterests= models.IntegerField()
    emotionality= models.IntegerField()
    adventurousness= models.IntegerField()
    intellect= models.IntegerField()
    liberalism= models.IntegerField()
    rabbia= models.IntegerField()
    aggressivita= models.IntegerField()
    impulsivita= models.IntegerField()
    depression= models.IntegerField()
    selfconsciousness= models.IntegerField()
    vulnerability= models.IntegerField()
    ansia= models.IntegerField()
    dipendenza= models.IntegerField()
    autoefficacia= models.IntegerField()
    orientamentorisultato= models.IntegerField()
    autodisciplina= models.IntegerField()
    personalitaproattiva= models.IntegerField()
    ordine= models.IntegerField()
    sensodovere= models.IntegerField()
    cauteladelibera= models.IntegerField()
    fiduciaaltri= models.IntegerField()
    altruismo= models.IntegerField()
    empatia= models.IntegerField()
    simpatia= models.IntegerField()
    cooperazione= models.IntegerField()
    modestia= models.IntegerField()
    onesta= models.IntegerField()
    gregarieta= models.IntegerField()
    ricercasensazioni= models.IntegerField()
    assertivita= models.IntegerField()
    livelloattivita= models.IntegerField()
    emozionipositive= models.IntegerField()
    capacitagestireemozionipositive= models.IntegerField()
    intelligenzaemotiva= models.IntegerField()
    desiderabilitasociale= models.IntegerField()
    percezionecontrollogeneraleesterno= models.IntegerField()
    percezionecontrollogeneraleinterno= models.IntegerField()
    orientamentoapprend= models.IntegerField()

    class Meta:
            db_table ='scala'
            verbose_name ='scala'
            verbose_name_plural ='scale'


    def __str__(self):
        return f"{self.candidato}-{self.imagination} "


class Privacy(models.Model):

    testo = models.TextField()
    slide = models.CharField(max_length=25)
    posizione = models.CharField(max_length=25)
    lingua = models.ForeignKey(Lingua, on_delete=models.PROTECT)

    class Meta:
            db_table ='privacy'
            verbose_name ='privacy'
            verbose_name_plural ='privacys'

    def __str__(self):
        return self.testo
