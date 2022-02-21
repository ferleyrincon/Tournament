from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class bienvenida(Page):
    def is_displayed(self):
        return self.round_number == 1


class instrucciones(Page):
    def is_displayed(self):
        return self.round_number == 1
    


class tarea(Page):
    def is_displayed(self):
        return self.round_number > 0

    form_model = 'player'
    form_fields = ['palabras', 'mistakes']
    if Constants.use_timeout:
        timeout_seconds = Constants.seconds_per_period

    def vars_for_template(self):
        legend_list = [j for j in range(5)]
        task_list = [j for j in range(Constants.letters_per_word)]
        task_width = 90 / Constants.letters_per_word
        return {'legend_list': legend_list,
                'task_list': task_list,
                'task_width': task_width,
                }

class resultados(Page):
    def is_displayed(self):
        self.player.set_pago_ronda()
        return self.round_number > 0
    def vars_for_template(self):
        return {
            "palabras": self.player.palabras,
            "ronda": self.round_number - 1,
        }


class pago_total(Page):
    def is_displayed(self):
        self.subsession.set_pago_jugadores()
        return self.round_number == Constants.num_rounds
    def vars_for_template(self): 
        return {
            "ronda_pagar" :  Constants.ronda_pagar - 1,
            "pago_total" : "$"+format(int(str(self.player.pago.to_real_world_currency(self.session)).split(",")[0]),',d')
        }
    
class gracias(Page):
    def is_displayed(self):
        return self.round_number == Constants.num_rounds


page_sequence = [
	bienvenida, 
	instrucciones,
	tarea,
    resultados,
	pago_total,
    gracias,
]
