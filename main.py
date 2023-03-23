import matplotlib.pyplot as plt
import numpy as np
import math

width = 297
height = 210
diameter = 60 #Enter the diameter of the tube here in centimetres
line_width = 1

debug = False

if (math.pi * diameter) > width:
    print('This value is greater than the width of an A4')
    exit()

if not debug:
    print('What is the diameter of the inflatable beam?(mm)')
    diameter = int(input())

    print('What origami folding pattern should be used?')
    print('0 -> Symmetrical origami fold')
    print('1 -> Inflatesail folding pattern')
    origami_type = int(input())
else:
    diameter = 90
    origami_type = 1

circumference = math.pi * diameter
multiplier = circumference / width
accounted_width = width * multiplier
accounted_height = height * multiplier
accounted_line_width = line_width * multiplier

if accounted_line_width < 0.5:
    accounted_line_width = 0.5

x = np.array([0, width, width, 0, 0])
y = np.array([0, 0, height, height, 0])

plt.figure(figsize=(11.69,8.27))

#Draw the A4 size
plt.plot(x, y)

#Draw the width of the circumference line
x = np.array([0, circumference, circumference, 0, 0])
y = np.array([0, 0, height * multiplier, height * multiplier, 0])
plt.plot(x, y, linewidth=accounted_line_width)

if origami_type == 0:
    #Draw the triangles at the bottom line
    #
    triangle_width = accounted_width / 3

    #All the folding lines
    x = np.array([0, triangle_width / 2, triangle_width * 2.5, accounted_width, accounted_width / 2, 0, triangle_width / 2, triangle_width * 2.5, accounted_width, accounted_width / 2, 0])
    y = np.array([accounted_height / 4, 0, accounted_height, accounted_height * 0.75, 0, accounted_height * 0.75, accounted_height, 0, accounted_height / 4, accounted_height, accounted_height / 4])
    plt.plot(x, y, linewidth=accounted_line_width)

    #The three horizontal lines
    x = np.array([0, accounted_width])
    y = np.array([accounted_height * 0.25, accounted_height * 0.25])
    plt.plot(x, y, linestyle='dotted', linewidth=accounted_line_width)

    x = np.array([0, accounted_width])
    y = np.array([accounted_height * 0.5, accounted_height * 0.5])
    plt.plot(x, y, linestyle='dotted', linewidth=accounted_line_width)

    x = np.array([0, accounted_width])
    y = np.array([accounted_height * 0.75, accounted_height * 0.75])
    plt.plot(x, y, linestyle='dotted', linewidth=accounted_line_width)

else:
    print('Origami type is 1')

    sub_height = accounted_height / 4
    sub_width = accounted_width / 5
    phi_1 = 67
    phi_2 = 8 #This was an estimation based on the supplied image

    print('angle: {}'.format(90 - phi_1 - phi_2))

    coordinate_x = sub_height / math.tan(phi_1 + phi_2)

    print('coordinate x: {}'.format(coordinate_x))

    x = np.array([0, sub_width / 5])
    y = np.array([0, sub_height])
    plt.plot(x, y, linewidth=accounted_line_width)

plt.set_cmap('hot')
plt.axis('off')
plt.savefig("origami.png", orientation = 'portrait', bbox_inches='tight', format = 'png')
plt.show()