import math
from numpy import log as ln
import matplotlib.pyplot as plt

time_values = []
y_values = []
pressure_values = []

ambient_pressure = 101000
pin = 40000 + ambient_pressure

T = 300  # Temperature
n = 0.3863  # amount of particles
R = 8.1345  # Ideal gas constant
delta_p_0 = pin-ambient_pressure
rho = (pin)/(R*T)
#rho = 1.22
print('rho: {}'.format(rho))

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
leakage_rates = []

for index in range(len(time_values)):
    time_value = float(time_values[index])
    pressure_value = float(pressure_values[index]) + ambient_pressure

    print('time value: {}, pressure value: {}'.format(time_value, pressure_value))

    # Calculate tau first
    #tau = time_value / (-ln(pin / pressure_value))
    tau = -time_value / (ln((pressure_value - ambient_pressure) / (pin - ambient_pressure)))
    print('tau is: {}'.format(tau))

    # Calculate the leakage area
    #leakage_rate = (n*R*T / tau) / (pin * math.sqrt((2/rho) * (pin - ambient_pressure)))
    leakage_rate = ((n * R * T) / (pin ** 2 * tau)) * (pin - ambient_pressure) / (math.sqrt((2 / rho) * (pin - ambient_pressure)))
    leakage_rates.append(leakage_rate)
    total_leakage += leakage_rate
    print('Leakage rate for index {} is {}'.format(index, leakage_rate))

print('Average leakage rate is {} m2'.format(total_leakage / len(time_values)))
print('Median leakage rate: {}'.format(leakage_rates[int(len(leakage_rates) / 2)]))

plt.plot(time_values, pressure_values)
plt.xlabel('Time (seconds)')
plt.ylabel('Air pressure (kPa)')
plt.show()

plt.scatter(time_values, leakage_rates, marker="x")
plt.plot(time_values, [total_leakage / len(time_values)] * len(time_values))
plt.xlabel('Time (seconds)')
plt.ylabel('Leakage hole (m2)')
plt.show()