import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

# Membuat FIS
density = ctrl.Antecedent(np.arange(0, 501, 1), 'density')
distance = ctrl.Antecedent(np.arange(0, 11, 1), 'distance')
speed = ctrl.Consequent(np.arange(0, 61, 1), 'speed')

# Menentukan fungsi keanggotaan
density['low'] = fuzz.trimf(density.universe, [0, 0, 250])
density['medium'] = fuzz.trimf(density.universe, [0, 250, 500])
density['high'] = fuzz.trimf(density.universe, [250, 500, 500])

distance['close'] = fuzz.trimf(distance.universe, [0, 0, 5])
distance['medium'] = fuzz.trimf(distance.universe, [0, 5, 10])
distance['far'] = fuzz.trimf(distance.universe, [5, 10, 10])

speed['slow'] = fuzz.trimf(speed.universe, [0, 0, 30])
speed['medium'] = fuzz.trimf(speed.universe, [0, 30, 60])
speed['fast'] = fuzz.trimf(speed.universe, [30, 60, 60])

# Membuat aturan inferensi
rule1 = ctrl.Rule(density['low'] & distance['close'], speed['slow'])
rule2 = ctrl.Rule(density['medium'] | distance['medium'], speed['medium'])
rule3 = ctrl.Rule(density['high'] & distance['far'], speed['fast'])

# Menggabungkan aturan ke dalam kontrol sistem
speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])

# Membuat simulasi kontrol sistem
vehicle_speed = ctrl.ControlSystemSimulation(speed_ctrl)

# Visualisasi fungsi keanggotaan
density.view()
distance.view()
speed.view()

# Menampilkan aturan inferensi
rule1.view()
rule2.view()
rule3.view()

# Menampilkan grafik
plt.show()
