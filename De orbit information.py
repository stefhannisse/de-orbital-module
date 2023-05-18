import math
from matplotlib import pyplot as plt
import numpy as np

#Constants for the polynomials used to compute the density at different points in altitude.

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

mu = 3.986e14 #Gravitational parameter of Earth

surpassed_450 = False #Indicator that a satellite has gone lower than an orbital altitude of 450 km
surpassed_450_sat = False #Indicator that a satellite has gone lower than an orbital altitude of 450 km for a satellite without inflatable
prop = False
printmonth = True

#Setting up the lists which will be used for plotting or testing.

r_list = []
t_list = []
t_list_days = []
t_list_days_unit = []
z_list = []
z_list_days_unit = []
z_diff_list = []
F_list = []
e_list = []
angle_list = []
P_list = []
v_list = []

r_list_sat = []
t_list_sat = []
t_list_days_sat = []
z_list_sat = []
F_list_sat = []
e_list_sat = []
angle_list_sat = []

#Input values, their message has their meaning

#z0 = int(input("Enter starting altitude in km. "))
z0 = 525
#m = float(input("Enter mass in kg. "))
m = 12
#Area_sat_q = str(input("Personalised satellite area? (y/n) "))
#if Area_sat_q == "y":
#    A_sat = float(input("Enter the area of the satellite. "))
A_sat = 0.02
#Area_q = str(input("Personalised inflatable area? (y/n) "))
#if Area_q == "y":
    #A = float(input("Enter the area of the inflatable object. "))
A = 0.2
#CdChoice = int(input("Choose the drag coefficient. 1.Sphere(0.47) 2.Cone(0.50) 3.Cube(1.05) 4.Wall(1.17) 5.Semisphere(1.17) 6.Parachute(1.42) 7.Manual "))

#Drag coefficient assuming continous flow, do not use for regular de-orbits anymore, only the manual one (for a flat plate, Cd=1.325158).

CdChoice = 0
if CdChoice == 1:
    Cd = 0.47
elif CdChoice == 2:
    Cd = 0.5
elif CdChoice == 3:
    Cd = 1.05
elif CdChoice == 4 or CdChoice == 5:
    Cd = 1.17
elif CdChoice == 6:
    Cd = 1.42
elif CdChoice == 7:
    Cd = float(input("Enter the drag coefficient "))

Cd = 1.325158
Cd_sat = 1.66514 #Satellite body drag coefficient

#If the satellite area is not personalised, it will be extrapolated from the satellite database.

#f Area_sat_q == "n":
    #A_sat = 0.009*m
#if Area_q == "y":
if A < A_sat:
    prop = True
    A = A_sat

#If area is not personalised, it will use this old equation to determine its area. Now that we are using two separate equations for 10 years limmit and 5 times faster, this is no longer needed

# if Area_q == "n":
#     A = ((0.0123*z0)-0.535)*A_sat*(Cd_sat/Cd)

print("")
print("-------------------")
print("")

#A simple output to show the area ratio and the boom dimensions

print("Area of the satellite is", A_sat, "m^2. Area of device is", A, "m^2.", A/A_sat, "times larger.")
if prop == True:
    print("Area taken for calculation is thus ", A_sat, "m^2")

Lateral = math.sqrt(A)
boom_length = 0.5*Lateral/math.cos(math.pi/4)
print("Boom length is", boom_length, "m.")

r_E = 6378 #Earth radius in km
r0 = z0 + r_E #Initial orbit radius
r = r0 #Radius of orbit (changes in time)
r_sat = r0 #Radius of orbit for a satellite iwthout inflatable (changes in time)
z = z0 #Altitude of orbit (changes in time)
z_sat = z0 #Altitude of orbit for a satellite without inflatable (changes in time)

in_vel = math.sqrt(mu/(r0*1000)) #Initial orbital velocity
v = in_vel #Orbital velocity (changes in time)
v_sat = in_vel #Orbital velocity for a satellite without inflatable (changes in time)

t = 0 #Time variable
t_sat = 0 #Time variable for a satellite without inflatable
dt = 600 #Time beetween epochs
dt_sat = 3600 #Time between epochs for a satellite without inflatable
angle = 0 #Angle within an ellyptical orbit
angle_sat = 0 #Angle within an ellyptical orbit for a satellite without inflatable

#Appending the first values to the lists

r_list.append(r)
t_list.append(t/3600)
t_list_days.append((t/3600)/24)
z_list.append(z)
angle_list.append(angle)
v_list.append(v)

r_list_sat.append(r)
t_list_sat.append(t/3600)
t_list_days_sat.append((t/3600)/24)
z_list_sat.append(z)
angle_list_sat.append(angle_list_sat)

def semimajor_axis(rad, vel): #Computes the semi-major axis of an ellyptical orbit
    mu = 3.986e14
    a = ((2/rad)-(vel**2/mu))**(-1)
    return a

def eccentricity(rad, a): #Computes the eccentricity of the orbit
    eccen = (rad/a)-1
    return eccen

