import math
import math as m
import matplotlib.pyplot as plt
import numpy as np

delta_p_list = []
delta_p_list_space = []
t_list = []

ambient_pressure_space = 0
ambient_pressure = 101000
p_in = 40000 + ambient_pressure
p_in_space = 60000

T = 300
n = 0.3863
R = 8.1345

rho = p_in/(R*T)
#rho = 1.22
#A = float(input("Enter the area of the leakage hole: "))
A = 1.6587619393101267e-06
t0 = 0
t = t0
dt = 1

delta_p_0 = p_in-ambient_pressure
delta_p_0_2 = p_in - 0

#tau = (n * R * T) / (p_in * A * math.sqrt((2 / rho) * (p_in - ambient_pressure)))
tau = ((n * R * T) / (p_in**2 * A)) * (p_in - ambient_pressure) / (math.sqrt((2 / rho) * (p_in - ambient_pressure)))
print('tau is: {}'.format(tau))
tau_space = (n*R*T) / (p_in * A * math.sqrt((2/rho)*(p_in - ambient_pressure_space)))
print('tau space: {}'.format(tau_space))
Loop = True

while Loop == True:
    p = ambient_pressure + (p_in - ambient_pressure) * np.exp((((-t*p_in*A) / (n*R*T)) * math.sqrt((2/rho)*(p_in - ambient_pressure))))
    p_space = ambient_pressure_space + (p_in_space - ambient_pressure_space) * np.exp(
        (((-t * p_in_space * A) / (n * R * T)) * math.sqrt((2 / rho) * (p_in_space - ambient_pressure_space))))
    #p = p_in*np.exp((((-t*p_in*A) / (n*R*T)) * math.sqrt((2/rho)*(p_in - ambient_pressure))))
    #print('pressure for t is {}'.format(p))
    #print(delta_p)
    t_list.append(t)
    delta_p_list.append(p - ambient_pressure)
    delta_p_list_space.append(p_space - ambient_pressure_space)
    t = t + dt

    if(p_space < 54100):
        print('lower than regidization pressure at t={}'.format(t))
    # if p < (1000 + ambient_pressure):
    #     Loop = False
    if p_space < (1000 + ambient_pressure_space):
        Loop = False

    t_2 = t0
    Loop_2 = True

# print('Continuing to the second loop')
# Loop = True
# t = t0
#
# while Loop == True:
#     delta_p_2 = p_in*np.exp(-(t/tau_space))
#     delta_p_list_space.append(delta_p_2)
#     t = t + dt
#     if delta_p_2 < (1000 + ambient_pressure_space):
#         Loop = False

plt.plot(t_list, delta_p_list_space)
plt.xlabel('Time (seconds)')
plt.ylabel('Pressure (Pa)')
#plt.plot(t_list, delta_p_list_space)
plt.show()
