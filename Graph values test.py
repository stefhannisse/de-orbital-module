import matplotlib.pyplot as plt

x_values = []
y_values = []
pressure_values = []

with open('leaking_values.txt', 'r') as f:
    #print(f.readlines())
    for line in f.readlines():
        #print(line.find('e'))
        if(line.find('e') == -1):
            area_hole = float(line[:line.find('-')])
        else:
            area_hole = float(line[:line.find('-', line.find('-') + 1)])

        line = line.replace(str(area_hole), '')
        y_values.append(area_hole)

        time = line[::-1]
        time = time[:time.find('-')]
        time = float(time[::-1])

        x_values.append(time)
        line = line.replace(str(time), '')

        pressure_values.append(float(line[1:-2]))

plt.plot(x_values, pressure_values)
plt.xlabel('Time in seconds')
plt.ylabel('Internal pressure in kPa')
plt.show()

plt.plot(x_values, y_values)
plt.xlabel('Time in seconds')
plt.ylabel('Leakage hole in m2')
plt.show()

#Het is 2.4e-6 m2 groot