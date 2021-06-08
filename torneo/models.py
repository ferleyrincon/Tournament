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

from otree.models import subsession

author = 'Cesar Mantilla & Ferley Rincon'

doc = """
Mobility and productivity in a Dual Labor Market: a lab experiment.
"""

class Constants(BaseConstants):
    name_in_url = 'Torneo'
    players_per_group = 4
    num_rounds = 3
    payoff_A = c(2000)
    payoff_B = c(1000)
    round_payoff = random.randint(2, num_rounds)
    letters_per_word = 5
    use_timeout = True
    seconds_per_period = 90

class Subsession(BaseSubsession):
    merit = models.BooleanField(
        choices=[
                [False, 'luck'],
                [True, 'merit'],
            ]
    )
    discrimination = models.IntegerField(
        choices=[
                [1, 'random'],
                [2, 'perfect'],
                [3, 'noisy'],
            ]
        )
    tournament = models.BooleanField()
    round_payoff = models.IntegerField()

    def creating_session(self):
        """Esta función define los valores iniciales para cada ronda
        incluye la subsession y demás clases.
        Este método se ejecuta al comiezo de la sesion tantas veces como
        rondas haya"""
        self.discrimination = self.session.config["discrimination"]
        self.merit = self.session.config["merit"]
        self.round_payoff = Constants.round_payoff
        # Subsession Practice round (round<1), Tournament (round>1)
        self.tournament = self.round_number > 1

    def creating_groups(self):
        # Random stratified group matching
        players = self.get_players() #devuelve un array de objeto jugador
        num_groups = len(self.get_groups())
        a1, a2, b1, b2 = [], [], [], []
        for i in players:
            if i.contract_A_tournament:
                if i.position_contract_tournament == 1:
                    a1.append(i.in_round(self.round_number+1))  
                else:
                    a2.append(i.in_round(self.round_number+1))
            else:
                if i.position_contract_tournament == 1:
                    b1.append(i.in_round(self.round_number+1))  
                else:
                    b2.append(i.in_round(self.round_number+1))
            i.in_round(self.round_number+1).contract_A = i.contract_A_tournament

        matrix = np.c_[a1, a2, b1, b2]
        for i in range(Constants.players_per_group):
            x = np.random.choice(num_groups, num_groups, replace=False)
            matrix[:, i] = matrix[x, i]
        self.in_round(self.round_number+1).set_group_matrix(matrix)

    def sort(self, rank):
        l = list(rank.items())
        random.shuffle(l)
        rank = dict(l)
        rank = dict(sorted(rank.items(), key=lambda x: x[1], reverse=True))
        return rank

    """Este método retorna la posición del jugador en el ranking grupal"""
    def set_ranking(self):
        players = self.get_players()
        rank = {}
        for k, j in enumerate(players):
            rank['j' + str(k)] = j.tasks
        if (self.merit and self.round_number==1) or (self.discrimination > 0 and 
            self.round_number!=1):
            rank = self.sort(rank)
        else: 
            l = list(rank.items())
            random.shuffle(l)
            rank = dict(l)
        for j, i in enumerate(rank.keys()):
            jugador = players[int(i.split('j')[1])]
            # Half of the players are contract A (Primera mitad de los players es contrato A)
            if j < len(players)//2:
                jugador.contract_A_tournament = True
                # Players in the 1st quarter are in position Contract A1 (Primeta mitad de la mitad, primer cuarto, son posicion 1 contrato A)
                if j < len(players)//4:
                    jugador.position_contract_tournament = 1
                # The other 2nd quarter are in position Contract A2  (La otra mitad seria posicion 2 contrato A)
                else:
                    jugador.position_contract_tournament = 2
            # Half of the players are contract A (La otra mitad son contato B)
            else:
                jugador.contract_A_tournament= False
                # Players in the 3rd quarter are in position Contract B1 (La primera mitad de la mitad de B, osea 3/4, son posicion 1)
                if j < 3*len(players)//4:
                    jugador.position_contract_tournament = 1
                else:
                    jugador.position_contract_tournament = 2
            if(self.round_number==1):
                jugador.contract_A = jugador.contract_A_tournament
    
    def set_ranking_groups(self):
        for g in self.get_groups():
            g.set_ranking()
            g.set_ranking_contract()
    
    def set_positions_players(self):
        for j in self.get_players():
            j.set_payoff_round()
            j.set_position_group()
            j.set_position_contract()
            j.set_likelihood_contract_A()

    def set_payoff_players(self):
        for j in self.get_players():
            j.set_payoff()
            j.set_payoff_complete()
    
    def set_contract_A_players(self):
        if (self.round_number!=1):
            if (self.discrimination > 0):
                for j in self.get_players():
                    j.set_contract_A_tournament()
            else:
                for g in self.get_groups():
                    g.set_contract_A_tournament_random()

