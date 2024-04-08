from .models import MyUser


class Step:
    def get_next_step(self):
        raise NotImplementedError()

    def get_prev_step(self):
        raise NotImplementedError()

    def get_redirect_url(self):
        return self.redirect_url

    @staticmethod
    def get_instance(state):
        if state == MyUser.STATO_REGANA:
            return RegistrazioneAnagraficaStep()
        elif state == MyUser.STATO_REGSTUDI:
            return EsperienzeStudiStep()
        elif state == 3:
            return EsperienzeLavorativeStep()
        elif state == 4:
            return ConoscenzaLingueStep()
        elif state == 5:
            return QuestionarioStep()
        elif state == 6:
            return UpdateStep()


class RegistrazioneAnagraficaStep(Step):

    redirect_url = 'registrazioni_anagrafica'

    def get_next_step(self):
        return EsperienzeLavorativeStep()

    def __str__(self):
        return 'RegistrazioneAnagraficaStep'




class EsperienzeStudiStep(Step):

    redirect_url = 'registrazioni_studi'

    def get_next_step(self):
        return EsperienzeLavorativeStep()

    def __str__(self):
        return 'EsperienzeStudiStep'


class EsperienzeLavorativeStep(Step):

    redirect_url = 'registrazioni_esperienze'

    def get_next_step(self):
        return ConoscenzaLingueStep()

    def __str__(self):
        return 'EsperienzeLavorativeStep'


class ConoscenzaLingueStep(Step):

    redirect_url = 'registrazioni_lingue'

    def get_next_step(self):
        return QuestionarioStep()

    def __str__(self):
        return 'ConoscenzaLingueStep'

class QuestionarioStep(Step):

    redirect_url = 'registrazioni_questionari'

    def get_next_step(self):
        return UpdateStep()

    def __str__(self):
        return 'QuestionarioStep'

class UpdateStep(Step):

    redirect_url = 'pagina_utente'

    def get_next_step(self):
        return UpdateStep()

    def __str__(self):
        return 'UpdateStep'



if __name__=='__main__':
    state = 6
    current_step = Step.get_instance(state)
    print(current_step)
    current_step = current_step.get_next_step()
    print(current_step)
