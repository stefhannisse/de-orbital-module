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

T = 300
n = 0.3863
R = 8.1345

rho = p_in/(R*T)

#A = float(input("Enter the area of the leakage hole: "))
A = 5.917925927471826e-10
t0 = 0
t = t0
dt = 10

delta_p_0 = p_in-ambient_pressure
delta_p_0_2 = p_in - 0

tau = (n * R * T) / (p_in * A * math.sqrt((2 / rho) * (p_in - ambient_pressure)))
print('tau is: {}'.format(tau))
tau_space = (n*R*T) / (p_in * A * math.sqrt((2/rho)*(p_in - ambient_pressure_space)))
Loop = True

while Loop == True:
    p = p_in*np.exp(((-t*p_in*A) / (n*R*T)) * math.sqrt((2/rho)*(p_in - ambient_pressure)))
    print('pressure for t is {}'.format(p))
    #print(delta_p)
    t_list.append(t)
    delta_p_list.append(p)
    t = t + dt

    if p < (1000 + ambient_pressure):
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

plt.plot(t_list, delta_p_list)
#plt.plot(t_list, delta_p_list_space)
plt.show()
