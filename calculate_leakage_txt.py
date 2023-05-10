import math
from numpy import log as ln

time_values = []
y_values = []
pressure_values = []

ambient_pressure = 101000
pin = 40000 + ambient_pressure

T = 300  # Temperature
n = 0.3863  # amount of particles
R = 8.1345  # Ideal gas constant
delta_p_0 = pin-ambient_pressure
rho = pin/(R*T)

with open('leaking_values.txt', 'r') as f:
    for line in f.readlines():
        if(line.find('e') == -1):
            area_hole = float(line[:line.find('-')])
        else:
            area_hole = float(line[:line.find('-', line.find('-') + 1)])

        line = line.replace(str(area_hole), '')
        y_values.append(area_hole)

        time = line[::-1]
        time = time[:time.find('-')]
        time = float(time[::-1])

        time_values.append(time)
        line = line.replace(str(time), '')

        pressure_values.append(float(line[1:-2]))

if len(time_values) != len(pressure_values):
    print('The amount of time readings and pressure readings are not the same, aborting')
    exit()

total_leakage = 0
for index in range(len(time_values)):
    time_value = float(time_values[index]) + ambient_pressure
    pressure_value = float(pressure_values[index]) + ambient_pressure

    # Calculate tau first
    #tau = time_value / (-ln(pin / pressure_value))
    tau = time_value / (-ln(pressure_value / pin))
    print('tau is: {}'.format(tau))

    # Calculate the leakage area
    leakage_rate = (n*R*T / tau) / (pin * math.sqrt((2/rho) * (pin - ambient_pressure)))
    total_leakage += leakage_rate
    print('Leakage rate for index {} is {}'.format(index, leakage_rate))

print('Average leakage rate is {} m2'.format(total_leakage / len(time_values)))
#5.917925927471826e-10