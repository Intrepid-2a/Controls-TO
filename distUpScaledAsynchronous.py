 #!/usr/bin/env python
# -*- coding: utf-8 -*-

""" 
Distance comparison across blind spot
TWCF IIT vs PP experiment 2a piloting
Authors: Clement Abbatecola, Belén María Montabes de la Cruz
    Code version:
        2.2 # 2024/03/25    Various fixes (notably better file saving, eye-tracker handling and bug when first response was bad)
        2.1 # 2024/02/16    Common code for LH and RH
        2.0 # 2024/02/12    Final common version before eye tracking
"""


# look at how to read out key presses?
# https://discourse.psychopy.org/t/why-is-my-event-getkeys-memory-buffer-not-clearing/26716/4


import psychopy
from psychopy import core, visual, gui, data, event
from psychopy.tools.coordinatetools import pol2cart, cart2pol
import numpy as np
import random, datetime, os
from glob import glob
from itertools import compress

from psychopy.hardware import keyboard
from pyglet.window import key


import sys, os
sys.path.append(os.path.join('..', 'EyeTracking'))
from EyeTracking import localizeSetup, EyeTracker

######
#### Initialize experiment
######

def doDistUpScaledAsynchronousTask(ID=None, hemifield=None, location=None):

    ## parameters
    nRevs   = 10   #
    nTrials = 30
    # nTrials = 25  # at least 10 reversals and 25 trials for each staircase (~ 25*8 staircases = 200 trials)
    # letter_height = 40 # 40 dva is pretty big?
    letter_height = 1

    ## files
    # expInfo = {'ID':'test', 'hemifield':['left','right']}
    # dlg = gui.DlgFromDict(expInfo, title='Infos', screen=0)
    # ID = expInfo['ID'].lower()
    # hemifield = expInfo['hemifield']
    expInfo = {}
    askQuestions = False
    if ID == None:
        expInfo['ID'] = ''
        askQuestions = True
    if hemifield == None:
        expInfo['hemifield'] = ['left','right']
        askQuestions = True
    # expInfo = {'ID':'test', 'hemifield':['left','right']}
    if askQuestions:
        dlg = gui.DlgFromDict(expInfo, title='Infos', screen=0)

    if ID == None:
        ID = expInfo['ID'].lower()
    if hemifield == None:
        hemifield = expInfo['hemifield']

    # need to know which eye-tracker to use:
    if location == None:
        # hacky, but true for now:
        if os.sys.platform == 'linux':
            location = 'toronto'
        else:
            location = 'glasgow'


    random.seed(ID+'distance'+hemifield)

    trackEyes = [True, True]

    # ## path
    main_path = '../data/distUpScaledAsynchronous/'
    data_path = main_path
    eyetracking_path = main_path + 'eyetracking/' + ID + '/'
    
    # this _should_ already be handled by the Runner utility: setupDataFolders()
    os.makedirs(data_path, exist_ok=True)
    # but not this one:
    os.makedirs(eyetracking_path, exist_ok=True)


    # create output file:
    x = 1
    # filename = '_dist_' + ('LH' if hemifield == 'left' else 'RH') + '_' + ID + '_'
    filename = ID + '_distusa_' + ('LH' if hemifield == 'left' else 'RH') + '_'
    while (filename + str(x) + '.txt') in os.listdir(data_path):
        x += 1
    respFileName = data_path + filename + str(x) + '.txt'
    respFile = open(respFileName,'w')

    respFile.write(''.join(map(str, ['Start: \t' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M') + '\n'])))
    respFile.write('\t'.join(map(str, ['Resp',
                                    'Targ_loc',
                                    'Foil_loc',
                                    'Targ_len',
                                    'Difference',
                                    'Which_first',
                                    'Targ_chosen',
                                    'Reversal',
                                    'Foil_type',
                                    'Eye',
                                    'Gaze_out',
                                    'Stair',
                                    'Trial'])) + '\n')
    respFile.close()
    print(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
    print("Resp",
        "Targ_loc",
        "Foil_loc",
        "Targ_len",
        "Difference",
        "Which_first",
        "Targ_chosen",
        "Reversal",
        "Foil_type",
        "Eye",
        "Gaze_out",
        "Stair")


    x = 1
    et_filename = 'dSA' + ('LH' if hemifield == 'left' else 'RH')
    while len(glob(eyetracking_path + et_filename + str(x) + '.*')):
        x += 1

    # get everything shared from central:
    setup = localizeSetup(location=location, trackEyes=trackEyes, filefolder=eyetracking_path, filename=et_filename+str(x), task='distUpScaledAsynchronous', ID=ID) # data path is for the mapping data, not the eye-tracker data!

    # setup = localizeSetup(location=location, trackEyes=trackEyes, filefolder=eyetracking_path, filename=et_filename+str(x), task='distScaledAsynchronous', ID=ID, noEyeTracker=True ) # data path is for the mapping data, not the eye-tracker data!
    # print(setup['paths']) # not using yet, just testing

    # unpack all this
    win = setup['win']


    pyg_keyboard = key.KeyStateHandler()
    win.winHandle.push_handlers(pyg_keyboard)

    colors = setup['colors']
    col_both = colors['both']
    if hemifield == 'left':
        col_ipsi, col_contra = colors['left'], colors['right']
    if hemifield == 'right':
        col_contra, col_ipsi = colors['left'], colors['right']

    # if hemifield == 'left':
    #     col_ipsi, col_contra = colors['right'], colors['left']
    # if hemifield == 'right':
    #     col_contra, col_ipsi = colors['right'], colors['left']

    # print(colors)

    hiFusion = setup['fusion']['hi']
    loFusion = setup['fusion']['lo']

    blindspot = setup['blindspotmarkers'][hemifield]
    # print(blindspot.fillColor)
    
    fixation   = setup['fixation']
    fixation_x = setup['fixation_x']

    tracker = setup['tracker']
    



    ## instructions
    visual.TextStim(win,'Troughout the experiment you will fixate at a white cross that will be located at the center of the screen.   \
    It is important that you fixate on this cross at all times.\n\n You will be presented with pairs of dots. You will have to indicate which dots were closer together.\n\n Left arrow = first pair of dots were closer together.\
    \n\n Right arrow = second pair of dots were closer together.\n\n\n Press the space bar to start the experiment.', height = letter_height,wrapWidth=15, color = 'black').draw()
    win.flip()
    k = ['wait']
    while k[0] not in ['q','space']:
        k = event.waitKeys()
    if k[0] in ['q']:
        win.close()
        core.quit()


    ######
    #### Prepare stimulation
    ######

    ## stimuli
    point_1 = visual.Circle(win, radius = .5, pos = pol2cart(00, 3), units = 'deg', fillColor = col_both, lineColor = None)
    point_2 = visual.Circle(win, radius = .5, pos = pol2cart(00, 6), units = 'deg', fillColor = col_both, lineColor = None)
    point_3 = visual.Circle(win, radius = .5, pos = pol2cart(45, 3), units = 'deg', fillColor = col_both, lineColor = None)
    point_4 = visual.Circle(win, radius = .5, pos = pol2cart(45, 6), units = 'deg', fillColor = col_both, lineColor = None)

    # blindspot = visual.Circle(win, radius = .5, pos = [7,0], units = 'deg', fillColor=col_ipsi, lineColor = None)
    # blindspot.pos = spot_cart
    # blindspot.size = spot_size
    # blindspot.autoDraw = True 

    left_prop  = setup['blindspotmarkers']['left_prop']
    right_prop = setup['blindspotmarkers']['right_prop']

    spot_left    = left_prop['spot']
    ang_up_left  = left_prop['ang_up']
    tar_left     = left_prop['tar']

    spot_right   = right_prop['spot']
    ang_up_right = right_prop['ang_up']
    tar_right    = right_prop['tar']

    # left_scale  = (spot_left[1]  - tar_left/2)  / (spot_left[1]  + tar_left/2)
    # right_scale = (spot_right[1] - tar_right/2) / (spot_right[1] + tar_right/2)
    left_scale  = 1
    right_scale = 1


    ## prepare trials
    # these are in polar coordinates, for both an inner and outer dot position:
    # positions = {
    #     "left-top": [(spot_left[0]  - ang_up_left,  spot_left[1]  - tar_left/2),  (spot_left[0]  - ang_up_left,  spot_left[1]  + tar_left/2)],
    #     "left-mid": [(spot_left[0]  +          00,  spot_left[1]  - tar_left/2),  (spot_left[0]  +          00,  spot_left[1]  + tar_left/2)],
    #     "left-bot": [(spot_left[0]  + ang_up_left,  spot_left[1]  - tar_left/2),  (spot_left[0]  + ang_up_left,  spot_left[1]  + tar_left/2)],
    #     "righ-top": [(spot_right[0] + ang_up_right, spot_right[1] - tar_right/2), (spot_right[0] + ang_up_right, spot_right[1] + tar_right/2)],
    #     "righ-mid": [(spot_right[0] +           00, spot_right[1] - tar_right/2), (spot_right[0] +           00, spot_right[1] + tar_right/2)],
    #     "righ-bot": [(spot_right[0] - ang_up_right, spot_right[1] - tar_right/2), (spot_right[0] - ang_up_right, spot_right[1] + tar_right/2)],
    # }
    # we want cartesian for this variant:
    # positions = {
    #     "left-top": pol2cart(spot_left[0]  - ang_up_left,  spot_left[1]  * left_scale  ),
    #     "left-mid": pol2cart(spot_left[0]  +          00,  spot_left[1]  * left_scale  ),
    #     "left-bot": pol2cart(spot_left[0]  + ang_up_left,  spot_left[1]  * left_scale  ),
    #     "righ-top": pol2cart(spot_right[0] + ang_up_right, spot_right[1] * right_scale ),
    #     "righ-mid": pol2cart(spot_right[0] +           00, spot_right[1] * right_scale ),
    #     "righ-bot": pol2cart(spot_right[0] - ang_up_right, spot_right[1] * right_scale ),
    # }
    positions = {
        "left-top": [a+b for a,b in zip(pol2cart(spot_left[0]  - ang_up_left,  spot_left[1])  , [tar_left+1,0]  )],
        "left-mid": [a+b for a,b in zip(pol2cart(spot_left[0]  +          00,  spot_left[1])  , [tar_left+1,0]  )],
        "left-bot": [a+b for a,b in zip(pol2cart(spot_left[0]  + ang_up_left,  spot_left[1])  , [tar_left+1,0]  )],
        "righ-top": [a-b for a,b in zip(pol2cart(spot_right[0] + ang_up_right, spot_right[1]) , [tar_right+1,0] )],
        "righ-mid": [a-b for a,b in zip(pol2cart(spot_right[0] +           00, spot_right[1]) , [tar_right+1,0] )],
        "righ-bot": [a-b for a,b in zip(pol2cart(spot_right[0] - ang_up_right, spot_right[1]) , [tar_right+1,0] )],
    }

    if hemifield == 'left':
        # First column is target, second column is foil
        pos_array = [["left-mid", "left-top"],
                     ["left-mid", "left-bot"],
                     ["left-top", "left-bot"],
                     ["left-bot", "left-top"]]
        tar = tar_left
        scale = left_scale
        dir = -1
        win.viewPos = [10,0]
        # cfg['hw']['fusion']['lo'].pos = [-10,-7] # does this even make sense? should just be the old position...
        # cfg['hw']['fusion']['hi'].pos = [-10,7]
    else:
        pos_array = [["righ-mid", "righ-top"],
                     ["righ-mid", "righ-bot"],
                     ["righ-top", "righ-bot"],
                     ["righ-bot", "righ-top"]]
        tar = tar_right
        scale = right_scale
        dir =  1
        win.viewPos = [-10,0]

    tar = tar * scale

    pos_array_bsa = pos_array[0:2]
    pos_array_out = pos_array[2:4]

    point_1.radius = 0.75 
    point_2.radius = 0.75 
    point_3.radius = 0.75 
    point_4.radius = 0.75 


    ######
    #### Prepare eye tracking
    ######

    ## setup and initialize eye-tracker + gaze ok region etc.
    #!!#

    # first calibration
    visual.TextStim(win,'Calibration...', color = col_both, units = 'deg', pos = (0,-2)).draw()
    fixation.draw()
    win.flip()
    k = event.waitKeys()
    if k[0] in ['q']:
        respFile.close()

        # send quit comment
        # stop tracking
        # close file
        # shutdown eye-tracker

        win.close()
        core.quit()
    
    event.clearEvents(eventType='keyboard') # just to be sure?
        
    #!!# calibrate
    ####tracker.initialize() # this should be done in the central thing... dependent on location: in Toronto we need to override the calibrationTargets

    tracker.openfile()
    tracker.startcollecting()
    tracker.calibrate()
    
    fixation.draw()
    win.flip()

    k = event.waitKeys()
    if k[0] in ['q']:
        respFile.close()

        # send quit comment
        # stop tracking
        # close file
        # shutdown eye-tracker

        #! empty buffer?

        win.close()
        core.quit()
    
    event.clearEvents(eventType='keyboard') # just to be sure?

    #!!# start recording

    ######
    #### Staircase
    ######

    trial_clock = core.Clock()

    foil_type = [1, -1] * 4
    eye = ['left', 'left', 'right', 'right'] * 2
    pos_arrays = [pos_array_bsa[:]] * 4 + [pos_array_out[:]] * 4

    intervals = [3.5, 3, 2.5, 2, 1.5, 1, .5, 0, -.5, -1, -1.5, -2, -2.5, -3, -3.5]
    # intervals = [3.5,    2.5,    1.5, 1, .5, 0, -.5, -1, -1.5,     -2.5,     -3.5]
    # intervals = [ 1.05, 0.9, 0.75, 0.6, 0.45, 0.3, 0.15, 0.0, -0.15, -0.3, -0.45, -0.6, -0.75, -0.9, -1.05 ]

    position = [[]] * 8
    trial_stair = [0] * 8
    revs = [0] * 8
    direction = [1] * 8
    cur_int = [0] * 8
    reversal = False
    resps = [[True],[False]] * 4
    stairs_ongoing = [True] * 8

    trial = 1
    abort = False
    recalibrate = False
    break_trial = 1

    while any(stairs_ongoing):

        increment = True

        ## choose staircase
        which_stair = random.choice(list(compress([x for x in range(len(stairs_ongoing))], stairs_ongoing)))

        ## set trial
        if position[which_stair] == []:
            random.shuffle(pos_arrays[which_stair])
            position[which_stair] = pos_arrays[which_stair][:]
        pos = position[which_stair].pop()

        shift = random.sample([-.5, -.25, 0, .25, .5], 2) # used to be [-1, -.5, 0, .5, .1]
        dif = intervals[cur_int[which_stair]] * foil_type[which_stair]
        which_first = random.choice(['Targ', 'Foil'])




        # for radially oriented dot pairs:
        # if which_first == 'Targ':
        #     point_1.pos = pol2cart(positions[pos[0]][0][0], positions[pos[0]][0][1]       + shift[0])
        #     point_2.pos = pol2cart(positions[pos[0]][1][0], positions[pos[0]][1][1]       + shift[0])
        #     point_3.pos = pol2cart(positions[pos[1]][0][0], positions[pos[1]][0][1]       + shift[1])
        #     point_4.pos = pol2cart(positions[pos[1]][1][0], positions[pos[1]][1][1] + dif + shift[1])
        # else:
        #     point_3.pos = pol2cart(positions[pos[0]][0][0], positions[pos[0]][0][1]       + shift[0])tracker
        # print(positions[pos[0]])
        # print(positions[pos[1]])



        if which_first == 'Targ':
            point_1.pos = (positions[pos[0]][0]             + shift[0] -(tar/2)*dir, positions[pos[0]][1])
            point_2.pos = (positions[pos[0]][0]             + shift[0] +(tar/2)*dir, positions[pos[0]][1])
            point_3.pos = (positions[pos[1]][0]             + shift[1] -(tar/2)*dir, positions[pos[1]][1])
            point_4.pos = (positions[pos[1]][0] + (dif*dir) + shift[1] +(tar/2)*dir, positions[pos[1]][1])
        else:
            point_3.pos = (positions[pos[0]][0]             + shift[0] -(tar/2)*dir, positions[pos[0]][1])
            point_4.pos = (positions[pos[0]][0]             + shift[0] +(tar/2)*dir, positions[pos[0]][1])
            point_1.pos = (positions[pos[1]][0]             + shift[1] -(tar/2)*dir, positions[pos[1]][1])
            point_2.pos = (positions[pos[1]][0] + (dif*dir) + shift[1] +(tar/2)*dir, positions[pos[1]][1])


        # distPair1 = ((point_1.pos[0]-point_2.pos[0])**2 + (point_1.pos[1]-point_2.pos[1])**2)**0.5
        # distPair2 = ((point_3.pos[0]-point_4.pos[0])**2 + (point_3.pos[1]-point_4.pos[1])**2)**0.5

        # print(distPair1 - distPair2)

        if eye[which_stair] == hemifield:
            point_1.fillColor = col_ipsi
            point_2.fillColor = col_ipsi
            point_3.fillColor = col_ipsi
            point_4.fillColor = col_ipsi
        else:
            point_1.fillColor = col_contra
            point_2.fillColor = col_contra
            point_3.fillColor = col_contra
            point_4.fillColor = col_contra
        
        hiFusion.resetProperties()
        loFusion.resetProperties()

        ## pre trial fixation
        tracker.waitForFixation()
        gaze_out = False #? not sure what this variable is for but it needs to exist?

        
        # should the trial start be here, or maybe when waiting for fixation?
        tracker.comment('start trial %d'%(trial))

        # in reverse order, so we can pop() them off:
        stim_comments = ['pair 2 off', 'pair 2 on', 'pair 1 off', 'pair 1 on']


        if not gaze_out:
            ## trial
            
            trial_clock.reset()
            gaze_in_region = True
        
            while trial_clock.getTime() <= 1.4 and not abort:
                t = trial_clock.getTime()
                
                #!!# get position at each t
                #!!# if position is invalid or >2 dva, set gaze in region to False
                #!!# may also record gazes in file here and do stuff like showing gaze position if simulating with mouse
                
                if not tracker.gazeInFixationWindow():
                    gaze_out = True
                    tracker.comment('trial aborted')
                    break

                fixation.draw()
                blindspot.draw()
                hiFusion.draw()
                loFusion.draw()

                if .1 <= trial_clock.getTime() < .7:
                    if len(stim_comments) == 4:
                        tracker.comment(stim_comments.pop()) # pair 1 on
                    point_1.draw()
                    point_2.draw()
                if .7 <= trial_clock.getTime() < .8:
                    if len(stim_comments) == 3:
                        tracker.comment(stim_comments.pop()) # pair 1 off
                if .8 <= trial_clock.getTime() < 1.4:
                    if len(stim_comments) == 2:
                        tracker.comment(stim_comments.pop()) # pair 2 on
                    point_3.draw()
                    point_4.draw()

        
                blindspot.draw()
                win.flip()
                
                k = event.getKeys(['q']) # quit / abort during trial
                if k and 'q' in k:
                    abort = True
                    tracker.comment('trial aborted') # task aborted?
                    break
                
                event.clearEvents(eventType='keyboard') # just to be sure?

        if len(stim_comments) == 1:
            tracker.comment(stim_comments.pop()) # pair 2 off
        

      

        if abort:
            break
        
        if not gaze_out: # what is this testing? gaze_out is always False... I think
        
            ## response
            # fixation.ori += 45
            # fixation.color = 'black'
            hiFusion.draw()
            loFusion.draw()
            blindspot.draw()
            fixation_x.draw()
            win.flip()
            
            k = ['wait']
            #! empty buffer?
            while k[0] not in ['q', 'space', 'left', 'right', 'num_left', 'num_right', 'num_insert']:
                k = event.waitKeys()

            if k[0] in ['q']:
                abort = True
                tracker.comment('trial aborted') # this could be more like: "task aborted"?
                break
                #! empty buffer?
            elif k[0] in ['space', 'num_insert']:
                position[which_stair] = position[which_stair] + [pos]
                increment = False
                resp = 'abort'
                targ_chosen = 'abort'
                reversal = 'abort'
                tracker.comment('trial aborted')
                #! empty buffer?
            else:
                resp = 1 if k[0] in ['left', 'num_left'] else 2
                tracker.comment('response')
                #! empty buffer?

            event.clearEvents(eventType='keyboard') # just to be sure?
                
            # fixation.ori -= 45
            
        else:
        
            ## dealing with auto-aborted trials
        
            # auto recalibrate if no initial fixation
            if recalibrate:
                recalibrate = False
                visual.TextStim(win,'Calibration...', color = col_both, units = 'deg', pos = (0,-2)).draw()
                fixation.draw()
                win.flip()
                k = event.waitKeys()
                if k[0] in ['q']:
                    abort = True
                    break
                    #! empty buffer?
                
                event.clearEvents(eventType='keyboard') # just to be sure?
                    
                #!!# calibrate
                #### tracker.stopcollecting() # do we even have to stop/start collecting?
                tracker.calibrate()
                #### tracker.startcollecting()
                recalibrate = False

                
                fixation.draw()
                win.flip()
                k = event.waitKeys()
                if k[0] in ['q']:
                    abort = True
                    break
                    #! empty buffer?
                
                event.clearEvents(eventType='keyboard') # just to be sure?
            
            # changing fixation to signify gaze out, restart with 'up' possibily of break and manual recalibration 'r' 
            else:
                hiFusion.draw()
                loFusion.draw()
                blindspot.draw()
                visual.TextStim(win, '#', height = letter_height, color = col_both).draw()
                print('# auto abort')
                win.flip()

                k = ['wait']
                while k[0] not in ['q', 'up', 'r', 'num_up']:
                    k = event.waitKeys()
                if k[0] in ['q']:
                    abort = True
                    break
                    #! empty buffer?
        
                # manual recalibrate
                if k[0] in ['r']:
                    visual.TextStim(win,'Calibration...', color = col_both, units = 'deg', pos = (0,-2)).draw()
                    fixation.draw()
                    win.flip()
                    k = event.waitKeys()
                    if k[0] in ['q']:
                        abort = True
                        break

                    #!!# calibrate
                    #### tracker.stopcollecting() # do we even have to stop/start collecting?
                    tracker.calibrate()
                    #### tracker.startcollecting()

                    fixation.draw()
                    win.flip()
                    k = event.waitKeys()
                    if k[0] in ['q']:
                        abort = True
                        break
                        #! empty buffer?

                event.clearEvents(eventType='keyboard') # just to be sure?
                
            position[which_stair] = position[which_stair] + [pos]
            increment = False
            resp = 'auto_abort'
            targ_chosen = 'auto_abort'
            reversal = 'auto_abort'
        
        if increment:
            '''
            which_first == 'Targ'          => was target first? (True/False)
            dif > 0                        => was target smaller? (True/False)
            k[0] == 'left'                 => was first chosen? (True/False)
            target first == target smaller => was first smaller? (True/False)
            first smaller == first chosen  => was smaller chosen? (True/False)
            
            (which_first == 'Targ') == (k[0] == 'left') => was target chosen?
            '''
            
            targ_chosen = (which_first == 'Targ') == (k[0] == 'left')

            ## update staircase (which direction, is there a reversal?)
            reversal = False
            resps[which_stair] = resps[which_stair] + [targ_chosen]
            if  resps[which_stair][-2] != resps[which_stair][-1]:
                reversal = True
                direction[which_stair] *= -1
                revs[which_stair] += len(resps[which_stair]) > 2
                
            ## increment/update
            cur_int[which_stair] = max(min(cur_int[which_stair] + direction[which_stair], len(intervals) - 1), 0)
            trial_stair[which_stair] = trial_stair[which_stair] + 1
            stairs_ongoing[which_stair] = revs[which_stair] <= nRevs or trial_stair[which_stair] < nTrials

        ## print trial
        print(resp,
            pos[0],
            pos[1],
            tar,
            dif,
            which_first,
            targ_chosen,
            reversal,
            foil_type[which_stair],
            eye[which_stair],
            gaze_out,
            which_stair,
            trial)
        respFile = open(respFileName,'a')
        respFile.write('\t'.join(map(str, [resp,
                                        pos[0],
                                        pos[1],
                                        tar,
                                        dif,
                                        which_first,
                                        targ_chosen,
                                        reversal,
                                        foil_type[which_stair],
                                        eye[which_stair],
                                        gaze_out,
                                        which_stair,
                                        trial])) + "\n")
        respFile.close()
        trial += 1
        break_trial += 1

        if break_trial > 50:
            # do a break...

            win.flip()
            breaktext = visual.TextStim(win, 'take a break!', height = letter_height, color = col_both)
            print('- break...')
            breaktext.draw()
            win.flip()
            
            tracker.comment('break')

            on_break = True
            while on_break:
                keys = event.getKeys(keyList=['b']) # simpler solution: use a different key... like 'b'
                if 'b' in keys:
                    on_break = False
                breaktext.draw()
                win.flip()

            event.clearEvents(eventType='keyboard') # just to be sure?


            tracker.calibrate()
            break_trial = 1

        event.clearEvents(eventType='keyboard') # just to be more sure?


    if abort:
        respFile = open(respFileName,'a')
        respFile.write("Run manually ended at " + datetime.datetime.now().strftime("%Y-%m-%d-%H-%M") + "!")
        respFile.close()
        tracker.comment('run aborted')
        # stop collecting?
        # close file?
        # shutdown eye-tracker?
    elif not any(stairs_ongoing):
        tracker.comment('run finished')
        print('run ended properly!')

    print(datetime.datetime.now().strftime("%Y-%m-%d-%H-%M"))
    blindspot.autoDraw = False

    #!!# stop recording

    tracker.stopcollecting()
    tracker.closefile()
    tracker.shutdown()


    ## last screen
    visual.TextStim(win,'Run ended.', height = letter_height, color = 'black').draw()
    win.flip()
    k = event.waitKeys() # this is an appropriate use of 'waitKeys()' the rest might be better done with 'getKeys()'? not sure...

    #!!# close eye-tracker (eye-tracker object requires the window object - which should also be closed... but only after this last message)
    win.close()


if __name__ == "__main__":
    doDistUpScaledAsynchronousTask()