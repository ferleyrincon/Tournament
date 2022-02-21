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
import random

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'results'
    players_per_group = None
    num_rounds = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pago_total = models.CurrencyField()

    p_sex = models.IntegerField(
    choices=[
        [1, 'Hombre'],
        [2, 'Mujer'],
        [3, 'Otro'],
    ], label="2. ¿Cuál es su sexo?")
    p_age = models.IntegerField(label="3. Edad")
    p_student = models.IntegerField(
    choices=[
        [1, 'Sí'],
        [2, 'No'],
    ], label="4. ¿Es usted estudiante?")
    p_job = models.IntegerField(
    choices=[
        [1,'Solo estudio'],
        [2,'Desempleado'],
        [3,'Empleado a jornada completa'],
        [4,'Empleado a tiempo parcial'],
        [5,'Trabajador independiente'],
        [6,'Trabajador no remunerado (por ejemplo: ama de casa, empresa familiar)'],
        [7,'Retirado/pensionado'],
        [8,'Otro'],
        [9,'No sabe']
    ], label="5. ¿Cuál es su situación laboral actual?")
    p_educ = models.IntegerField(
    choices=[
        [1,'Ninguno'],
        [2,'Primaria'],
        [3,'Bachillerato'],
        [4,'Técnico o Tecnólogo'],
        [5,'Pregrado'],
        [6,'Posgrado (Especialización, Maestría, Doctorado)']
    ], label="6. ¿Cuál es el nivel educativo más alto que cursó o está cursando?")
    p_educ1 = models.IntegerField(label="7.¿Cuántos años de educación ha cursado en el nivel educativo que indicó previamente? (por ejemplo, si antes seleccionó Bachillerato debe escribir el número de años de Bachillerato que ha completado)")
    p_ocupation = models.StringField(label="8.Escriba el nombre de su profesión/ocupación/carrera")
    p_health = models.IntegerField(
    choices=[
        [1,'Subsidiado'],
        [2,'Contributivo (incluye regímenes especiales)']
    ], label="9. ¿A qué régimen de seguridad social en salud pertenece?")
    p_inc = models.IntegerField(
    choices=[
        [1,'Menos del Salario Mínimo Mensual (SMMLV)'],
        [2,'Entre 1 SMMLV - $ 1.500.000'],
        [3,'Entre $ 1.500.000 - $ 2.000.000'],
        [4,'Entre $ 2.000.000 - $ 4.000.000'],
        [5,'Mayor a $ 4.000.000'],
    ], label="10. ¿Cuál es el rango de su ingreso mensual?")
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

    p_pc = models.IntegerField(
    choices=[
        [1,'Portátil'],
        [2,'Equipo de escritorio']
    ], label="12. ¿Qué tipo de computador usó durante la actividad?")
    p_mouse = models.IntegerField(
    choices=[
        [1,'Sí (no incluye el mouse incorporado en el computador portátil).'],
        [2,'No']
    ], label="13. ¿Durante la actividad usted utilizó un “mouse/ratón” no incorporado al equipo?") 
    p_mouse1 = models.IntegerField(
    choices=[
        [1,'Bueno (funcionó adecuadamente).'],
        [2,'Regular (no funcionó bien en algunos momentos)'],
        [3,'Malo (dejó de funcionar en algún momento)'],
    ], label="14. ¿Cómo califica el funcionamiento del “mouse/ratón” que usó durante la actividad?") 
    p_wifi = models.IntegerField(
    choices=[
        [1,'Bueno (funcionó adecuadamente).'],
        [2,'Regular (no funcionó bien en algunos momentos)'],
        [3,'Malo (dejó de funcionar en algún momento)'],
    ], label="15. ¿Cómo califica el funcionamiento de su conexión a internet durante la actividad?") 

    pnorm_1 = models.PositiveIntegerField(choices=[1,2,3,4,5],
                                       widget=widgets.RadioSelectHorizontal(),
                                       verbose_name="Es justo que el talento determine los ingresos de una persona."
                                       )
    pnorm_2 = models.PositiveIntegerField(choices=[1,2,3,4,5],
                                       widget=widgets.RadioSelectHorizontal(),
                                       verbose_name="Es justo que la suerte determine los ingresos de una persona. "
                                       )
    pnorm_3 = models.PositiveIntegerField(choices=[1,2,3,4,5],
                                       widget=widgets.RadioSelectHorizontal(),
                                       verbose_name="Es justo que el esfuerzo determine los ingresos de una persona."
                                       )
    p_emp = models.PositiveIntegerField(choices=[1,2,3,4],
                                       widget=widgets.RadioSelectHorizontal(),
                                       verbose_name="En nuestra sociedad, tipicamente las personas con ingresos más altos se esfuerzan más que las personas con ingresos más bajos."
                                       )
    p_pension = models.IntegerField(
    choices=[
        [1,'Aportando en un fondo de pensiones obligatorias'],
        [2,'Aportando en un fondo de pensiones voluntarias (por ejemplo, BEPS)'],
        [3,'Ahorrando'],
        [4,'Haciendo inversiones'],
        [5,'Pagando un seguro por su cuenta'],
        [6,'Preparando a sus hijos para que puedan ayudarlo en su vejez'],
        [7,'Nada'],
    ], label="¿Qué está haciendo usted actualmente para mantenerse económicamente en su vejez?")

    p_pension2 = models.IntegerField(
    choices=[
        [1,'Aportando en un fondo de pensiones obligatorias'],
        [2,'Aportando en un fondo de pensiones voluntarias (por ejemplo, BEPS)'],
        [3,'Ahorrando'],
        [4,'Haciendo inversiones'],
        [5,'Pagando un seguro por su cuenta'],
        [6,'Preparando a los hijos para que puedan ayudarlos en su vejez'],
        [7,'Nada'],
    ], label="11. ¿Qué están haciendo (hicieron) sus padres para mantenerse económicamente en la vejez?")

    def payoff_complete(self):
        self.pago_total =  self.participant.vars['payoff_complete']+(self.participant.vars["icl_pago"]*100)