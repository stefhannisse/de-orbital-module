import numpy as np
import matplotlib.pyplot as plt

phi1 = 67 * (np.pi / 180)

n = 5
R = 17
HR = 0.67 #Was 16
H = HR * R

d_ratio = np.sin(phi1 - (np.pi / n)) / (np.sin(phi1 + (np.pi / n)))
print(d_ratio)

d2 = (2 * np.pi * R) / ((d_ratio + 1) * n)
d1 = d2 * d_ratio

l1 = H / np.tan(phi1)

point1x = 0
point1y = 0

point2x = l1
point2y = H

point3x = d1
point3y = 0

point4x = d1 + d2
point4y = 0

point5x = l1 + d2
point5y = H

point6x = l1 + d2 + d1
point6y = H

point7x = 0
point7y = 2 * H

point8x = d1
point8y = 2 * H

point9x = d1 + d2
point9y = 2 * H

print("d1: " + str(d1) + " mm")
print("d2: " + str(d2) + " mm")

print("Point 1    x: " + str(point1x) + " mm     y: " + str(point1y) + " mm")
print("Point 2    x: " + str(point3x) + " mm     y: " + str(point3y) + " mm")
print("Point 3    x: " + str(point2x) + " mm     y: " + str(point2y) + " mm")
print("Point 4    x: " + str(point4x) + " mm     y: " + str(point4y) + " mm")
print("Point 5    x: " + str(point5x) + " mm     y: " + str(point5y) + " mm")
print("Point 6    x: " + str(point6x) + " mm     y: " + str(point6y) + " mm")
print("Point 7    x: " + str(point7x) + " mm     y: " + str(point7y) + " mm")
print("Point 8    x: " + str(point8x) + " mm     y: " + str(point8y) + " mm")
print("Point 9    x: " + str(point9x) + " mm     y: " + str(point9y) + " mm")

plt.scatter(point1x, point1y)
plt.scatter(point2x, point2y)
plt.scatter(point3x, point3y)
plt.scatter(point4x, point4y)
plt.scatter(point5x, point5y)
plt.scatter(point6x, point6y)
plt.scatter(point7x, point7y)
plt.scatter(point8x, point8y)
plt.scatter(point9x, point9y)
plt.show()
