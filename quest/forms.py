from django import forms
from django.utils.translation import gettext_lazy as _
from .models import *
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
import pytz
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class CandidatoForm(UserCreationForm):
        email = forms.EmailField(label='user', max_length=25)
        trace = forms.CharField(label='trace', max_length=25, widget=forms.HiddenInput())
        ruolo = forms.IntegerField( widget=forms.HiddenInput(), initial = MyUser.STUDENTE )
        captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
#        captcha = ReCaptchaField()

        class Meta:
            model = MyUser
            fields = ('email','password1','password2','trace')
        def save(self,commit = True):
            user = super(CandidatoForm, self).save(commit=False)
            user.ruolo = self.cleaned_data['ruolo']
            trace = self.cleaned_data['trace']
#            azienda_lingua = AziendaLingua.objects.get(azienda= tracciamento, lingua__id = 1)
            azienda_lingua = AziendaLingua.objects.get(azienda= trace)
            giorno = datetime.now(pytz.utc)
            z = CandidatoParametro(candidato = user, parametro = azienda_lingua, giorno=giorno)
            if commit:
                user.save()
                z.save()
            return user,z



class AnagraficaForm(forms.Form):

        nome = forms.CharField(label= _('form.anagrafica.nome'), max_length=25)
        cognome = forms.CharField(label='cognome', max_length=25)
        telefono = forms.CharField(label='telefono', max_length=10)
        data = forms.DateField( )
        CHOICES=[('M','M'),
                ('F','F'),
                ]
        gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label= 'gender')

class ConsensoForm(forms.Form):


        CHOICES=[('YES','YES'),
                ('NO','NO'),
                ]
        consenso = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label= 'consenso')


class StudioForm(forms.Form):
        titolo = forms.CharField(label='titolo', max_length=25)

class LinguaForm(forms.Form):
        lingua = forms.CharField(label='lingua', max_length=25)
        livello = forms.CharField(label='livello', max_length=25)

class QuestionForm(forms.Form):
    questionario = forms.IntegerField()
    domanda = forms.IntegerField()
#     valutazione = forms.CharField()
    CHOICES=[('1','1'),
             ('2','2'),
             ('3','3'),
             ('4','4'),
             ('5','5'),
             ('6','6'),
             ('7','7'),]
    valutazione = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, label= 'Ciao')


class MyUserChangeForm(UserChangeForm):
    ruolo = forms.IntegerField()

    class Meta(UserChangeForm.Meta):
        model = MyUser



class EsperienzaCreationForm(forms.ModelForm):

    class Meta:
        model = CandidatoEsperienza
        fields = ['settore','professione',]

    def __init__(self,user,*args, **kwargs):
        try:
            super().__init__(user=user, *args, **kwargs)
        except TypeError:
            super().__init__(*args, **kwargs)
        azienda = AziendaLingua.objects.filter(candidatoparametro__candidato = user).first().id
        lingua = Lingua.objects.filter(aziendalingua__id = azienda).first().id
#        print(self.fields)
        self.fields['settore'] = forms.ModelChoiceField(queryset = Settore.objects.filter(lingua__id = lingua))
        self.fields['professione'] = forms.ModelChoiceField(queryset = Professione.objects.none())

        if 'settore' in self.data:
            try:
                settore_id = int(self.data.get('settore'))
                print(settore_id)
                self.fields['professione'].queryset = Professione.objects.filter(settore_id=settore_id)
                print(Professione.objects.filter(settore_id=settore_id))
                print('ciao')
            except (ValueError, TypeError):
                print('errore')
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['professione'].queryset = self.instance.settore.professione_set


