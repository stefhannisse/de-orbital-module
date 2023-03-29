import math
from matplotlib import pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D, axes3d
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import numpy as np
import pandas as pd
import matplotlib as mat

A4 = 1.14e-10
B4 = -2.13e-7
C4 = 1.57e-4
D4 = -7.03e-2
E4 = -1.29e1

A6 = 8.11e-12
B6 = -2.36e-9
C6 = -2.64e-6
D6 = -1.56e-2
E6 = -2.00e1

A2 = 1.19e-9
B2 = -1.45e-6
C2 = 6.91e-4
D2 = -1.74e-1
E2 = -5.32

mu = 3.986e14

surpassed_450 = False
surpassed_450_sat = False
prop = False
printmonth = True



def semimajor_axis(rad, vel):
    mu = 3.986e14
    a = ((2/rad)-(vel**2/mu))**(-1)
    return a

def eccentricity(rad, a):
    eccen = (rad/a)-1
    return eccen

def semiminor_axis(a, eccen):
    b = math.sqrt((a**2)*(1-(eccen**2)))
    return b

def period(a):
    mu = 3.986e14
    T = 2*math.pi*math.sqrt((a**3)/mu)
    return T

def angular_rate(a, b, T, rad):
    om = (2*math.pi*a*b)/((rad**2)*T)
    return om

def pos_ellipt(angle, eccen, a):
    radius = (a*(1-(eccen**2)))/(1+(eccen*math.cos(angle)))
    return radius

def drag_200_300(z, v, A, Cd, m):
    dens = math.exp((A2*z**4)+(B2*z**3)+(C2*z**2)+(D2*z)+E2)
    D = Cd*0.5*dens*(v**2)*A
    deceleration = D/m
    return deceleration, D

def drag_450_500(z, v, A, Cd, m):
    dens = math.exp((A4*z**4)+(B4*z**3)+(C4*z**2)+(D4*z)+E4)
    D = Cd*0.5*dens*(v**2)*A
    deceleration = D/m
    return deceleration, D

def drag_500_650(z, v, A, Cd, m):
    dens = math.exp((A6*z**4)+(B6*z**3)+(C6*z**2)+(D6*z)+E6)
    D = Cd*0.5*dens*(v**2)*A
    deceleration = D/m
    return deceleration, D

def new_vel(rad, a):
    mu = 3.986e14
    v = math.sqrt(mu*((2/rad)-(1/a)))
    return v

def decel_vel(v, z, A, Cd, m, dt):
    if z > 500:
        decel, D = drag_500_650(z, v, A, Cd, m)
    elif z <=500 and z > 300:
        decel, D = drag_450_500(z, v, A, Cd, m)
    elif z <= 300:
        decel, D = drag_200_300(z, v, A, Cd, m)
    v = v - decel*dt
    return v, D

def epoch(r, v, t, dt, A, Cd, m, angle, r_E):
    r_m = r*1000
    a = semimajor_axis(r_m, v)
    e = eccentricity(r_m, a)
    b = semiminor_axis(a, e)
    T = period(a)
    om = angular_rate(a, b, T, r_m)
    angle = angle + om*dt
    if angle > 2*math.pi:
        angle = angle - 2*math.pi
    r_m = pos_ellipt(angle, e, a)
    r = r_m/1000
    v = new_vel(r_m, a)
    z = r-r_E
    v, D = decel_vel(v, z, A, Cd, m, dt)
    t += dt
    return v, r, t, z, angle

def one_sim(z, r, t, dt, A, Cd, m, angle, v, r_E):
    low_limitm = 200
    while z > low_limitm:
        #print(z)
        v, r, t, z, angle = epoch(r, v, t, dt, A, Cd, m, angle, r_E)
    return(t)

def style_cell(x, r, c, color):
    styler = pd.DataFrame("", index=x.index, columns=x.columns)
    styler.iloc[r, c] = color
    return styler


z0 = float(input("Enter the initial orbital altitude in km: "))

shapechoice = int(input("Enter which the shape you want to simulate (1=Sphere,  2=Sail (flat plate)): "))

mass = float(input("Enter the mass of the satellite in kg: "))

area = float(input("Enter the area of the satellite in m^2: "))

if shapechoice == 1:
    Cd = 2.05
    shape = "Sphere"
elif shapechoice == 2:
    Cd = 1.325158
    shape = "Sail"
else:
    print("ERROR: You didn't input one of the shapes available")
    exit()

print("-------------------------------------------------------------------")

Cd_sat = 1.66514

increase_factor = 1.562282

t0 = 0
angle0 = 0
mode = "w"

z = z0
t = t0
angle = angle0
r_E = 6378
r = z + r_E
v_init = math.sqrt(mu/(r*1000))
v = v_init
dt = 3600
CD_ratio = Cd_sat/Cd

Time_uninf = one_sim(z, r, t, dt, area, Cd_sat, mass, angle, v, r_E)
t_years = Time_uninf/(3600*24*365.25)
print("Uninflated time is: "+str(t_years)+" years.")

if t_years >= 50:
    A_increase_factor = (t_years/10)*CD_ratio
    A_needed = area*A_increase_factor*increase_factor
elif t_years < 50:
    A_needed = CD_ratio*5*area*increase_factor

t = t0
angle = angle0
r_E = 6378
r = z + r_E
v_init = math.sqrt(mu/(r*1000))
v = v_init

t_solved = one_sim(z, r, t, dt, A_needed/increase_factor, Cd, mass, angle, v, r_E)
t_solved_years = t_solved/(3600*24*365.25)

print("Inflated time is: "+str(t_solved_years)+" years.")

print("Area for the sail needed is: "+str(A_needed)+" m^2.")

print("Which corresponds to the sides being {} m long.".format(math.sqrt(A_needed)))

inflatesail_boom_area = 0.006361725
Boom_area_decrease_factor = 4
inflatesail_area = 10
Boom_inclination_angle = np.pi/6

Boom_area = (inflatesail_boom_area/Boom_area_decrease_factor)*(A_needed/inflatesail_area)
Boom_diameter = 2*np.sqrt(Boom_area/np.pi)
boom_length_1 = ((0.5*np.sqrt(A_needed))/np.sin(np.pi/4))/np.cos(Boom_inclination_angle)

print("Boom diameter is: "+str(Boom_diameter*100)+" cm.")
print("Length of 1 boom is: "+str(boom_length_1*100)+" cm.")

exit()