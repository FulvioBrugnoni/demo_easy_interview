from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponsePermanentRedirect
from .forms import *
from quest.models import *
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .decorators import login_active_required, login_recruiter_required
from django.core.mail import send_mail
from .utils import Step
import logging
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.views import LoginView, PasswordResetCompleteView, PasswordResetView, PasswordResetDoneView, \
                                        PasswordResetConfirmView, PasswordChangeView, PasswordChangeDoneView, LogoutView
from django.contrib import messages
from .ricerca import RicercaCandidato
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta
import pytz

logger = logging.getLogger('www-logger')

def mail(request):
    send_mail('oggetto','body','info@easy-interview.com',['fulvio.brugnoni1984@gmail.com'],fail_silently = True)
    return HttpResponse('ciao')




def testo_candidato(candidato, slide):
            azienda = AziendaLingua.objects.filter(candidatoparametro__candidato = candidato).first().id
            lingua = Lingua.objects.filter(aziendalingua__id = azienda).first().id
            testo = Testo.objects.filter(lingua = lingua, slide =slide)
            return testo


@login_required
def dashboard(request):
    current_step = Step.get_instance(request.user.stato)
    return redirect(reverse(current_step.get_redirect_url()))

@login_recruiter_required
def utente2(request):
        return render(request,'quest/utente2.html')

def proxy(request):
        if  request.user.ruolo == 1:
            passaggio = 'tabella'
        elif request.user.candidatoazienda_set.exists():
            passaggio = 'pagina_personale'
        elif request.user.risposta_set.exists():
            passaggio = 'questionario'
        elif request.user.anagrafica_set.exists():
            passaggio = 'questionario'
        else:
            step = 'anagrafica'
        return HttpResponsePermanentRedirect(passaggio)

def proxy2(request):
        candidato = request.user
        testo = testo_candidato(candidato, 29)
        if  request.user.ruolo == 1:
            passaggio = 'rec'
        elif request.user.candidatoazienda_set.exists():
            passaggio = 'per-pg'
        elif request.user.risposta_set.exists():
            passaggio = 'quest'
        elif request.user.candidatoresidenza_set.exists():
            passaggio = 'quest'
        elif request.user.anagrafica_set.exists():
            passaggio = 'res'
        else:
            passaggio = 'per'
        passaggio = {'passaggio':passaggio, 'tab':testo}
        return render(request,'quest/proxy.html',passaggio)

def homepage(request):
        logger.debug('Errore!!!!')
        return render(request,'quest/home.html')

def inter(request):
        return render(request,'quest/inter.html')

def gestione_inserimento_view(request, passo_corrente,trace= None):
        gestione_ins = GestioneInserimento.objects.get(passo_corrente =passo_corrente)
        passo_sinistra = gestione_ins.passo_sinistra
        passo_destra = gestione_ins.passo_destra
        testo = 'testo'
        if trace:
            passo_destra+= f"/{trace}"
            passo_sinistra+= f"{trace}"
            azienda = AziendaLingua.objects.filter(azienda = trace).first().id
            lingua = Lingua.objects.filter(aziendalingua__id = azienda).first().id
            slide = GestioneInserimento.objects.get(passo_corrente =passo_corrente).slide
            testo = Testo.objects.filter(lingua = lingua, slide =slide)
        else:
            candidato = request.user
            azienda = AziendaLingua.objects.filter(candidatoparametro__candidato = candidato).first().id
            lingua = Lingua.objects.filter(aziendalingua__id = azienda).first().id
            slide = GestioneInserimento.objects.get(passo_corrente =passo_corrente).slide
            testo = Testo.objects.filter(lingua = lingua, slide =slide)
        tab = {'tab': testo, 'passo_destra':passo_destra, 'passo_sinistra':passo_sinistra,}
        return render(request,'quest/richiesta_inserimento.html',tab)


#---------------------------------------------------------------------------------------------------------


def registration_view(request,trace):
        azienda = AziendaLingua.objects.filter(azienda = trace).first().id
        lingua = Lingua.objects.filter(aziendalingua__id = azienda).first().id
        testo = Testo.objects.filter(lingua = lingua, slide =1)