def semiminor_axis(a, eccen): #Computes the sami-minor axis of the orbit
    b = math.sqrt((a**2)*(1-(eccen**2)))
    return b

def period(a): #Computes the time period it takes to perform a full orbit
    mu = 3.986e14
    T = 2*math.pi*math.sqrt((a**3)/mu)
    return T

def angular_rate(a, b, T, rad): #Computes the angiular rate within an orbit of the satellite
    om = (2*math.pi*a*b)/((rad**2)*T)
    return om

def pos_ellipt(angle, eccen, a): #Computes the new radius after an epoch
    radius = (a*(1-(eccen**2)))/(1+(eccen*math.cos(angle)))
    return radius

def drag_200_300(z, v, A, Cd, m): #Computes drag between 200km and 300 km altitude
    dens = math.exp((A2*z**4)+(B2*z**3)+(C2*z**2)+(D2*z)+E2) #Density according to 1979 US standard atmosphere for this altitude range
    D = Cd*0.5*dens*(v**2)*A #Drag computed from a simple drag equation
    deceleration = D/m #acceleration = force / mass
    return deceleration, D

def drag_450_500(z, v, A, Cd, m): #Computes the drag between 300km and 500km altitude
    dens = math.exp((A4*z**4)+(B4*z**3)+(C4*z**2)+(D4*z)+E4) #Density according to 1979 US standard atmosphere for this altitude range
    D = Cd*0.5*dens*(v**2)*A #Drag computed from a simple drag equation
    deceleration = D/m #acceleration = force / mass
    return deceleration, D

def drag_500_650(z, v, A, Cd, m): #Compute sthe drag between 500km and 650km altitude
    dens = math.exp((A6*z**4)+(B6*z**3)+(C6*z**2)+(D6*z)+E6) #Density according to 1979 US standard atmosphere for this altitude range
    D = Cd*0.5*dens*(v**2)*A #Drag computed from a simple drag equation
    deceleration = D/m #acceleration = force / mass
    return deceleration, D

def new_vel(rad, a): #Computes the new velocity from the elliptical orbit
    mu = 3.986e14
    v = math.sqrt(mu*((2/rad)-(1/a)))
    return v

def decel_vel(v, z, A, Cd, m, dt): #A function simply to manage different drag altitudes and return the velocity after the new epoch
    if z > 500:
        decel, D = drag_500_650(z, v, A, Cd, m)
    elif z <=500 and z > 300:
        decel, D = drag_450_500(z, v, A, Cd, m)
    elif z <= 300:
        decel, D = drag_200_300(z, v, A, Cd, m)
    v = v - decel*dt
    return v, D

def epoch(r, v, t, dt, A, Cd, m, angle): #Funciton to compute each epoch within the de-orbit
    r_m = r*1000 #Make sure the radius is in meters instead of km
    a = semimajor_axis(r_m, v)
    e = eccentricity(r_m, a)
    b = semiminor_axis(a, e)
    T = period(a)
    om = angular_rate(a, b, T, r_m)
    angle = angle + om*dt #Computing the angle change in the orbit
    if angle > 2*math.pi: #Making sure if it goes full circle, it does not exceed 360 degreees, instead goes back from 0 degrees
        angle = angle - 2*math.pi
    r_m = pos_ellipt(angle, e, a)
    r = r_m/1000
    v = new_vel(r_m, a)
    z = r-r_E
    v, D = decel_vel(v, z, A, Cd, m, dt)
    t += dt #advancement in time from the epoch.
    return v, r, t, z, D, e, angle, T

low_limitm = 200 #Limit altitude at which the de-orbit is considered finished in km.

while z > low_limitm:
    if printmonth == True:#Funciton simply to print each month or year of the de-orbit, can be deactivated
        if t % (3600*24*30*12) == 0:
            print("Dragged Orbit, Year", t/(3600*24*30*12))
    v, r, t, z, D, e, angle, P = epoch(r, v, t, dt, A, Cd, m, angle) #computation of 1 epoch
    if surpassed_450 == False and z < 450: #If statement to record the time in which the satellite surpasses 450km, our operational limit altitude
        t_450 = (t/3600)/24
        surpassed_450 = True

    #Appending values into the lists each epoch

    r_list.append(r)
    t_list.append(t/3600)
    t_list_days.append((t/3600)/24)
    z_list.append(z)
    F_list.append(D)
    e_list.append(e)
    angle_list.append(angle)
    P_list.append(P/3600)
    v_list.append(v)

print("----------------------------")

while z_sat > low_limitm: #Same process is done but for a satellite without an inflatable
    if printmonth == True:
        if t_sat % (3600*24*30*12) == 0:
            print("Regular Orbit, Year", t_sat/(30*3600*24*12))
    v_sat, r_sat, t_sat, z_sat, D_sat, e_sat, angle_sat, P_sat = epoch(r_sat, v_sat, t_sat, dt_sat, A_sat, Cd_sat, m, angle_sat)
    if surpassed_450_sat == False and z_sat < 450:
        t_450_sat = (t_sat/3600)/24
        surpassed_450_sat = True
    r_list_sat.append(r_sat)
    t_list_sat.append(t_sat/3600)
    t_list_days_sat.append((t_sat/3600)/24)
    z_list_sat.append(z_sat)
    F_list_sat.append(D)
    e_list_sat.append(e_sat)
    angle_list_sat.append(angle_sat)

