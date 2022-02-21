from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import numpy as np
import random
import json

author = 'Ferley Rincón & Cesar Mantilla'

doc = """
Informalidad Laboral: Movilidad y Observabilidad Laboral
"""

class Constants(BaseConstants):
    name_in_url = 'Tarea'
    players_per_group = None
    num_rounds = 6
    pago = c(2000)
    ronda_pagar = random.randint(2, num_rounds)
    letters_per_word = 5
    use_timeout = True
    seconds_per_period = 20

class Subsession(BaseSubsession):
    ronda_pagar = models.IntegerField()

    def creating_session(self):
        """Esta función define los valores iniciales para cada ronda
        incluye la subsession y demás clases.
        Este método se ejecuta al comiezo de la sesion tantas veces como
        rondas haya"""
        self.ronda_pagar = Constants.ronda_pagar


    def set_pago_jugadores(self):
        for j in self.get_players():
            j.set_pago()

class Group(BaseGroup):
    pass

class Player(BasePlayer):
    palabras = models.IntegerField(initial=0) 
    pago = models.CurrencyField()
    pago_ronda = models.CurrencyField()
    mistakes = models.IntegerField(initial=0)
    filtro = models.IntegerField()

    #Esta función define el pago final
    def set_pago(self):
        if (self.round_number==Constants.num_rounds):
            ronda = self.subsession.ronda_pagar
            pagos_rondas = []
            for j in self.in_all_rounds():
                pagos_rondas.append(j.pago_ronda)
            self.pago= pagos_rondas[ronda - 1]
        
    
    def set_pago_ronda(self):
        self.pago_ronda = Constants.pago * self.palabras
 