class Group(BaseGroup):
    #solo deben declararse variables por medio de models.
    rank = models.StringField()
    rankA = models.StringField()
    rankB = models.StringField()
    winner_contract_A = models.IntegerField(initial=0)
    tasks_tournament = models.IntegerField(initial=0)

    def get_tasks_tournament(self):
        rankA = json.loads(self.rankA)
        rankB = json.loads(self.rankB) 
        p2 = list(rankA.values())[1]  # tasks player in position A2 (palabras del jugador en la posicion 2 del ranking A)
        p3 = list(rankB.values())[0]  # tasks player in position B1 (palabras del jugador en la posicion 1 del ranking B)
        tasks_tournament = p2 + p3
        return tasks_tournament

    def set_winner_contract_A(self):
        rankA = json.loads(self.rankA)
        rankB = json.loads(self.rankB)
        p2 = self.get_player_by_id(int(list(rankA.keys())[1].split('j')[1]))
        p3 = self.get_player_by_id(int(list(rankB.keys())[0].split('j')[1]))
        p_choise = [str(list(rankA.keys())[1]).split('j')[1], str(list(rankB.keys())[0]).split('j')[1]]
        self.winner_contract_A = int(random.choices(p_choise, weights=[p2.likelihood_contract_A, p3.likelihood_contract_A], k = 1)[0])
        return self.winner_contract_A
        
    def sort(self, rank):
        l = list(rank.items())
        random.shuffle(l)
        rank = dict(l)
        rank = dict(sorted(rank.items(), key=lambda x: x[1], reverse=True))
        return rank

    def set_ranking(self):
        players = self.get_players() # [<P1>,<P2>,]
        rank = {}
        for k,j in enumerate(players):
            rank['j' + str(k+1)] = j.tasks
        self.rank = json.dumps(self.sort(rank))
        # '{'j1':7, 'j2':5 }'

    def set_contract_A_tournament_random(self):
            players = self.get_players()
            rank = {}
            for k, j in enumerate(players):
                rank['j' + str(k)] = j.tasks
                l = list(rank.items())
                random.shuffle(l)
                rank = dict(l)
            for j, i in enumerate(rank.keys()):
                jugador = players[int(i.split('j')[1])]
                if j < len(players)//2:
                    jugador.contract_A_tournament = True
                    if j < len(players)//4:
                        jugador.position_contract_tournament = 1
                    else:
                        jugador.position_contract_tournament = 2
                else:
                    jugador.contract_A_tournament= False
                    if j < 3*len(players)//4:
                        jugador.position_contract_tournament = 1
                    else:
                        jugador.position_contract_tournament = 2   
    

    def set_ranking_contract(self):
        rankA = {}
        rankB = {}
        for k,j in enumerate(self.get_players()):
            if j.contract_A:
                rankA['j' + str(k+1)] = j.tasks
            else:
                rankB['j' + str(k+1)] = j.tasks
        self.rankA = json.dumps(self.sort(rankA))
        self.rankB = json.dumps(self.sort(rankB))

