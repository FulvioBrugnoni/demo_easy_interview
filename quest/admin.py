from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import MyUserChangeForm


@admin .register(MyUser)
class MyUserAdmin(UserAdmin):
    list_display = ('id','username','email','ruolo','is_recruiter','stato')
    form = MyUserChangeForm
    fieldsets = UserAdmin.fieldsets+(('campi aggiuntivi',{
        'fields': ('ruolo','stato')
    }),)
    ordering = ['email',]
    def is_recruiter(self, obj):
        return obj.is_recruiter()
    is_recruiter.boolean = True
    is_recruiter.short_description = 'recruiter!'

@admin .register(GestioneInserimento)
class GestioneInserimentoAdmin(admin.ModelAdmin):
    list_display = ('passo_corrente','passo_sinistra','passo_destra','slide')
    pass

@admin .register(CandidatoParametro)
class CandidatoParametro(admin.ModelAdmin):
    list_display = ('candidato','parametro')
    pass

@admin .register(Lingua)
class Lingua(admin.ModelAdmin):
    pass

@admin .register(AziendaLingua)
class AziendaLingua(admin.ModelAdmin):
    pass

@admin .register(Questionario)
class Questionario(admin.ModelAdmin):
    pass

@admin .register(Domanda)
class Domanda(admin.ModelAdmin):
    list_display = ('chiave','testo')
    pass

@admin .register(QuestionarioDomanda)
class QuestionarioDomanda(admin.ModelAdmin):
    list_display = ('questionario','domanda','posizione')
    pass

@admin .register(Anagrafica)
class Anagrafica(admin.ModelAdmin):
    list_display = ('nome','cognome')
    pass

@admin .register(Studio)
class Studio(admin.ModelAdmin):
    list_display = ('candidato','titolo')
    pass

admin.site.register(Settore)
admin.site.register(Professione)
admin.site.register(CandidatoEsperienza)
admin.site.register(Amm1)
admin.site.register(Amm2)
admin.site.register(Amm3)
admin.site.register(Amm4)

@admin .register(CandidatoResidenza)
class CandidatoResidenza(admin.ModelAdmin):
    list_display = ('candidato','amm1','amm2','amm3','amm4')
    pass

admin.site.register(Lang)
admin.site.register(Livello)
admin.site.register(Titolo)
admin.site.register(Materia)
admin.site.register(AlgoritmoRecruit)

@admin .register(Linguaconosciuta)
class Linguaconosciuta(admin.ModelAdmin):
    list_display = ('candidato','lingua','livello')
    pass

@admin .register(Risposta)
class Risposta(admin.ModelAdmin):
    list_display = ('utente','domanda','valutazione')
    pass

@admin .register(CandidatoAzienda)
class CandidadtoAzienda(admin.ModelAdmin):
    pass

@admin .register(Testo)
class Testo(admin.ModelAdmin):
    list_display = ('testo','slide','posizione','lingua')
    pass

@admin .register(Previsione)
class Testo(admin.ModelAdmin):
    list_display = ('candidato','previsione','esito')
    pass

@admin .register(CandidatoConsenso)
class CandidatoConsenso(admin.ModelAdmin):
    pass

@admin .register(AziendaConsenso)
class AziendaConsenso(admin.ModelAdmin):
    pass

@admin .register(PrevisioneControllo)
class PrevisioneControllo(admin.ModelAdmin):
    pass

@admin .register(Privacy)
class Privacy(admin.ModelAdmin):
    pass
