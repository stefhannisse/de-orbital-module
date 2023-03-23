import math as m
import matplotlib.pyplot as plt
import numpy as np

delta_p_list = []
delta_p_list_2 = []
t_list = []
t_list_2 = []
p_out = 0.01

p_in = 40000 #Pressure
p_in_2 = 15000 #Pressure
V_i = 0.02356 #Volume
T = 300 #temperature
n = 0.3863 #amount of particles
n_2 = 0.1449 #Amount of molls
R = 8.1345 #Ideal gas constant

rho = p_in/(R*T)
rho_2 = p_in_2/(R*T)
A = float(input("Enter the area of the leakage hole: "))
t0 = 0
t = t0
dt = 10

delta_p_0 = p_in-p_out
delta_p_0_2 = p_in_2-p_out

tau = (n*R*T)/((p_in*A*((2/rho)*delta_p_0)**(0.5)))
tau_2 = (n_2*R*T)/((p_in_2*A*((2/rho_2)*delta_p_0_2)**(0.5)))
Loop = True

while Loop == True:
    delta_p = p_in*np.exp(-(t/tau))
    print(delta_p)
    t_list.append(t/3600)
    delta_p_list.append(delta_p)
    t = t + dt

    if delta_p < 1000:
        Loop = False

    t_2 = t0
    Loop_2 = True

    while Loop_2 == True:
        delta_p_2 = p_in_2*np.exp(-(t_2/tau_2))
        t_list_2.append((t_2)/3600)
        delta_p_list_2.append(delta_p_2)
        t_2 = t_2 + dt
        if delta_p_2 < 1000:
            Loop_2 = False

print(t-t_2)
plt.plot(t_list, delta_p_list)
plt.plot(t_list_2, delta_p_list_2)
plt.show()
