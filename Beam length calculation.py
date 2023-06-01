import math

sail_side_length = 0.45 #The length of the sail sides in meters
beam_angle = 35 #Angle in degrees for the inflated beam

b1 = (sail_side_length / 2) / math.sin(45 * (math.pi / 180))

bl = b1 / math.cos(beam_angle * (math.pi / 180))

#Substract the container length from the beam length
bl = bl - 0.04

print('The beam length must be {} meters'.format(bl))