#        print(len(testo))
        if request.method == "POST":
                form = CandidatoForm(request.POST)
                if form.is_valid():
                    user = form.save()
                    new_user = authenticate(email=form.cleaned_data['email'],password=form.cleaned_data['password1'],)
                    login(request, new_user)
#                    send_mail('oggetto','body','fulvio.brugnoni1984@gmail.com',['fulvio.brugnoni1984@gmail.com'],fail_silently = False)
                    return HttpResponseRedirect(reverse('registrazioni_anagrafica'))
        else:
            form = CandidatoForm(initial={'trace': trace})

        return render(request,'quest/registrazione_utente_.html', {'form': form, 'tab':testo,'trace': trace})

@login_required
def registration_anag_view(request,a=None):
        candidato = request.user
        testo = testo_candidato(candidato, 2)
        if request.method == "POST":
                form = AnagraficaForm(request.POST)
                if form.is_valid():
                    nome = form.cleaned_data["nome"]
                    cognome = form.cleaned_data["cognome"]
                    telefono = form.cleaned_data["telefono"]
                    data = form.cleaned_data["data"]
                    gender = form.cleaned_data["gender"]
                    u = Anagrafica(candidato =candidato, nome=nome, cognome=cognome, telefono=telefono,
                                 data =data, gender=gender)
                    u.save()
                    candidato.stato = MyUser.STATO_REGSTUDI
                    candidato.save()
#                    return HttpResponseRedirect('gestione-inserimento/2')
                    if a=='a':
                        return HttpResponseRedirect('/per-pg')
                    else:
                        return redirect(reverse('residenza_add'))
        else:
            form = AnagraficaForm()

        return render(request,'quest/registrazione_utente_anagrafica.html', {'form': form, 'tab':testo})

@login_required
def registration_stud_view(request,a=None):
        candidato = request.user
        testo = testo_candidato(candidato, 4)
        if request.method == "POST":
                form = StudioCreationForm(request.user,request.POST)
                if form.is_valid():
                    materia = form.cleaned_data["materia"]
                    titolo = form.cleaned_data["titolo"]
                    u = Studio(candidato =candidato, materia=materia, titolo=titolo)
                    u.save()
                    if a=='a':
                        return HttpResponseRedirect('/per-pg')
                    else:
                        return HttpResponseRedirect('ins/3')
        else:
            form = StudioCreationForm(request.user,request.POST)

        return render(request,'quest/registrazione_utente_studio.html', {'form': form, 'tab':testo})

@login_required
def esperienza_create_view(request,a=None):
    form = EsperienzaCreationForm(request.user)
    testo = testo_candidato(request.user, 5)
    if request.method == 'POST':
        form = EsperienzaCreationForm(request.user,request.POST)
        if form.is_valid():
            settore = form.cleaned_data["settore"]
            professione = form.cleaned_data["professione"]
            u = CandidatoEsperienza(candidato =request.user, settore=settore, professione=professione)
            u.save()
#            messages.info(request, 'ciao ciao')
            if a=='a':
                return HttpResponseRedirect('/per-pg')
            else:
                return HttpResponseRedirect('/ins/5')
    return render(request, 'quest/esperienza2.html', {'form': form, 'tab':testo})


def load_professioni(request):
    settore_id = request.GET.get('settore_id')
    professioni = Professione.objects.filter(settore_id=settore_id).all()
    return render(request, 'quest/professione_dropdown_list_options.html', {'professioni': professioni})

@login_required
def residenza_create_view(request,a=None):
#    form = ResidenzaCreationForm(request.user)
    testo = testo_candidato(request.user, 3)
    form = ResidenzaCreationForm(request.user)
    if request.method == 'POST':
        form = ResidenzaCreationForm(request.user,request.POST)
        if form.is_valid():
            amm1 = form.cleaned_data["amm1"]
            amm2 = form.cleaned_data["amm2"]
            amm3 = form.cleaned_data["amm3"]
            amm4 = form.cleaned_data["amm4"]
            u = CandidatoResidenza(candidato = request.user, amm1=amm1, amm2=amm2, amm3=amm3, amm4=amm4)
            u.save()

            if a=='a':
                return HttpResponseRedirect('/per-pg')
            else:
                return HttpResponseRedirect('/ins/2')
    return render(request, 'quest/residenza2.html', {'form': form, 'tab':testo})