for i in range(len(t_list)):
    if t_list[i] % 24 == 0:
        t_list_days_unit.append(t_list[i]/24)
        z_list_days_unit.append(z_list[i])
z_diff_list.append(0)
for i in range(1, len(z_list_days_unit)):
    z_diff = z_list_days_unit[i] - z_list_days_unit[i-1]
    z_diff_list.append(abs(z_diff))

#Process to be able to graph the de-orbit in 2 dimensions

xlist = []
ylist = []
xzlist = []
yzlist = []
for i in range(len(t_list)):
    x = r_list[i]*math.cos(angle_list[i])
    y = r_list[i]*math.sin(angle_list[i])
    xz = z_list[i]*math.cos(angle_list[i])
    yz = z_list[i]*math.sin(angle_list[i])
    xlist.append(x)
    ylist.append(y)
    xzlist.append(xz)
    yzlist.append(yz)

circ_an = np.linspace(0, 2*math.pi, 150)
circ_radius = 6378
circ_x = []
circ_y = []
for i in range(len(circ_an)):
    circ_x.append(circ_radius*math.cos(circ_an[i]))
    circ_y.append(circ_radius*math.sin(circ_an[i]))

#Output of data to be able to test.

print("")
print("De-orbit time without device is", t_list_days_sat[-1], "days (", t_list_days_sat[-1]/365, "years). De-orbit time with device is", t_list_days[-1], "days. (", t_list_days[-1]/365, "years).")
print("De-orbit time is", t_list_days_sat[-1]/t_list_days[-1], "times faster with the de-orbiting device.")
print("")
print("450 km time without device is", t_450_sat, "days (", t_450_sat/365, "years). 450 km time with device is", t_450, "days (", t_450/365, "years).")
print("450 km time is", t_450_sat/t_450, "times faster with the de-orbiting device.")

#De-orbit altitude graph plot

plt.plot(t_list_days, z_list, label="with inflatable")
plt.plot(t_list_days_sat, z_list_sat, label="without inflatable")
plt.axhline(y=450, linestyle="--", color="green")
plt.xlabel("Time (Days)")
plt.ylabel("Altitude (km)")
plt.legend()
plt.grid()
plt.show()

#Computing the time in years

t_list_years = []
t_list_years_sat = []
for i in range(len(t_list_days)):
    t_list_years.append(t_list_days[i]/365)
for i in range(len(t_list_days_sat)):
    t_list_years_sat.append(t_list_days_sat[i]/365)

#Graph computed in years

plt.plot(t_list_years, z_list, label="with inflatable")
plt.plot(t_list_years_sat, z_list_sat, label="without inflatable")
plt.axhline(y=450, linestyle="--", color="green")
plt.xlabel("Time (Years)")
plt.ylabel("Altitude (km)")
plt.title(("Time for a "+ str(m)+ " kg satellite to de-orbit from "+ str(z0)+ " km."))
plt.legend()
plt.grid()
plt.show()

#Drag force graph

plt.plot(t_list_days[1:], F_list)
plt.xlabel("Time (Days)")
plt.ylabel("Drag Force (N)")
plt.grid()
plt.show()

#Orbital eccentricity graph
#
# plt.plot(t_list_days[1:], e_list)
# plt.xlabel("Time (Days)")
# plt.ylabel("Eccentricity (-)")
# plt.grid()
# plt.show()
#
# #altitude decay rate graph
#
# plt.plot(t_list_days_unit, z_diff_list)
# plt.xlabel("Time (Days)")
# plt.ylabel("Decay Rate (km/day)")
# plt.grid()
# plt.show()
#
# #Orbital angle graph
#
# plt.plot(t_list_days, angle_list)
# plt.xlabel("Time (Days)")
# plt.ylabel("Angle (rad)")
# plt.grid()
# plt.show()
#
# #TIme period to make a full orbit graph
#
# plt.plot(t_list_days[1:], P_list)
# plt.xlabel("Time (Days)")
# plt.ylabel("Orbital Period (Hours)")
# plt.grid()
# plt.show()
#
# #2d orbit graph
#
# plt.plot(xlist, ylist)
# plt.plot(circ_x, circ_y)
# plt.xlabel("")
# plt.ylabel("")
# plt.grid()
# plt.show()
#
# #2d altitude orit graph
#
# plt.plot(xzlist, yzlist)
# plt.xlabel("")
# plt.ylabel("")
# plt.grid()
# plt.show()
#
# #velocity of the satellite graph
#
plt.plot(t_list_days, v_list)
plt.xlabel("Time (Days)")
plt.ylabel("Velocity (m/s)")
plt.grid()
plt.show()