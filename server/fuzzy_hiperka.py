from __future__ import absolute_import
import numpy as np
import time
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# New Antecedent/Consequent objects hold universe variables and membership
# functions
hearthr = ctrl.Antecedent(np.arange(0, 201, 1), 'hearthr')
hiperka = ctrl.Antecedent(np.arange(5, 10, 0.5), 'hiperka')

#import pdb;pdb.set_trace()
alarm = ctrl.Consequent(np.arange(0, 101, 1), 'alarm')

#hearthr['brady'] = fuzz.trimf(hearthr.universe, [-1000, 400, 60])
hearthr['brady'] = fuzz.trapmf(hearthr.universe, [-1000,-400, 40, 60])
hearthr['normo'] = fuzz.trapmf(hearthr.universe, [30,60,100,130])
hearthr['tachy'] = fuzz.trapmf(hearthr.universe, [100, 120, 400,1000])

hiperka['moderate'] = fuzz.trapmf(hiperka.universe, [6, 6.5, 7.5,8])
hiperka['severe'] = fuzz.trapmf(hiperka.universe, [7.5, 8, 100,1000])



alarm['alarm_brady'] = fuzz.trimf(alarm.universe, [0, 0, 50])
alarm['no_alarm'] = fuzz.trimf(alarm.universe, [0, 50, 100])
alarm['alarm_tachy'] = fuzz.trimf(alarm.universe, [50, 100, 101])
'''hearthr.view()
alarm.view()
raw_input("Press Enter to continue...")'''

rule1 = ctrl.Rule(hearthr['brady'], alarm['alarm_brady'])
rule2 = ctrl.Rule(hearthr['normo'], alarm['no_alarm'])
rule3 = ctrl.Rule(hearthr['tachy'] | hiperka['severe'], alarm['alarm_tachy'])

#rule1.view()
#raw_input("Press Enter to continue...")
tipping_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
tipping = ctrl.ControlSystemSimulation(tipping_ctrl)
#grafiquito de la logica difusa
#hearthr.view()
input("Press Enter to continue...")

def fuzzy_logic_hiperka(contador):
    tipping.input['hiperka'] = 7.6
    tipping.input['hearthr'] = contador
    tipping.compute()
    print ("Porcentaje :")
    print (tipping.output['alarm'])