def load_amm2(request):
    amm1_id = request.GET.get('amm1_id')
    amm2s = Amm2.objects.filter(amm1_id=amm1_id).all()
    return render(request, 'quest/amm_dropdown_list_options.html', {'items': amm2s})

def load_amm3(request):
    amm2_id = request.GET.get('amm2_id')
    amm3s = Amm3.objects.filter(amm2_id=amm2_id).all()
    return render(request, 'quest/amm_dropdown_list_options.html', {'items': amm3s})

def load_amm4(request):
    amm3_id = request.GET.get('amm3_id')
    amm4s = Amm4.objects.filter(amm3_id=amm3_id).all()
    return render(request, 'quest/amm_dropdown_list_options.html', {'items': amm4s})

def registration_lang_view(request,a=None):
        candidato = request.user
        testo = testo_candidato(request.user, 6)
        if request.method == "POST":
                form = LinguaCreationForm(request.user,request.POST)
                if form.is_valid():
                    lingua = form.cleaned_data["lingua"]
                    livello = form.cleaned_data["livello"]
                    u = Linguaconosciuta(candidato =candidato, lingua=lingua, livello=livello)
                    u.save()
                    if a=='a':
                        return HttpResponseRedirect('/per-pg')
                    else:
                        return HttpResponseRedirect('ins/7')
        else:
            form = LinguaCreationForm(request.user,request.POST)

        return render(request,'quest/registrazione_utente_lingua.html', {'form': form, 'tab':testo})


def prova_view(request):
#        query = Risposta.objects.filter(utente__id = 5).order_by('-domanda__posizione').first()
#         print(query.domanda)
        return render(request,'quest/prova.html')

@login_required
def quest_view(request):
        utente = request.user
        testo = testo_candidato(utente, 7)
        azienda = AziendaLingua.objects.filter(candidatoparametro__candidato = utente).first().id
        lingua = Lingua.objects.filter(aziendalingua__id = azienda).first().id
        if request.method == "POST":
            form = QuestionForm(request.POST)
            if form.is_valid():
                valutazione= form.cleaned_data["valutazione"]
                questionario_id= form.cleaned_data["questionario"]
                domanda_id= form.cleaned_data["domanda"]
                questionario_domanda =QuestionarioDomanda.objects.get(questionario__id =questionario_id, domanda__id = domanda_id)
                v = Risposta(utente=utente,domanda=questionario_domanda ,valutazione=valutazione)
                v.save()
                try:
                    questionario_domanda =QuestionarioDomanda.objects \
                        .get(questionario =questionario_domanda.questionario,
                        posizione=questionario_domanda.posizione +1 )
                    form = QuestionForm(initial={'questionario':questionario_domanda.questionario.id, 'domanda': questionario_domanda.domanda.id })
                except ObjectDoesNotExist:
                    parametri = CandidatoParametro.objects.filter(candidato = utente)
                    for parametro in parametri:
                        parametro = parametro.parametro
                        importazione = CandidatoAzienda(candidato=utente, azienda = parametro, giorno=datetime.now(pytz.utc))
                        importazione.save()
                    return HttpResponseRedirect(reverse('consenso'))
        else:
            questionario = Questionario.objects.get(id=lingua)
            risposte = Risposta.objects.filter(domanda__questionario =questionario, utente=utente).order_by('-domanda__posizione')
            if len(risposte) == 0:
                questionario_domanda =QuestionarioDomanda.objects.filter(questionario =questionario).order_by('posizione').first()

            else:
                ultima_questionario_domanda = risposte.first().domanda
                try:
                    questionario_domanda =QuestionarioDomanda.objects \
                        .get(questionario =ultima_questionario_domanda.questionario,
                            posizione=ultima_questionario_domanda.posizione +1 )
                except ObjectDoesNotExist:
                    return HttpResponseRedirect(reverse('consenso'))

            form = QuestionForm(initial={'questionario':questionario.id, 'domanda': questionario_domanda.domanda.id })

        return render(request,'quest/15c.html', {'form': form, 'testo_domanda':questionario_domanda.domanda.testo,'tab':testo})

#---------------------------------------------------------------------------------------------------------------------------------------------------------

