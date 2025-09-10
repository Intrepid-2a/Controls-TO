import random

from RNGunused import RNGobject


def testRNGindependence(externalCalls=False):

    shuffler = RNGobject()

    random.seed('somestring')

    for trial in range(10):

        if externalCalls:
            shuffler.generateRN()

        print(random.choice([1,2,3,4,5]))