class Player(BasePlayer):
    contract_A = models.BooleanField()
    likelihood_contract_A = models.FloatField()
    contract_A_tournament = models.BooleanField()
    position_group = models.IntegerField() #De 1-4
    position_contract = models.IntegerField() #De 1-2
    position_contract_tournament = models.IntegerField() #De 1-2
    payoff_round = models.CurrencyField()
    pago = models.CurrencyField()
    payoff_complete  = models.CurrencyField()
    mistakes = models.IntegerField(initial=0)
    tasks = models.IntegerField(initial=0)
    consent = models.BooleanField(blank=True)
    consent_account = models.BooleanField(blank=True)
    identificador = models.StringField(label='Para iniciar por favor ingrese las iniciales de su primer nombre y apellido seguido de su fecha de nacimiento. Por ejemplo, si usted se llama Lina Ríos y usted nació el 11 de febrero de 1995, debe ingresar LR11021995. Escriba todo en mayúscula. Este código es importante para asegurar su participación en el resto de la actividad y la realización de los pagos.')
    
    p1 = models.IntegerField(
    choices=[
        [1, 'Hombre'],
        [2, 'Mujer'],
        [3, 'Otro'],
    ], label="¿Con qué género se identifica?")
    p2 = models.IntegerField(label="Edad")
    p3 = models.IntegerField(
    choices=[
        [1,'Estudiante'],
        [2,'Desempleado'],
        [3,'Empleado a jornada completa'],
        [4,'Empleado a tiempo parcial'],
        [5,'Trabajador independiente'],
        [6,'Trabajador no remunerado (por ejemplo: ama de casa, empresa familiar)'],
        [7,'Retirado/pensionado'],
        [8,'Otro'],
        [9,'No sabe']
    ], label="¿Cuál es su situación laboral actual?")
    p4 = models.IntegerField(
    choices=[
        [1,'Ninguno'],
        [2,'Primaria incompleta'],
        [3,'Primaria'],
        [4,'Bachillerato'],
        [5,'Técnico o Tecnólogo'],
        [6,'Pregrado'],
        [7,'Posgrado (Especialización, Maestría, Doctorado)']
    ], label="¿Cuál es el nivel educativo más alto que ha completado?")
    p5 = models.StringField(label="Escriba el nombre de su profesión/ocupación")
    p6 = models.IntegerField(
    choices=[
        [1,'Subsidiado'],
        [2,'Contributivo (incluye regímenes especiales)']
    ], label="A qué régimen de seguridad social en salud pertenece")
    p7 = models.IntegerField(
    choices=[
        [1,'Menos del Salario Mínimo Mensual (SMMLV)'],
        [2,'Entre 1 SMMLV - $ 1.500.000'],
        [3,'Entre $ 1.500.000 - $ 2.000.000'],
        [4,'Entre $ 2.000.000 - $ 4.000.000'],
        [5,'Mayor a $ 4.000.000'],
    ], label="¿Cuál es el rango de su ingreso mensual?")
    p_risk = models.IntegerField(widget=widgets.RadioSelectHorizontal, 
                                 label="", 
                                 choices=[  [0, "0"],
                                            [1, "1"],
                                            [2, "2"],
                                            [3, "3"],
                                            [4, "4"],
                                            [5, "5"],
                                            [6, "6"],
                                            [7, "7"],
                                            [8, "8"],
                                            [9, "9"],
                                            [10, "10"]])


    #Esta función define el pago final
    def set_payoff(self):
        if (self.round_number==Constants.num_rounds):
            ronda = self.subsession.round_payoff
            payoff_rounds = []
            for j in self.in_all_rounds():
                payoff_rounds.append(j.payoff_round)
            self.pago= payoff_rounds[ronda- 1]
        else:
            self.pago= 0
 #           j.pago = j.pago_ronda.in_all_rounds()[ronda - 1]
        
    def set_likelihood_contract_A(self):
        if self.subsession.discrimination == 0:
            self.likelihood_contract_A = 0.5
        else:     
            if (self.contract_A == True and self.position_contract == 1):
                    self.likelihood_contract_A = 1
            elif (self.contract_A == False and self.position_contract == 2):
                    self.likelihood_contract_A = 0
            else:
                if self.subsession.discrimination == 1:#(perfect)
                    if (self.tasks > self.group.get_tasks_tournament()/2):
                        self.likelihood_contract_A = 1
                    elif (self.tasks == self.group.get_tasks_tournament()/2):
                        self.likelihood_contract_A = 0.5
                    else:
                        self.likelihood_contract_A = 0
                else: #subsession.discrimination == 2 (noisy)
                    if self.group.get_tasks_tournament() == 0:
                        self.likelihood_contract_A = 0.5
                    else:
                        self.likelihood_contract_A = self.tasks / self.group.get_tasks_tournament()

    def set_position_group(self):
        rank = json.loads(self.group.rank)
        self.position_group = list(rank.keys()).index('j' + str(self.id_in_group)) + 1

    def set_position_contract(self):
        rankA = json.loads(self.group.rankA)
        rankB = json.loads(self.group.rankB)
        if self.contract_A:
            self.position_contract = list(rankA).index('j' + str(self.id_in_group)) + 1
        else:
            self.position_contract = list(rankB).index('j' + str(self.id_in_group)) + 1

    def set_contract_A_tournament(self):
            winner = self.group.set_winner_contract_A()
            if (self.contract_A == True and self.position_contract == 1) or (self.contract_A == False and self.position_contract == 2):
                self.contract_A_tournament = self.contract_A
                if self.position_contract == 1:
                    self.position_contract_tournament = 1
                else:
                    self.position_contract_tournament = 2
            else:
                if self.id_in_group == int(winner):
                    self.contract_A_tournament = True
                    self.position_contract_tournament = 2
                else:
                    self.contract_A_tournament = False
                    self.position_contract_tournament = 1


    def set_payoff_round(self):
        if (self.contract_A):
            self.payoff_round= Constants.payoff_A * self.tasks
        else:
            self.payoff_round = Constants.payoff_B * self.tasks

    def set_payoff_complete(self):
        if (self.round_number==Constants.num_rounds):
            self.payoff_complete = self.pago + 4000
        return self.payoff_complete 