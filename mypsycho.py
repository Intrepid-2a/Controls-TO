# for reproducing previous stuff
# it might be better to import the actual psychopy functions after all

# import numpy as np

# def cart2pol(x, y):
#     theta = (np.arctan2(y,x) / np.pi) * 180
#     radius = (x**2 + y**2)**0.5
#     return([theta, radius])


# def pol2cart(theta, radius):
#     rad = (theta / 180) * np.pi
#     x = np.cos(rad) * radius
#     y = np.sin(rad) * radius
#     return([x,y])

class myCircle:

    def __init__(self, 
                 win         = False, 
                 radius      = .5, 
                 pos         = [0,0], 
                 units       = 'deg',
                 fillColor   = [-1,-1,-1],
                 lineColor   = None,
                 interpolate = False,
                 size        = None):

        self.win         = win
        self.radius      = radius
        self.pos         = pos
        self.units       = units
        self.fillColor   = fillColor
        self.lineColor   = lineColor
        self.interpolate = interpolate
        self.size        = size

    def draw(self):
        return