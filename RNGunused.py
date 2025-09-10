import random

class RNGobject:

    def __init__(self):

        self.counter = 0

    def generateRN(self):
        self.counter += 1
        random.shuffle([0,1,2,3])
