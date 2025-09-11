# for reproducing previous stuff
# it might be better to import the actual psychopy functions after all

import numpy as np

def cart2pol(x, y):
    theta = (np.arctan2(y,x) / np.pi) * 180
    radius = (x**2 + y**2)**0.5
    return([theta, radius])


def pol2cart(theta, radius):
    rad = (theta / 180) * np.pi
    x = np.cos(rad) * radius
    y = np.sin(rad) * radius
    return([x,y])