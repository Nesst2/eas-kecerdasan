from flask import Flask, render_template, request, jsonify
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

app = Flask(__name__)

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

rule1 = ctrl.Rule(density['low'] & distance['close'], speed['slow'])
rule2 = ctrl.Rule(density['medium'] | distance['medium'], speed['medium'])
rule3 = ctrl.Rule(density['high'] & distance['far'], speed['fast'])

speed_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
vehicle_speed = ctrl.ControlSystemSimulation(speed_ctrl)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/calculate_speed', methods=['POST'])
def calculate_speed():
    data = request.get_json()
    density_value = float(data['density'])
    distance_value = float(data['distance'])

    vehicle_speed.input['density'] = density_value
    vehicle_speed.input['distance'] = distance_value
    vehicle_speed.compute()

    speed_value = vehicle_speed.output['speed']

    response = {'speed': speed_value}
    return jsonify(response)

if __name__ == '__main__':
    app.run()
