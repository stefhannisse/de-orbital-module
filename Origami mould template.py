import matplotlib.pyplot as plt
import numpy as np
import math

#The distance between the lines varies per diameter:
# 32mm: 4mm
# 33mm: 4.5mm

def draw_phi1_lines(line_width, line_index, circumference, accounted_line_width, inverted, line_distance):
    height_interval = circumference / 5
    for line_index_height in range(6):
        x = np.array([line_width * line_index, (line_index + 1) * line_width])
        if inverted:
            y = np.array([line_index_height * height_interval, (line_index_height * height_interval) + line_distance])
        else:
            y = np.array([(line_index_height * height_interval) + line_distance, line_index_height * height_interval])

        plt.plot(x, y, linewidth=accounted_line_width)

def draw_phi2_lines(line_width, line_index, circumference, accounted_line_width, inverted, line_distance):
    height_interval = circumference / 5
    for line_index_height in range(5):
        x = np.array([line_width * line_index, (line_index + 1) * line_width])
        if inverted:
            y = np.array([(line_index_height * height_interval) + line_distance, ((line_index_height + 1) * height_interval)])
        else:
            y = np.array([((line_index_height + 1) * height_interval), (line_index_height * height_interval) + line_distance])

        plt.plot(x, y, linewidth=accounted_line_width)

def main():
    width = 297
    height = 210
    diameter = 60  # Enter the diameter of the tube here in centimetres
    line_width = 1
    height_width_factor = 0.67
    line_distance = 5

    debug = True

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
        diameter = 33 #Stond op 32, maar was wel te klein; nieuwe poging is 33(3 mm breder)
        origami_type = 1

    if(diameter == 32):
        line_distance = 4
    elif(diameter == 33):
        line_distance = 4.3

    if origami_type == 0:
        circumference = math.pi * diameter
        multiplier = circumference / width
        accounted_width = width * multiplier
        accounted_height = height * multiplier
        accounted_line_width = line_width * multiplier
    else:
        circumference = math.pi * diameter
        multiplier = circumference / height
        accounted_width = width * multiplier
        accounted_height = height * multiplier
        accounted_line_width = line_width * multiplier

    if accounted_line_width < 0.5:
        accounted_line_width = 0.5

    print('circumference is: {}'.format(circumference))

    x = np.array([0, width, width, 0, 0])
    y = np.array([0, 0, height, height, 0])

    plt.figure(figsize=(11.69,8.27))

    #Draw the A4 size
    plt.plot(x, y)

    if origami_type == 0:
        #Draw the width of the circumference line
        x = np.array([0, width, width, 0, 0])
        y = np.array([0, 0, height * multiplier, height * multiplier, 0])
        plt.plot(x, y, linewidth=accounted_line_width)

    if origami_type == 0:
        #Draw the triangles at the bottom line
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

        #Calculate the length between the individual lines
        line_width = (diameter / 2) * height_width_factor
        inverted = True

        for line_index in range(0, math.floor(width / line_width)):
            #Create the horizontal lines
            x = np.array([line_index * line_width, line_index * line_width])
            y = np.array([0, accounted_height])
            plt.plot(x, y, linestyle='dotted', linewidth=accounted_line_width)

            #Create the phi1 angle lines
            draw_phi1_lines(line_width, line_index, circumference, accounted_line_width, inverted, line_distance)
            draw_phi2_lines(line_width, line_index, circumference, accounted_line_width, inverted, line_distance)
            inverted = not inverted

    plt.set_cmap('hot')
    plt.axis('off')
    plt.savefig("origami.png", orientation = 'portrait', bbox_inches='tight', format = 'png')
    plt.show()

if __name__ == '__main__':
    main()