class ResidenzaCreationForm(forms.ModelForm):
#    def __init__(self,user,*args,**kwargs):
#        super().__init__(*args, **kwargs)
#        self.fields['amm1'] = forms.ModelChoiceField(queryset = Amm1.objects.filter(lingua__id = 1))
    class Meta:
        model = CandidatoResidenza
        fields = ['amm1','amm2','amm3','amm4']

    def __init__(self,user, *args, **kwargs):
        try:
            super().__init__( user=user, *args, **kwargs)
        except TypeError as err:
            super().__init__( *args, **kwargs)
        self.fields['amm2'].queryset = Amm2.objects.none()
        self.fields['amm3'].queryset = Amm3.objects.none()
        self.fields['amm4'].queryset = Amm4.objects.none()
        self.fields['amm1'].required = True
        self.fields['amm2'].required = True
        self.fields['amm3'].required = True
        self.fields['amm4'].required = True

        if 'amm1' in self.data:
            try:
                amm1_id = int(self.data.get('amm1'))
                self.fields['amm2'].queryset = Amm2.objects.filter(amm1_id=amm1_id)
            except (ValueError, TypeError):
                pass

        if 'amm2' in self.data:
            try:
                amm2_id = int(self.data.get('amm2'))
                self.fields['amm3'].queryset = Amm3.objects.filter(amm2_id=amm2_id)
            except (ValueError, TypeError):
                pass

        if 'amm3' in self.data:
            try:
                amm3_id = int(self.data.get('amm3'))
                self.fields['amm4'].queryset = Amm4.objects.filter(amm3_id=amm3_id)
            except (ValueError, TypeError):
                pass




class StudioCreationForm(forms.ModelForm):

    class Meta:
        model = Studio
        fields = '__all__'

    def __init__(self,user,*args, **kwargs):
        try:
            super().__init__( user=user, *args, **kwargs)
        except TypeError:
            super().__init__( *args, **kwargs)
        azienda = AziendaLingua.objects.filter(candidatoparametro__candidato = user).first().id
        lingua = Lingua.objects.filter(aziendalingua__id = azienda).first().id
        self.fields['materia'] = forms.ModelChoiceField(queryset = Materia.objects.filter(lingua__id = lingua))
        self.fields['titolo'] = forms.ModelChoiceField(queryset = Titolo.objects.filter(lingua__id = lingua))



class LinguaCreationForm(forms.ModelForm):

    class Meta:
        model = Linguaconosciuta
        fields = '__all__'

    def __init__(self,user,*args, **kwargs):
        super().__init__(*args, **kwargs)
        azienda = AziendaLingua.objects.filter(candidatoparametro__candidato = user).first().id
        lingua = Lingua.objects.filter(aziendalingua__id = azienda).first().id
        self.fields['lingua'] = forms.ModelChoiceField(queryset = Lang.objects.filter(lingua__id = lingua))
        self.fields['livello'] = forms.ModelChoiceField(queryset = Livello.objects.filter(lingua__id = lingua))
#        print(self.data)

class RangeEtaForm(forms.Form):
        min = forms.IntegerField(label= 'min_eta' , initial= 0)
        max = forms.IntegerField(label= 'max_eta' , initial= 99)

class GenderForm(forms.Form):
        CHOICES=[('',''),
                ('M','M'),
                ('F','F'),
                ]
        gender = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, initial='',label= 'gender')

class ApplicationForm(forms.Form):
        CHOICES=[('',''),
                ('Y','Y'),
                ('N','N'),
                ]
        application = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect, initial='',label= 'application')

class EmailForm(forms.Form):
        email = forms.EmailField(label='email', max_length=50)

class NomeCognomeForm(forms.Form):
        nome = forms.CharField(label= 'nome', max_length=25)
        cognome = forms.CharField(label='cognome', max_length=25)


class EsperienzaCreationFormRecruiter(EsperienzaCreationForm):
    def __init__(self,user,*args, **kwargs):
        super().__init__(user=user, *args, **kwargs)
        self.fields['settore'].required = False
        self.fields['professione'].required = False



class Ricerca(ResidenzaCreationForm,StudioCreationForm,EsperienzaCreationForm,RangeEtaForm,\
                LinguaCreationForm,ApplicationForm,GenderForm,EmailForm,NomeCognomeForm):

                    def __init__(self,user,*args, **kwargs):
                        super().__init__(user=user, *args, **kwargs)
                        for key in self.fields:
                            self.fields[key].required = False