@login_required
def riassunto_candidato(request):
    candidato = request.user
    testo = testo_candidato(request.user, 8)
    lingua = Linguaconosciuta.objects.filter(candidato = candidato)
    studio = Studio.objects.filter(candidato = candidato)
    esperienza = CandidatoEsperienza.objects.filter(candidato = candidato)
    angrafica_id = Anagrafica.objects.filter(candidato = candidato).order_by('id').last().id
    anagrafica = Anagrafica.objects.get(id = angrafica_id)
    residenza_id = CandidatoResidenza.objects.filter(candidato = candidato).order_by('id').last().id
    residenza = CandidatoResidenza.objects.get(id = residenza_id)
    testo_residenza = testo_candidato(request.user, 3)
    testo_anagrafica = testo_candidato(request.user, 2)
    testo_studi = testo_candidato(request.user, 4)
    testo_esperienza = testo_candidato(request.user, 5)
    testo_lingue = testo_candidato(request.user, 6)
    return render(request,'quest/riassunto_candidato.html', {'lingua': lingua,'studio': studio, \
    'esperienza': esperienza , 'anagrafica': anagrafica, 'residenza': residenza,'tab':testo, 'testo_residenza': testo_residenza, \
    'testo_anagrafica' : testo_anagrafica , 'testo_studi' : testo_studi, 'testo_esperienza' : testo_esperienza, \
    'testo_lingue' : testo_lingue })

@login_recruiter_required
def riassunto_candidato_recruiter(request, id):
    candidato = MyUser.objects.get(id =id)
    testo = testo_candidato(request.user, 8)
    lingua = Linguaconosciuta.objects.filter(candidato = candidato)
    studio = Studio.objects.filter(candidato = candidato)
    esperienza = CandidatoEsperienza.objects.filter(candidato = candidato)
    angrafica_id = Anagrafica.objects.filter(candidato = candidato).order_by('id').last().id
    anagrafica = Anagrafica.objects.get(id = angrafica_id)
    residenza_id = CandidatoResidenza.objects.filter(candidato = candidato).order_by('id').last().id
    residenza = CandidatoResidenza.objects.get(id = residenza_id)
    testo_residenza = testo_candidato(request.user, 3)
    testo_anagrafica = testo_candidato(request.user, 2)
    testo_studi = testo_candidato(request.user, 4)
    testo_esperienza = testo_candidato(request.user, 5)
    testo_lingue = testo_candidato(request.user, 6)
    return render(request,'quest/riassunto_candidato_recruiter.html', {'lingua': lingua,'studio': studio, \
    'esperienza': esperienza , 'anagrafica': anagrafica, 'residenza': residenza,'tab':testo, 'testo_residenza': testo_residenza, \
    'testo_anagrafica' : testo_anagrafica , 'testo_studi' : testo_studi, 'testo_esperienza' : testo_esperienza, \
    'testo_lingue' : testo_lingue})


@login_required
def cancella_lingua(request,id):
    Linguaconosciuta.objects.filter(id=id).delete()
    testo = testo_candidato(request.user, 9)
    tab = {'tab':testo}
    return render(request,'quest/cancella_dato.html',tab)

@login_required
def cancella_esperienza(request,id):
    CandidatoEsperienza.objects.filter(id=id).delete()
    testo = testo_candidato(request.user, 9)
    tab = {'tab':testo}
    return render(request,'quest/cancella_dato.html',tab)

@login_required
def cancella_studio(request,id):
    Studio.objects.filter(id=id).delete()
    testo = testo_candidato(request.user, 9)
    tab = {'tab':testo}
    return render(request,'quest/cancella_dato.html',tab)

@login_required
def quest_1(request):
    testo = testo_candidato(request.user, 27)
    tab = {'tab':testo}
    return render(request,'quest/quest_1.html',tab)

@login_required
def quest_2(request):
    testo = testo_candidato(request.user, 28)
    tab = {'tab':testo}
    return render(request,'quest/quest_2.html',tab)

