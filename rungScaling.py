import os
from glob import glob
import numpy as np

from psychopy.tools.coordinatetools import pol2cart, cart2pol

from utilities import *

def getBlindSpotProperties(ID, task='distance'):

    if task == None:
        return({})

    if ID == None:
        return({})

    main_path = '../data/' + task + '/'
    
    hemifields = []

    ## read blindspot parameters... if any...
    path = os.path.join('..', 'data', task, 'mapping', ID + '_LH_blindspot*.txt' )
    left_files = glob.glob( path )
    if len(left_files):
        idx = np.argmax([int(os.path.splitext(os.path.basename(x))[0].split('_')[3]) for x in left_files])
        bs_file = open(left_files[idx], 'r')
        bs_param = bs_file.read().replace('\t','\n').split('\n')
        bs_file.close()
        spot_left_cart = eval(bs_param[1])
        spot_left = cart2pol(spot_left_cart[0], spot_left_cart[1])
        spot_left_size = eval(bs_param[3])
        hemifields.append('left')

    right_files = glob.glob(os.path.join('..', 'data', task, 'mapping', ID + '_RH_blindspot*.txt' ) )
    if len(right_files):
        idx = np.argmax([int(os.path.splitext(os.path.basename(x))[0].split('_')[3]) for x in right_files])
        bs_file = open(right_files[idx],'r')
        bs_param = bs_file.read().replace('\t','\n').split('\n')
        bs_file.close()
        spot_righ_cart = eval(bs_param[1])
        spot_righ = cart2pol(spot_righ_cart[0], spot_righ_cart[1])
        spot_righ_size = eval(bs_param[3])
        hemifields.append('right')

    # print(hemifields)

    blindspotmarkers = {}
    
    for hemifield in hemifields:

        if hemifield == 'left':
            spot_cart = spot_left_cart
            spot      = spot_left
            spot_size = spot_left_size
            tar       = spot_size[0] + 2 + 2
        if hemifield == 'right':
            spot_cart = spot_righ_cart
            spot      = spot_righ
            spot_size = spot_righ_size
            tar       = spot_size[0] + 2 + 2

        # size of blind spot + 2 (dot width, padding)
        if hemifield == 'left' and spot_cart[1] < 0:
            ang_up = (cart2pol(spot_cart[0], spot_cart[1] - spot_size[1])[0] - spot[0]) + 2
        else:
            ang_up = (cart2pol(spot_cart[0], spot_cart[1] + spot_size[1])[0] - spot[0]) + 2
        
        blindspotmarkers[hemifield+'_prop'] = { 'cart'   : spot_cart,
                                                'spot'   : spot,
                                                'size'   : spot_size,
                                                'tar'    : tar,
                                                'ang_up' : ang_up       }

        # print(spot_size)
        spot_size = [max(min(1,x),x-1.5) for x in spot_size]
        # print(spot_size)


        # blindspotmarkers[hemifield] = visual.Circle(win, radius = .5, pos = [7,0], units = 'deg', fillColor=colors[hemifield], lineColor = None, interpolate = True)
        # blindspotmarkers[hemifield].pos = spot_cart
        # blindspotmarkers[hemifield].size = spot_size

    # print(len(blindspotmarkers))

    return(blindspotmarkers)

from utilities import *

def checkBlindSpotLocations():

    genInfo = getGeneralDataInfo()

    participants = genInfo['IDbyTask']['distance']

    for ID in participants:

        BSprop = getBlindSpotProperties(ID)

        left_prop    = BSprop['left_prop']
        right_prop   = BSprop['right_prop']

        spot_left    = left_prop['spot']
        ang_up_left  = left_prop['ang_up']
        tar_left     = left_prop['tar']

        spot_right   = right_prop['spot']
        ang_up_right = right_prop['ang_up']
        tar_right    = right_prop['tar']

        ## prepare trials

        # these positions are polar coordinates: (angle, distance)
        positions = {
            "left-top": [(spot_left[0]  - ang_up_left,  spot_left[1]  - tar_left/2),  (spot_left[0]  - ang_up_left,  spot_left[1]  + tar_left/2)],
            "left-mid": [(spot_left[0]  +          00,  spot_left[1]  - tar_left/2),  (spot_left[0]  +          00,  spot_left[1]  + tar_left/2)],
            "left-bot": [(spot_left[0]  + ang_up_left,  spot_left[1]  - tar_left/2),  (spot_left[0]  + ang_up_left,  spot_left[1]  + tar_left/2)],
            "righ-top": [(spot_right[0] + ang_up_right, spot_right[1] - tar_right/2), (spot_right[0] + ang_up_right, spot_right[1] + tar_right/2)],
            "righ-mid": [(spot_right[0] +           00, spot_right[1] - tar_right/2), (spot_right[0] +           00, spot_right[1] + tar_right/2)],
            "righ-bot": [(spot_right[0] - ang_up_right, spot_right[1] - tar_right/2), (spot_right[0] - ang_up_right, spot_right[1] + tar_right/2)],
        }

        left_scale = (positions["left-mid"][0][1] - 1) / (positions["left-mid"][1][1])
        righ_scale = (positions["righ-mid"][0][1] - 1) / (positions["righ-mid"][1][1])

        print([left_scale, righ_scale])

