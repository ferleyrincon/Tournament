from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants

class device(Page):
    def is_displayed(self):
        return self.round_number == 1

class wait_all(WaitPage):
    wait_for_all_groups = True
    def is_displayed(self):
        return self.round_number == 1

class consent(Page):
    form_model = 'player'
    form_fields = ['consent','consent_account']

    def is_displayed(self):
        return self.round_number == 1

class welcome(Page):
    form_model = 'player'
    form_fields = ['identificador']

    def is_displayed(self):
        return self.round_number == 1

    def vars_for_template(self): 
        return {
            "consent" : self.player.consent,
            "consent_account" : self.player.consent_account
        }

class instructions_practice(Page):
    def is_displayed(self):
        return self.round_number == 1
    
    def vars_for_template(self):
        return {
            "merit" : self.session.config["merit"]
        }

class instructions_task(Page):
    def is_displayed(self):
        return self.round_number == 1

class instructions_tournament(Page):
    def is_displayed(self):
        return self.round_number == 2

    def vars_for_template(self): 
        return {
            "discrimination" : self.session.config["discrimination"]
        }

class quiz(Page):
    def is_displayed(self):
        return self.round_number == 2
    form_model = 'player'
    form_fields = ['p_random1', 'p_random2', 'p_perfect1', 'p_perfect2', 'p_noisy1', 'p_noisy2'] 

    def vars_for_template(self): 
        return {
            "discrimination" : self.session.config["discrimination"]
        }

class quiz_answer(Page):
    def is_displayed(self):
        return self.round_number == 2
    def vars_for_template(self): 
        return {
            "discrimination" : self.session.config["discrimination"],
            "p_random1" : self.player.p_random1,
            "p_random2" : self.player.p_random2,
            "p_perfect1" : self.player.p_perfect1,
            "p_perfect2" : self.player.p_perfect2,
            "p_noisy1" : self.player.p_noisy1,
            "p_noisy2" : self.player.p_noisy2,
        }
class task_practice(Page):
    def is_displayed(self):
        return self.round_number == 1

    form_model = 'player'
    form_fields = ['tasks', 'mistakes']
    if Constants.use_timeout:
        timeout_seconds = Constants.seconds_per_period

    def vars_for_template(self):
        legend_list = [j for j in range(5)]
        task_list = [j for j in range(Constants.letters_per_word)]
        task_width = 90 / Constants.letters_per_word
        return {'legend_list': legend_list,
                "round": self.round_number - 1, #Restar 1 al número de rondas. Ronda 0 = Práctica
                'task_list': task_list,
                'task_width': task_width,
                }
           
class task_tournament(Page):
    def is_displayed(self):
        return self.round_number > 1

    form_model = 'player'
    form_fields = ['tasks', 'mistakes']
    if Constants.use_timeout:
        timeout_seconds = Constants.seconds_per_period

    def vars_for_template(self):
        legend_list = [j for j in range(5)]
        task_list = [j for j in range(Constants.letters_per_word)]
        task_width = 90 / Constants.letters_per_word
        return {'legend_list': legend_list,
                "round": self.round_number - 1, #Restar 1 al número de rondas. Ronda 0 = Práctica
                'task_list': task_list,
                'task_width': task_width,
                "payoff_A": "$"+format(int(str(Constants.payoff_A).split(",")[0]), ',d'),
                "payoff_B": "$"+format(int(str(Constants.payoff_B).split(",")[0]), ',d'),
                "contract_A": self.player.contract_A,
                }

class calculations1(WaitPage):
    wait_for_all_groups = True
    def after_all_players_arrive(self):
        self.subsession.set_ranking()
        self.subsession.set_ranking_groups()
        self.subsession.set_positions_players()

class calculations2(WaitPage):
    wait_for_all_groups = True
    def after_all_players_arrive(self):        
        self.subsession.set_tasks()
        self.subsession.set_winners_contract_A()
        self.subsession.set_contract_A_players()        
                
class results_practice(Page):
    def is_displayed(self):
        return self.round_number == 1
    def vars_for_template(self):
        return {
            "tasks": self.player.tasks,
            "round": self.round_number - 1,
        }

class results_tournament(Page):
    def is_displayed(self):
        return self.round_number > 1
    def vars_for_template(self):
        return {
            "discrimination" : self.session.config["discrimination"],
            "num_rounds" : Constants.num_rounds -1,
            "round": self.round_number - 1, #Restar 1 al número de rondas. Ronda 0 = Práctica
            "round_next": self.round_number,
            "tasks" : self.player.tasks,          
            "tasks_other":self.group.tasks_tournament - self.player.tasks,
            "tasks_p1" : self.group.tasks_p1,
            "tasks_p2" : self.group.tasks_p2,
            "tasks_p3" : self.group.tasks_p3,
            "tasks_p4" : self.group.tasks_p4,
            "payoff_round": "$"+format(int(str(self.player.payoff_round).split(",")[0]),',d'),
            "position_group": self.player.position_group,
            "contract_A": self.player.contract_A,
            "position_contract": self.player.position_contract,
            "position_ranking":self.player.position_ranking,
            "likelihood_contract_A_p2": "{0:.0f}%".format(self.group.likelihood_contract_A_p2*100),
            "likelihood_contract_A_p3": "{0:.0f}%".format(100-self.group.likelihood_contract_A_p2*100),
            "likelihood_contract_A_number": self.player.likelihood_contract_A,
            "likelihood_contract_A": "{0:.0f}%".format(self.player.likelihood_contract_A*100),
            "likelihood_contract_A_other": "{0:.0f}%".format(100-self.player.likelihood_contract_A*100),
            "contract_A_tournament" : self.player.contract_A_tournament
        }

class allocation(Page):
    def is_displayed(self):
        return self.round_number < Constants.num_rounds
    def vars_for_template(self): 
        return {
            "round": self.round_number,
            "contract_A_tournament" : self.player.contract_A_tournament,
        }

class wait_groups(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'creating_groups'
    def is_displayed(self):
        return self.round_number < Constants.num_rounds

class wait_payoff_total(WaitPage):
    wait_for_all_groups = True
    def after_all_players_arrive(self):
        self.subsession.set_payoff_players()
    def is_displayed(self):
        return self.round_number == Constants.num_rounds 

page_sequence = [
    device,
    wait_all, 
    consent,
	welcome, 
	instructions_practice,
    instructions_task,
    instructions_tournament,
    quiz,
    quiz_answer,
	task_practice,
    task_tournament,
    calculations1,
    calculations2,
    results_practice,
    results_tournament,
    allocation,
    wait_groups,
    wait_payoff_total,
]