@login_recruiter_required
def tabella(request):

    testo = testo_candidato(request.user, 12)
    form = Ricerca(request.user)
    ricerca_candidato = RicercaCandidato(request.GET,request.user)
    paginator = Paginator(ricerca_candidato.get_objects(), 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
#    print(paginator.count)
#    print(paginator.num_pages)
    pred = {'pred': ricerca_candidato.get_objects(),'page_obj': page_obj ,'form':form , 'tab':testo}
    return render(request,'quest/previsioni.html', pred)

def stampa(sender,user,**kwargs):

    request = kwargs['request']
    tracciamento = request.GET.get('trace',None)
    if tracciamento:
        azienda_lingua = AziendaLingua.objects.get(azienda= tracciamento)
        if request.user.candidatoazienda_set.exists():
            z = CandidatoAzienda(candidato = user, azienda = azienda_lingua, giorno=datetime.now(pytz.utc))
            z.save()
        else :
            z = CandidatoParametro(candidato = user, parametro = azienda_lingua, giorno=datetime.now(pytz.utc))
            z.save()

user_logged_in.connect(stampa)

class LoginTracciamento(LoginView):
    pass

class Logout(LogoutView):
    pass

class PasswordReset(PasswordResetView):
    template_name = 'registration/psw_reset_form.html'


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'registration/psw_reset_done.html'
    pass

class PasswordResetConfirm(PasswordResetConfirmView):
    template_name = 'registration/psw_reset_confirm.html'
    pass

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'registration/psw_reset_complete.html'
    pass

class PasswordChange(PasswordChangeView):
    template_name = 'registration/psw_change_form.html'
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['testo'] = testo_candidato(self.request.user, 14)
        return context

class PasswordChangeDone(PasswordChangeDoneView):
    template_name = 'registration/psw_change_done.html'
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['testo'] = testo_candidato(self.request.user, 15)
        return context


def prova_campo(request):
    form = EsperienzaCreationFormRecruiter(request.user, None)
    if request.method == 'POST':
        form = EsperienzaCreationFormRecruiter(request.user,request.POST)
        if form.is_valid():
            print('ciao')
            pass
    return render(request, 'quest/prova_campo.html', {'form': form})

@login_required
def oblio(request):
#    testo = testo_candidato(request.user, 27)

    Anagrafica.objects.filter(candidato = request.user).delete()
    Studio.objects.filter(candidato = request.user).delete()
    CandidatoEsperienza.objects.filter(candidato = request.user).delete()
    CandidatoResidenza.objects.filter(candidato = request.user).delete()
    Linguaconosciuta.objects.filter(candidato = request.user).delete()
    Risposta.objects.filter(utente = request.user).delete()
    CandidatoAzienda.objects.filter(candidato = request.user).delete()
    CandidatoParametro.objects.filter(candidato = request.user).delete()
    Previsione.objects.filter(candidato = request.user).delete()
    CandidatoConsenso.objects.filter(candidato = request.user).delete()
    PrevisioneControllo.objects.filter(candidato = request.user).delete()
    MyUser.objects.get(email = request.user).delete()


#    print("studio:",len(studio))
    tab = {'tab': "User deleted"}
    return render(request,'quest/oblio.html',tab)


@login_required
def consenso_form(request):
        candidato = request.user
        testo = testo_candidato(candidato, 30)

        if request.method == "POST":
                form = ConsensoForm(request.POST)
                if form.is_valid():
                    consenso = form.cleaned_data["consenso"]
                    u = CandidatoConsenso(candidato =candidato, consenso = consenso)
                    u.save()
#                    candidato.stato = MyUser.STATO_REGSTUDI
#                    candidato.save()
#                    return HttpResponseRedirect('gestione-inserimento/2')
                    return redirect(reverse('pagina_utente'))
        else:
            form = ConsensoForm()

        return render(request,'quest/consenso.html', {'form': form, 'tab':testo})


def privacy(request,trace=None):

    if trace == None:
        candidato = request.user
        azienda = AziendaLingua.objects.filter(candidatoparametro__candidato = candidato).first().id
        lingua = Lingua.objects.filter(aziendalingua__id = azienda).first().id
        testo = Privacy.objects.filter(lingua = lingua, slide =100)

    else:
        azienda = AziendaLingua.objects.filter(azienda = trace).first().id
        lingua = Lingua.objects.filter(aziendalingua__id = azienda).first().id
        testo = Privacy.objects.filter(lingua = lingua, slide =100)

    tab = {'tab': testo}
    return render(request,'quest/privacy.html',tab)
