import matplotlib.pyplot as plt
import numpy as np
import serial
import time

ser = serial.Serial('COM3', 9800, timeout=2)

p_in = 40000 #Pressure
V_i = 0.02356 #Volume

T = 300 #temperature
n = 0.3863 #amount of particles
R = 8.1345 #Ideal gas constant

A = 1e-7 #Area of the hole
p_out = 101 #Ambient pressure, offset of the sensor
pressure_reading_offset = p_out #Offset to convert sensor readings to the absolute pressure

delta_p_0 = p_in-p_out

rho = p_in/(R*T)

def get_pressure_value():
    valid_value = False

    while not valid_value:
        print('waiting for a line')
        line = ser.readline()
        print('got: {}'.format(line))
        string = line.decode()
        stripped_string = string.strip()

        if len(stripped_string) < 7:
            print(' got a valid number')
            valid_value = True

    num_int = float(stripped_string)
    print('returning: {}'.format(num_int))
    return num_int

def calibration_procedure():
    #Get three values from the sensor and calculate the average number
    total = 0.0
    for index in range(3):
        total += get_pressure_value()

    return total / 3.0

if __name__ == '__main__':
    #First, calibrate the sensor and finetune the ambient pressure p_out
    print('Initializing the calibration process, press enter without the sensor being connected to the beam')
    input()
    pressure_value_ambient = calibration_procedure()
    pressure_reading_offset = p_out - pressure_value_ambient
    print('Offset of the sensor was recorded at: {}'.format(pressure_value_ambient))

    print('Please inflate the inflatable to the desired pressure and press enter again')
    input()
    p_current = get_pressure_value() + pressure_reading_offset
    starting_epoch = time.time()
    print('A starting pressure of {} kPa has been recorded'.format(p_current))

    recording = True
    while recording:
        elapsed_seconds = time.time() - starting_epoch
        p_current = get_pressure_value() + pressure_reading_offset

        tau = elapsed_seconds / -np.log(p_current / p_in)
        A_leak = ((n*R*T) / tau) / (p_in * (((2 / rho) * delta_p_0) ** (0.5)))
        print('The leak at the moment is around {} m2, pressure {} kPa, elapsed seconds {}'.format(A_leak, p_current, elapsed_seconds))

        if elapsed_seconds > 0.8:
            with open('leaking_values.txt', 'a') as f:
                f.write('{}-{}-{}\n'.format(A_leak, p_current, elapsed_seconds))




