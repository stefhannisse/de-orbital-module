import math
import matplotlib.pyplot as plt
import numpy as np

p_ideal_list = []
p_leak_list = []
t_list = []

ambient_pressure_space = 0
p_in_space = 60000

n = 0.3863
R = 8.1345

A = 1.1507593680620897e-06
t0 = 0
t = t0
dt = 1

temperature = 125 #Temperature in degrees
length_beam = 0.35 #In meters
radius_beam = 16 #In millimeters
pressure_beam = 60000 #In kPa
density_gas = 0.00196
molecular_mass = 0.044

timeShown = False

def convertCtoKelvin(temp):
    return temp + 273.15

if __name__ == '__main__':
    volume_beam = math.pi*((radius_beam/1000)**2)*length_beam
    number_of_moles = (pressure_beam * volume_beam) / (8.1345 * convertCtoKelvin(temperature))
    print('moles: {}'.format(number_of_moles))

    mass_gas = molecular_mass * number_of_moles
    volume_gas = mass_gas / density_gas

    print('Needed volume: {}'.format(volume_gas))

    #At -65: 0.223 L, at 125: 0.117 L
    #Calculate the temperature delta over time
    #Temperature difference of 190 degrees is observed in 90 minutes

    loop = True
    t = 0
    dt = 1
    T = convertCtoKelvin(125)
    circumference_orbit = 2 * math.pi * 6903000
    speed_orbit = 7598.88  # Speed in m/s

    while loop:
        #Calculate the temperature at this timestamp, considering the temperature curve is linear
        #2*pi*r

        #Calculate the circumference of the orbit
        if t < ((95.13 * 60) / 2):
            T_current = convertCtoKelvin(125) - ((speed_orbit * t / (circumference_orbit / 2)) * 190)
        else:
            # = 208.15 +
            T_current = convertCtoKelvin(-65) + ((speed_orbit * (t - 2854) / (circumference_orbit / 2)) * 190)

        #Calculate pressure over temperature difference
        P = (number_of_moles * 8.1345 * t) / volume_beam

        #Calculate the pressure at this temperature
        p_in = number_of_moles * 8.1345 * T_current / volume_beam
        #print('t={} T={} p={}'.format(t, T_current, p_in))

        rho = p_in / (R * T)

        p_space = ambient_pressure_space + (p_in_space - ambient_pressure_space) * np.exp(
            (((-t * p_in_space * A) / (n * R * T)) * math.sqrt((2 / rho) * (p_in_space - ambient_pressure_space))))

        if p_space < 54100 and not timeShown:
            timeShown = True
            print('Tijd onder 54.1 kpa: {}'.format(t))

        t_list.append(t)
        p_ideal_list.append(p_in)
        p_leak_list.append(p_space)

        if(t > (95.13 * 60)):
            loop = False

        t = t + dt

plt.plot(t_list, p_ideal_list)
plt.xlabel('Time (seconds)')
plt.ylabel('Pressure (Pa)')
#plt.plot(t_list, delta_p_list_space)
plt.show()

plt.plot(t_list, p_leak_list)
plt.xlabel('Time (seconds)')
plt.ylabel('Pressure (Pa)')
#plt.plot(t_list, delta_p_list_space)
plt.show()