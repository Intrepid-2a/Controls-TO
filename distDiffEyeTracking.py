import sys
import warnings
import numbers
import numpy as np
import time
import math
import os
import json
import copy
import random
import re

from glob import glob

from mypsycho import *


# to test if input objects are valid psychopy classes:
# import psychopy

# mouse dummy needs a psychopy.event.mouse object
# calibration requires a psychopy.visual.Window
# and psychopy.visual.*Stim (circleStim?)
# from psychopy import core, event, visual, gui, monitors

# from psychopy.tools import monitorunittools
from psychopy.tools.coordinatetools import pol2cart, cart2pol
# from psychopy.hardware import keyboard
# from pyglet.window import key

# import sys, os
# sys.path.append(os.path.join('..', 'EyeTracking'))
# from EyeTracking import EyeTracker



# this file has just 1 object that is needed: EyeTracker
# for now, it can be used as:
# -  from EyeTracker import EyeTracker
# -  myEyeTracker = EyeTracker(tracker='LiveTrack', trackEyes=[True,True], fixationWindow=2, psychopyWindow=cfg['hw']['win'])
# I could set up the folder to work like a proper Python module later where that is taken care of


class EyeTracker:

    def __init__(self, 
                 tracker=None, 
                 trackEyes=[False, False], 
                 fixationWindow=None,
                 minFixDur=None,
                 fixTimeout=None,
                #  psychopyWindow=None, NO PsychoPy window!
                 filefolder=None, 
                 filename=None,
                 samplemode=None,
                 calibrationpoints=5,
                 colors=None,
                 fixationStimuli=None):


        # the functions below check the user input,
        # and store it for future use if OK
        # they can also be used later on to change how the object works
        # and are supposed to be device-agnostic

        # self.setPsychopyWindow(psychopyWindow) # NO PsychoPy window
        self.setCalibrationpoints(calibrationpoints)
        self.setColors(colors)
        # self.setEyetracker(tracker) # we ONLY keep the liveTrack functions
        self.trackEyes(trackEyes)
        self.setFixationWindow(fixationWindow)
        self.setMinFixDur(minFixDur)
        self.setFixTimeout(fixTimeout)
        self.setFilePath(filefolder, filename)
        self.setSamplemode(samplemode)
        self.setFixationStimuli(fixationStimuli)

        # things below this comment are still up for change... depends a bit on how the EyeLink does things

        # maybe these should be a property that has a function to set it?
        # it's only used for the LiveTrack, so probably not...
        # self.__calibrationTargets = np.array([[0,0],   [-3,0],[0,3],[3,0],[0,-3],     [6,6],[6,-6],[-6,6],[-6,-6]])
        
        # print(filefolder)
        # print(filename)
        # print(self.storefiles)
        
        self.__fileOpen = False
        self.__recording = False

        self.__EL_currentfile = ''
        self.__EL_downloadFiles = []

        self.__N_calibrations = 0
        self.__N_rawdatafiles = 0

        # self.__createTargetStim() # no actual stimuli !




    # def setEyetracker(self, tracker):
    #     if isinstance(tracker, str):
    #         if tracker in ['eyelink', 'livetrack', 'mouse']:

    #             if tracker == 'eyelink':
    #                 # set up the eyelink device here
    #                 self.setupEyeLink()

    #             if tracker == 'livetrack':
    #                 # set up the livetrack device here
    #                 self.setupLiveTrack()

    #             if tracker == 'mouse':
    #                 # not sure what to do here
    #                 self.setupMouse()

    #             self.tracker = tracker
    #         else:
    #             raise Warning("unkown eye-tracker: %s"%(tracker))
    #     else:
    #         raise Warning("tracker must be a string")

    def trackEyes(self, trackEyes):
        if isinstance(trackEyes, list):
            if len(trackEyes) == 2:
                if all([isinstance(x, bool) for x in trackEyes]):
                    if any(trackEyes):
                        self.trackEyes = trackEyes
                    else:
                        raise Warning("one or both eyes must be tracked")
                else:
                    raise Warning("trackEyes must only contain booleans")
            else:
                raise Warning("trackEyes must have length 2")
        else:
            raise Warning("trackEyes must be a list")

    def setFixationWindow(self, fixationWindow):
        if isinstance(fixationWindow, numbers.Number):
            if fixationWindow > 0:
                self.fixationWindow = fixationWindow
            else:
                raise Warning("fixationWindow must be larger than 0")
        else:
            raise Warning("fixationWindow must be a number")

    def setMinFixDur(self, minFixDur):
        if isinstance(minFixDur, numbers.Number):
            if minFixDur > 0:
                self.minFixDur = minFixDur
            else:
                raise Warning("minimum fixation duration must be larger than 0")
        else:
            raise Warning("minimum fixation duration must be a number")


    def setFixTimeout(self, fixTimeout):
        if isinstance(fixTimeout, numbers.Number):
            if fixTimeout > self.minFixDur:
                self.fixTimeout = fixTimeout
            else:
                raise Warning("fixation timeout must be larger than minimum fixation duration")
        else:
            raise Warning("fixation timeout must be a number")



    def setPsychopyWindow(self, psychopyWindow):
        print('set psychopy window')
        return
        # if isinstance(psychopyWindow, psychopy.visual.window.Window):
        #     if psychopyWindow.units == 'deg':
        #         self.psychopyWindow = psychopyWindow
        #     else:
        #         raise Warning("psychopyWindow must have units set to 'deg'")
        # else:
        #     raise Warning("psychopyWindow must be a psychopy Window")


    def setFilePath(self, filefolder, filename):
        # self.storefiles = False
        # self.filefolder = None
        # self.filename = None

        self.storefiles  = True
        self.filefolder  = filefolder
        self.filename    = filename

        return

        # everything below this line is irrelevant:
        print('this line in SETFILEPATH should not be printed')

        # if isinstance(filefolder, str):
        #     if len(filefolder) > 0:
        #         # self.storefiles = False
        #         # check if it is an existing path
        #         if os.path.isdir(filefolder):
        #             if isinstance(filename, str):
        #                 if len(filename) > 0:

        #                     # check if target file already exists:
        #                     if len(glob(os.path.join(filefolder, filename + '.*'))):
        #                         y = 1
        #                         while len(glob(os.path.join(filefolder, filename + '_' + str(y) + '.*'))):
        #                             y += 1
        #                         filename = filename + '_' + str(y)
        #                         print('NOTE: target eye-tracking data file already exists, changing to: '+filename)

        #                     self.storefiles  = True
        #                     self.filefolder  = filefolder
        #                     self.filename    = filename
        #                 else:
        #                     print('NOTE: not storing any data since filename is an empty string')
        #             else:
        #                 print('NOTE: not storing any data since filename is not a string')
        #         else:
        #             raise Warning("filefolder is not a valid or existing path: %s"%(filefolder))
        #     else:
        #         print('NOTE: not storing any files since filefolder is an empty string')
        # else:
        #     print('NOTE: not storing any files since filefolder is not a string')
        

    def setSamplemode(self, samplemode):
        if isinstance(samplemode, str):
            if samplemode in ['both', 'left', 'right', 'average']:
                self.samplemode = samplemode
            else:
                raise Warning("unkown samplemode: %s"%(samplemode))
        else:
            raise Warning("samplemode must be a string")



    def setCalibrationpoints(self, calibrationpoints):
        if isinstance(calibrationpoints, numbers.Number):
            if calibrationpoints in [5,9]:
                # allowed number of points?
                self.calibrationpoints = calibrationpoints
                if calibrationpoints == 5:
                    self.__calibrationTargets = np.array([[0,0],   [-3,0],[0,3],[3,0],[0,-3]                                 ])
                    # self.__calibrationTargets = np.array([[0,0],   [-10.437,0],[0,5.916],[10.437,0],[0,-5.916]                                 ])
                if calibrationpoints == 9:
                    self.__calibrationTargets = np.array([[0,0],   [-3,0],[0,3],[3,0],[0,-3],     [6,6],[6,-6],[-6,6],[-6,-6]])
                    # self.__calibrationTargets = np.array([[0,0],   [-10.437,0],[0,5.916],[10.437,0],[0,-5.916],     [2*10.437,2*5.916],[2*10.437,-2*5.916],[-2*10.437,2*5.916],[-2*10.437,-2*5.916]  ])
                # print(self.__calibrationTargets)
            else:
                raise Warning("calibration points must be 5 (default) or 9")
        else:
            raise Warning("calibration points must be a number")


        # eyetracker_config['calibration'] = dict(type='THIRTEEN_POINTS')

    def setColors(self, colors):

        # print(colors)

        if isinstance(colors, dict):
            # no more checks for now, but should check that it has at least col_back: used for eyelink calibration...
            self.colors = colors
        else:
            raise Warning("colors should be a dictionary")

        # print(self.colors)

    def setFixationStimuli(self, fixationStimuli):
        print('set fixation stimuli')
        return

        # if not fixationStimuli == None:
        #     # make sur eit's a list:
        #     if not isinstance(fixationStimuli, list):
        #         fixationStimuli = [fixationStimuli]
        #     for stim in fixationStimuli:
        #         if hasattr(stim, 'draw'): 
        #             if callable(stim.draw):
        #                 if stim.win == self.psychopyWindow:
        #                     # seems good?
        #                     pass
        #                 else:
        #                     raise Warning("fixationStimuli must be defined for 'psychopyWindow'")
        #             else:
        #                 raise Warning("fixationStimuli.draw must be callable")
        #         else:
        #             raise Warning("fixationStimuli must have a draw property")
        #     # all good, store them:
        #     self.fixationStimuli = fixationStimuli
        # else:
        #     pass # it's fine not to specify any



    # def setupLiveTrack(self):
    #     import LiveTrack
    #     self.LiveTrack = LiveTrack

    #     # remap functions:
    #     self.initialize = self.__LT_initialize
    #     self.calibrate  = self.__LT_calibrate
    #     self.savecalibration = self.__LT_savecalibration

    #     self.lastsample = self.__LT_lastsample

    #     self.openfile = self.__LT_openfile
    #     self.startcollecting = self.__LT_startcollecting
    #     self.stopcollecting = self.__LT_stopcollecting
    #     self.closefile = self.__LT_closefile

    #     self.comment = self.__LT_comment
    #     self.shutdown = self.__LT_shutdown
        # ...
        # here we map other functions
        # ...



    # functions to initialize each device:
    # region



    def initialize(self, calibrationPoints=None):
        print('initialize LiveTrack')
        self.__calibrationTargets = calibrationPoints
        return

        # everything below is irrelevant:
        print('this line in INITIALIZE() should not be printed')

        # self.LiveTrack.Init()

        # Start LiveTrack using raw data (camera coords)
        # self.LiveTrack.SetResultsTypeRaw()

        # Start buffering data
        # self.LiveTrack.StartTracking()
        # self.LiveTrack.SetTracking(leftEye=self.trackEyes[0],rightEye=self.trackEyes[1])

        # what's this for?
        # [ width, height, sampleRate, offsetX, offsetY ] = self.LiveTrack.GetCaptureConfig()
        # self.__LiveTrackConfig = { 'width'      : width,
        #                            'height'     : height,
        #                            'sampleRate' : sampleRate,
        #                            'offsetX'    : offsetX,
        #                            'offsetY'    : offsetY      }

        # these checks can be much simpler! but leave it be for now...
        if isinstance(calibrationPoints, np.ndarray):
            if len(calibrationPoints) >= 3:
                if all([isinstance(x, np.ndarray) and len(x) == 2 for x in calibrationPoints]):
                    if all([len(x) == 2 for x in calibrationPoints]):
                        if all([all([isinstance(y, numbers.Number) for y in x]) for x in calibrationPoints]):
                            # seems more or less OK?
                            self.__calibrationTargets = calibrationPoints
                        else:
                            raise Warning("all elements in calibrationPoints must be numeric")
                    else:
                        raise Warning("all rows in calibrationPoints must have 2 items")
                else:
                    raise Warning("all rows in calibrationPoints must be numpy.ndarray")
            else:
                raise Warning("calibrationPoints must have at least 3 rows")
        else:
            if calibrationPoints == None:
                return
            else:
                raise Warning("calibrationPoints must be a numpy.ndarray")


        

    # endregion


    # functions to calibrate each device:
    # region


    def calibrate(self):

        calTargets = copy.deepcopy(self.__calibrationTargets)


        mididx = list(range(1,len(calTargets)))
        random.shuffle(mididx)

        # everything past this line is irrelevant:

        return


        print('this line in CALIBRATE() should NOT be printed')

        allidx = [0] + mididx + [0]
        ntargets = len(allidx)


        # configure calibration:
        setupDelay = 1000.0 # time before collecting any samples in ms
        minDur = 300 # min fixation duration in ms
        fixTimeout = 5  # timeout duration in seconds (point is skipped!)
        fixThreshold = 5 # pixel window for all samples within a 'fixation'

        # ntargets = np.shape(self.__calibrationTargets)[0]
        # tgtLocs = self.__calibrationTargets.astype(float) 
        tgtLocs = copy.deepcopy(self.__calibrationTargets)
        tgtLocs = tgtLocs[allidx,:]
        tgtLocs = tgtLocs.astype(float) # make sure locations are floats





        self.LiveTrack.SetResultsTypeRaw() # stream raw data
        # self.LiveTrack.StartTracking() # buffer data to lib
        [ width, height, sampleRate, offsetX, offsetY ] = self.LiveTrack.GetCaptureConfig() # estimate sample rate
        fixDurSamples = round((float(minDur)/1000)*float(sampleRate)) # samples per fixation duration

        self.LiveTrack.SetTracking(self.trackEyes[0], self.trackEyes[1]) # make sure we're only tracking the requires eyes
        # print(self.LiveTrack.GetTracking()) # see what's being tracked

        if self.trackEyes[0]:
            VectXL = [None] * ntargets
            VectYL = [None] * ntargets
            GlintXL = [None] * ntargets
            GlintYL = [None] * ntargets
        if self.trackEyes[1]:
            VectXR = [None] * ntargets
            VectYR = [None] * ntargets
            GlintXR = [None] * ntargets
            GlintYR = [None] * ntargets

        # visual.TextStim(self.psychopyWindow,'calibration', height = 1,wrapWidth=30, color = 'black').draw()
        # self.psychopyWindow.flip()
        time.sleep(0.3333) # is this necessary? well, we just show this briefly, so the participant knows what's going to happen

        for target_idx in range(ntargets):

            targetpos = tgtLocs[target_idx]

            self.target.pos = targetpos
            self.target.draw()

            # self.psychopyWindow.flip()

            # This flag will be set to true when a valid fixation has been acquired
            gotFixLeft = 0  
            gotFixRight = 0
            
            t0 = time.time() # reset fixation timer 
        
            # Loop until fixation data has been aquired for this dot (or timed out) 
            while 1:
                d = self.LiveTrack.GetBufferedEyePositions(0,fixDurSamples,0)

                if self.trackEyes[0]:

                    VectX = self.LiveTrack.GetFieldAsList(d,'VectX')
                    VectY = self.LiveTrack.GetFieldAsList(d,'VectY')
                    GlintX = self.LiveTrack.GetFieldAsList(d,'GlintX')
                    GlintY = self.LiveTrack.GetFieldAsList(d,'GlintY')
                    Tracked = self.LiveTrack.GetFieldAsList(d,'Tracked')

                    # Calculate the maximum difference in the pupil-to-glint 
                    # vectors for the samples in the buffer, for left eye
                    pgDistL = max([max(VectX)-min(VectX),max(VectY)-min(VectY)])

                    # Check if the maximum vector difference is within the defined
                    # limit for a fixation (fixWindow) and all samples ajsone tracked, and
                    # the time to wait for fixations (waitTimeForFix) has passed, for
                    # the left eye
                    if pgDistL<=fixThreshold and np.all(Tracked) and (time.time()-t0)>setupDelay/1000:
                        # Check if there are enough samples in the buffer for the
                        # defined duration (fixDurSamples)
                        if len(d)>=fixDurSamples and gotFixLeft==0:
                            # save the data for this fixation
                            VectXL[target_idx] = np.median(VectX)
                            VectYL[target_idx] = np.median(VectY)
                            GlintXL[target_idx] = np.median(GlintX)
                            GlintYL[target_idx] = np.median(GlintY)
                            print('Fixation #',str(target_idx+1),str(targetpos),': Found valid fixation for left eye')
                            gotFixLeft = 1 # good fixation aquired
                
                if self.trackEyes[1]:
                    VectXRight = self.LiveTrack.GetFieldAsList(d,'VectXRight')
                    VectYRight = self.LiveTrack.GetFieldAsList(d,'VectYRight')
                    GlintXRight = self.LiveTrack.GetFieldAsList(d,'GlintXRight')
                    GlintYRight = self.LiveTrack.GetFieldAsList(d,'GlintYRight')
                    TrackedRight = self.LiveTrack.GetFieldAsList(d,'TrackedRight')
                
                    # and for the right eye
                    pgDistR = max([max(VectXRight)-min(VectXRight),max(VectYRight)-min(VectYRight)])


                    # and for the right eye
                    if pgDistR<=fixThreshold and np.all(TrackedRight) and (time.time()-t0)>setupDelay/1000:
                        # Check if there are enough samples in the buffer for the
                        # defined duration (fixDurSamples)
                        if  len(d)>=fixDurSamples and gotFixRight==0:
                            # save the data for this fixation
                            VectXR[target_idx] = np.median(VectXRight)
                            VectYR[target_idx] = np.median(VectYRight)
                            GlintXR[target_idx] = np.median(GlintXRight)
                            GlintYR[target_idx] = np.median(GlintYRight)
                            print('Fixation #',str(target_idx+1),str(targetpos),': Found valid fixation for right eye')
                            gotFixRight = 1 # good fixation aquired
                

                if (time.time()-t0)>fixTimeout:
                    if not gotFixLeft and self.trackEyes[0]>0:
                        print('Fixation #',str(target_idx+1),str(targetpos),': Did not get fixation for left eye (timeout)')
                    if not gotFixRight and self.trackEyes[1]>0:
                        print('Fixation #',str(target_idx+1),str(targetpos),': Did not get fixation for right eye (timeout)')
                    break # fixation timed out

                
                # Exit if all eyes that are enabled have got a fixation
                if (gotFixLeft or self.trackEyes[0]==False) and (gotFixRight or self.trackEyes[1]==False):
                    # self.psychopyWindow.flip()
                    break

        # Stop buffering data to the library
        ######################################################### NOT SURE ABOUT THIS:

        # self.LiveTrack.StopTracking()

        # Clear the data in the buffer
        self.LiveTrack.ClearDataBuffer()


        # viewDist = self.psychopyWindow.monitor.getDistance()

        redoCalibration = False

        # %% remove failed fixations from data

        if self.trackEyes[0]:
            # left eye
            failedFixL = []
            for i in range(0,len(VectXL)):
                if VectXL[i] is None:
                    failedFixL.append(i)
            
            # %% remove failed fixations from data
            VectXL = np.delete(VectXL, failedFixL).tolist()
            VectYL = np.delete(VectYL, failedFixL).tolist()
            GlintXL = np.delete(GlintXL, failedFixL).tolist()
            GlintYL = np.delete(GlintYL, failedFixL).tolist()
            tgtLocsXL = np.delete(tgtLocs[:,0], failedFixL).tolist()
            tgtLocsYL = np.delete(tgtLocs[:,1], failedFixL).tolist()

            if len(tgtLocsXL) < 2:
                print('left eye calibration fewer than 3 good points: redoing calibration')
                redoCalibration = True
            else:
                # %% send fixation data to LiveTrack to calibrate
                calErrL = self.LiveTrack.CalibrateDevice(0, len(tgtLocsXL), tgtLocsXL, tgtLocsYL, VectXL, VectYL, viewDist, np.median(GlintXL), np.median(GlintYL))
                print('Left eye calibration accuraccy: ',str(math.sqrt(float(calErrL)/len(tgtLocsXL))), 'errors in dva')


        if self.trackEyes[1]:
            # right eye
            failedFixR = []
            for i in range(0,len(VectXR)):
                if VectXR[i] is None:
                    failedFixR.append(i)

            # %% remove failed fixations from data
            VectXR = np.delete(VectXR, failedFixR).tolist()
            VectYR = np.delete(VectYR, failedFixR).tolist()
            GlintXR = np.delete(GlintXR, failedFixR).tolist()
            GlintYR = np.delete(GlintYR, failedFixR).tolist()
            tgtLocsXR = np.delete(tgtLocs[:,0], failedFixR).tolist()
            tgtLocsYR = np.delete(tgtLocs[:,1], failedFixR).tolist()
            
            if len(tgtLocsXR) < 2:
                print('right eye calibration fewer than 3 good points: redoing calibration')
                redoCalibration = True
            else:
                calErrR = self.LiveTrack.CalibrateDevice(1, len(tgtLocsXR), tgtLocsXR, tgtLocsYR, VectXR, VectYR, viewDist, np.median(GlintXR), np.median(GlintYR))
                print('Right eye calibration accuraccy: ',str(math.sqrt(float(calErrR)/len(tgtLocsXR))), 'errors in dva')
        

        if redoCalibration:

            # redo_text = visual.TextStim(win = self.psychopyWindow,
            #                             'not enough fixations detected\n\nadjust eye-tracker?\n\n    press  [ SPACE ]\nto redo calibration')
            # visual.TextStim(self.psychopyWindow,'not enough fixations detected\n\nadjust eye-tracker?\n\n    press  [ SPACE ]\nto redo calibration', height = 1,wrapWidth=30, color = 'black').draw()
            # redo_text.draw()
            # self.psychopyWindow.flip()

            k=[]
            while k[0] not in ['q','space']:
                k = event.waitKeys()
            event.clearEvents(eventType='keyboard')

            self.calibrate() # this somehow doesn't work...
            
        else:

            self.LiveTrack.SetResultsTypeCalibrated()
            # self.LiveTrack.StartTracking()

            if self.storefiles:
                
                cal_files = glob( os.path.join(self.filefolder, 'calibration_*.json' ) )
                if len(cal_files):
                    idx = np.max([int(os.path.splitext(os.path.basename(x))[0].split('_')[1]) for x in cal_files]) + 1
                else:
                    idx = 1

                self.__N_calibrations = idx
                self.comment('calibration %d'%(self.__N_calibrations))

                self.savecalibration()

    
    # endregion


    def savecalibration(self):

        print('save calibration')
        return

        # # collect calibration info in a dictionary:
        # calibrations = {}
        # if self.trackEyes[0]:
        #     calibrations['left']  = self.LiveTrack.GetCalibration(eye=0)
        # if self.trackEyes[1]:
        #     calibrations['right'] = self.LiveTrack.GetCalibration(eye=1)

        # # write calibration info to a json file:
        # filename = '%s/calibration_%s.json'%(self.filefolder, self.__N_calibrations)
        # out_file = open(filename, "w")
        # json.dump( calibrations,
        #            fp=out_file,
        #            indent=4)
        # out_file.close()

    
    # endregion


    # function to open new raw data file
    # region



    def openfile(self):
        
        print('opening file')
        return

        # # maybe this should also be done at the level of the whole session?
        # # yes!

        # if self.__fileOpen:
        #     self.closefile()
        #     print('note: closed open file before opening a new file')

        # # filename = self.saneFilename(self.filename, ext='.csv')


        # print(os.path.join(self.filefolder,self.filename)+'.csv')
        # self.LiveTrack.SetDataFilename(os.path.join(self.filefolder,self.filename)+'.csv')

        # self.__fileOpen = True
        # self.__N_rawdatafiles += 1


    # def saneFilename(self, filename, ext):

    #     if filename == None:
    #         filename = 'raw_%d%s'%(self.__N_rawdatafiles+1, ext)
    #     else:
    #         if isinstance(filename, str):
    #             if len(filename) > 0:
    #                 if not(os.path.isfile(filename)):
    #                     file_path, file_ext = os.path.splitext(filename)
    #                     if not(file_ext in [ext,ext.upper()]):
    #                         file_ext = '.csv'
    #                         filename = file_path + file_ext
    #                         print("changed file extention to '.csv'")
    #                     if len(os.path.dirname(filename)) > 0:
    #                         filename = os.path.basename(filename)
    #                         print('storing in designated folder: path removed from filename')
    #                 else:
    #                     raise Warning('file already exists')
    #             else:
    #                 raise Warning('filename should have non-zero length')
    #         else:
    #             raise Warning('filename should be a string')

    #     return(filename)

    # endregion


    # function to start collecting raw data
    # region

    def startcollecting(self):
        print('start collecting')
        return
        # self.LiveTrack.StartTracking()

    # endregion


    # function to stop collecting raw data
    # region


    def stopcollecting(self):
        print('stop collecting')
        return
        # self.LiveTrack.StopTracking()


    # endregion

    # function to close existing raw data file
    # region

            

    def closefile(self):
        print('close file')
        return
        # if self.__fileOpen:
        #     self.LiveTrack.CloseDataFile()
        #     self.__fileOpen = False
        # else:
        #     print('no file to close, moving on')


    # endregion


    # the following functions are used during the experiment:

    # get the last sample from the specified tracker:
    # region




    def lastsample(self):
        print('get last sample')
        return
        # data = LiveTrack.GetBufferedEyePositions(0,fixDurSamples,0) # this would get the last x samples, given by the second argument
        # data = self.LiveTrack.GetLastResult() # gets only the very last sample

        # # this needs to be formatted in some standard way that is the same for all eye-tracker devices
        # sample = {}
        # if self.samplemode in ['both','left','average']:
        #     if self.trackEyes[0]:
        #         if data.Tracked:
        #             sample['left'] = np.array([data.GazeX, data.GazeY])
        #         else:
        #             sample['left'] = np.array([np.NaN, np.NaN])
        # if self.samplemode in ['both','right','average']:
        #     if self.trackEyes[1]:
        #         if data.TrackedRight:
        #             sample['right'] = np.array([data.GazeXRight, data.GazeYRight])
        #         else:
        #             sample['right'] = np.array([np.NaN, np.NaN])

        # if self.samplemode == 'average':
        #     X = []
        #     Y = []
        #     # skip NAN values?
        #     if data.Tracked:
        #         X.append(sample['left'][0])
        #         Y.append(sample['left'][1])
        #     if data.TrackedRight:
        #         X.append(sample['right'][0])
        #         Y.append(sample['right'][1])
        #     if (any([data.Tracked, data.TrackedRight])):
        #         sample['average'] = np.array([np.mean(X), np.mean(Y)])

        # return(sample)



    # endregion


    def gazeInFixationWindow(self):


        # sample = self.lastsample()
        # check_samples = self.getSamplesToCheck()
        
        # for cs in check_samples: # skipping irrelevant sample types
        #     if cs in sample.keys():
        #         if any(np.isnan(sample[cs])):
        #             return(False) # return False if there is a nan value
        #         d = np.sqrt(np.sum(np.array(sample[cs])**2))
        #         if d > self.fixationWindow:
        #             return(False) # return false if the distance from fixation is larger than 2 (or whatever the fixation window is)
        #     else:
        #         return(False) # return false if any of the samples that need to be checked are not in the data

        return(True) # should only get here if all samples exist, are not nans, and are within the fixation window



    def getSamplesToCheck(self):
        pass

        # return( {'both':['left','right'],
        #          'left':['left'],
        #          'right':['right'],
        #          'average':['average']}[self.samplemode] )

    def waitForFixation(self, minFixDur=None, fixTimeout=None, fixationStimuli=None):
        return True

        # if minFixDur == None:
        #     minFixDur = self.minFixDur
        # if fixTimeout == None:
        #     fixTimeout = self.fixTimeout

        # if fixationStimuli == None:
        #     if hasattr(self, 'fixationStimuli'):
        #         fixationStimuli = self.fixationStimuli
        #     else:
        #         self.target.pos = [0,0]
        #         fixationStimuli = [self.target]
        # else:
        #     if not isinstance(fixationStimuli, list):
        #         fixationStimuli = [fixationStimuli]
        

        # # most the initially set values should be used, but we do 1 sanity check here:
        # # if the initially set values are used, this should already be true:
        # if fixTimeout < minFixDur:
        #     raise Warning("fixation timeout should be longer than minimum fixation duration")

        # starttime = time.time()
        # timeout = starttime + fixTimeout
        # now = starttime

        # fixationStart = None

        # while now < timeout:

        #     for stim in fixationStimuli:
        #         stim.draw()
        #     self.psychopyWindow.flip()

        #     now = time.time()

        #     fixated = self.gazeInFixationWindow()

        #     if fixated:
        #         if fixationStart == None:
        #             fixationStart = now
        #         else:
        #             if (now - fixationStart) >= minFixDur:
        #                 return True
        #     else:
        #         fixationStart = None
        
        # return False





    # insert a comment into the raw data file storing tracker data:
    # region



    def comment(self, comment):
        pass

        # if self.__fileOpen:
        #     self.LiveTrack.SetDataComment(comment)
        #     time.sleep(1.5/self.__LiveTrackConfig['sampleRate'])

        # the experiment sleeps for 1.5 eye-tracker samples
        # this ensures actually storing the comment
        # and doesn't get overwritten by the next comment... at the same sample (shouldn't send comments that quickly?)
        # and we might skip 1 sample, but that will be less than 1 frame




    # endregion





    # functions to close the eye-tracker
    # region



    def shutdown(self):
        return

        self.stopcollecting()
        self.closefile()
        self.LiveTrack.Close()


    # endregion



    # this runs shutdown on garbage collection
    # which could be much later then expected
    # it's to make sure it gets done at some point
    # especially since it renames/moves eyelink data files now
    # def __del__(self):
    #     self.shutdown()


    # def __createTargetStim(self):
        
    #     # should these be accessible / changeble by the user?
    #     fixDotInDeg  = 0.2 # inner circle
    #     fixDotOutDeg = 1.0
        
    #     self.target = visual.TargetStim(self.psychopyWindow, 
    #                                     name='fixTarget',
    #                                     radius=fixDotOutDeg/2, 
    #                                     innerRadius=fixDotInDeg/2, 
    #                                     fillColor=[-1,-1,-1], 
    #                                     innerFillColor=[1,1,1], 
    #                                     lineWidth=0, 
    #                                     innerLineWidth=0, 
    #                                     borderColor=None, 
    #                                     innerBorderColor=None,
    #                                     units='deg')



def localizeSetup( trackEyes, filefolder, filename, location=None, glasses='RG', colors=None, task=None, ID=None, noEyeTracker=False, offset=[0,0] ):
    
    # sanity checks on trackEyes, filefolder and filename are done by the eyetracker object

    # sanity check on location argument
    if location == None:
        raise Warning("set location to a string: Glasgow or Toronto")
    if isinstance(location, str):
        if location in ['Toronto', 'toronto', 'tor', 'TOR', 't', 'T', 'YYZ']:
            location = 'toronto'
        if location in ['Glasgow', 'glasgow', 'gla', 'GLA', 'g', 'G', 'EGPF']:
            location = 'glasgow'
    else:
        raise Warning("set location to a string: Glasgow or Toronto")



    # RED/GREEN COLORS

    if colors == None:
        colors = {}

    # sanity check on glasses argument, and picking back-ground color
    if isinstance(glasses, str):
        if glasses in ['RG', 'RB']:
            if glasses == 'RG':
                if location == 'glasgow':
                    colors['back']   = [ 0.55,  0.45, -1.00] 
                    colors['red']    = [ 0.55, -1.00, -1.00]
                    colors['blue']   = [-1.00,  0.45, -1.00]
                if location == 'toronto':
                    colors['back']   = [ 0.5,  0.5, -1.0 ]
                    colors['red']    = [ 0.5, -1.0, -1.0 ]
                    colors['blue']   = [-1.0,  0.5, -1.0 ]
            if glasses == 'RB':
                # this should no longer be used:
                print('are you sure about using RED/BLUE glasses?')
                colors['back']   = [ 0.5, -1.0,  0.5]
                colors['red']    = [ 0.5, -1.0, -1.0]
                colors['blue']   = [-1.0, -1.0,  0.5] 
        else:
            raise Warning('glasses should be RG (default) or RB')
    else:
        raise Warning('glasses should be a string')

    # CALIBRATED COLORS:

    # for blind spot mapping, task == None, but it still needs the calibrated colors...
    # handle this in the function?

    colors = getColors(colors=colors, 
                       task=task, 
                       ID=ID)

    # WINDOW OBJECT

    if location == 'glasgow':
        # not a calibrated monitor?
        gammaGrid = np.array([ [  0., 1.0, 1.0, np.nan, np.nan, np.nan  ],
                               [  0., 1.0, 1.0, np.nan, np.nan, np.nan  ],
                               [  0., 1.0, 1.0, np.nan, np.nan, np.nan  ],
                               [  0., 1.0, 1.0, np.nan, np.nan, np.nan  ]  ], dtype=np.float32)

        resolution = [1920, 1080] # in pixels
        size       = [60, 33.75] # in cm
        distance   = 57 # in cm
        screen     = 1 # index on the system: 0 = first monitor, 1 = second monitor, and so on

        tracker = 'eyelink'


    if location == 'toronto':
        # color calibrated monitor:
        gammaGrid = np.array([ [  0., 135.44739,  2.4203537, np.nan, np.nan, np.nan  ],
                               [  0.,  27.722954, 2.4203537, np.nan, np.nan, np.nan  ],
                               [  0.,  97.999275, 2.4203537, np.nan, np.nan, np.nan  ],
                               [  0.,   9.235623, 2.4203537, np.nan, np.nan, np.nan  ]  ], dtype=np.float32)

        resolution = [1920, 1080] # in pixels
        size       = [59.8, 33.6] # in cm
        distance   = 49.53 # in cm
        screen     = 1  # index on the system: 0 = first monitor, 1 = second monitor, and so on

        tracker = 'livetrack'


    # mymonitor = monitors.Monitor(name='temp',
    #                              distance=distance,
    #                              width=size[0])
    # if location == 'toronto':
    #     mymonitor.setGammaGrid(gammaGrid)
    # mymonitor.setSizePix(resolution)

    #win = visual.Window([1000, 500], allowGUI=True, monitor='ccni', units='deg', fullscr=True, color = back_col, colorSpace = 'rgb')
    # win = visual.Window(resolution, monitor=mymonitor, allowGUI=True, units='deg', fullscr=True, color=colors['back'], colorSpace = 'rgb', screen=screen)
            # size = [34.5, 19.5]filefolder,

    # fixation = visual.ShapeStim(win, 
    #                             vertices = ((0, -1), (0, 1), (0,0), (-1, 0), (1, 0)), 
    #                             lineWidth = 5, 
    #                             units = 'deg', 
    #                             size = (1, 1), # might be too small?
    #                             closeShape = False, 
    #                             lineColor = [-1.0, -1.0, -1.0]) # close to col_both?

    # fixation_x = visual.ShapeStim(win, 
    #                               vertices = ((0, -1), (0, 1), (0,0), (-1, 0), (1, 0)), 
    #                               lineWidth = 5, 
    #                               units = 'deg', 
    #                               size = (1, 1), # might be too small?
    #                               closeShape = False, 
    #                               lineColor = [-1.0, -1.0, -1.0], # close to col_both?
    #                               ori = 45)

    # if 'both' in colors.keys():
    #     fixation.lineColor = colors['both']
    #     fixation_x.lineColor = colors['both']


    if not any(trackEyes):
        tracker = 'mouse'
        trackEyes = [True, False]

    print(filefolder)

    if noEyeTracker:
        ET = None
    else:
        ET = EyeTracker(tracker           = tracker,
                        trackEyes         = trackEyes,
                        fixationWindow    = 2.0,
                        minFixDur         = 0.2,
                        fixTimeout        = 3.0,
                        # psychopyWindow    = win,
                        filefolder        = filefolder,
                        filename          = filename,
                        samplemode        = 'average',
                        calibrationpoints = 5,
                        colors            = colors )

        if location == 'toronto':
            if not tracker == 'mouse':
                # this is where the calibrationPoints come from...
                ET.initialize(calibrationPoints = np.array([[0,0],   [-10.437,0],[0,5.916],[10.437,0],[0,-5.916]                                 ]) )
            else:
                ET.initialize()
        else:
            if location == 'glasgow':
                ET.initialize(calibrationScale=(0.35, 0.35))
            else:
                ET.initialize()

    fcols = [[-1,-1,-1],[1,1,1]]
    if 'both' in colors.keys():
        fcols[0] = colors['both']
    if 'back' in colors.keys():
        fcols[1] = colors['back']

    if task in ['area', 'curvature', 'orientation', 'distCentred']:
        fusion = {'hi': fusionStim(
                                #    win    = win,
                                   rows    = 9,
                                   columns = 2,
                                   pos    = [0,15],
                                   colors = fcols),
                  'lo': fusionStim(
                                #    win    = win,
                                   rows    = 2,
                                   columns = 9,
                                   pos    = [0,-15],
                                   colors = fcols)}

    if task in ['distRotated','distUpturned','distUpshifted']:
        print('rotated fusion stims')
        fusion = {'hi': fusionStim(
                                #    win    = win,
                                   rows    = 11,
                                   columns = 2,
                                   pos    = [0,15],
                                   colors = fcols),
                  'lo': fusionStim(
                                #    win    = win,
                                   rows    = 3,
                                   columns = 2,
                                   pos    = [0,-5],
                                   colors = fcols)}

    if task in ['distHorizontal','distBinocular','distance', 'distScaled', 'distAsynchronous', 'distScaledAsynchronous']:

        fusion = {'hi': fusionStim(
                                #    win    = win,
                                   pos    = [0,7],
                                   colors = fcols),
                  'lo': fusionStim(
                                #    win    = win,
                                   pos    = [0,-7],
                                   colors = fcols)}



    # color calibration doesn't use any of this (except the window object?)
    # for either calibration task, the task should not be set
    # which returns an empty dictionary
    blindspotmarkers = makeBlindSpotMarkers(
        # win=False, 
        task=task, 
        ID=ID, 
        colors=colors)

    # print(blindspotmarkers)

    paths = {} # worst case, we return an empty dictionary?
    if not task == None:
        paths['data']         = os.path.join('..', 'data', task )
        paths['color']        = os.path.join('..', 'data', task, 'color' )
        paths['mapping']      = os.path.join('..', 'data', task, 'mapping' )
        paths['eyetracking']  = os.path.join('..', 'data', task, 'eyetracking', ID )
        for p in paths.keys():
            if not os.path.exists(paths[p]):
                os.makedirs(paths[p], exist_ok = True)

    


    return( {'win'              : False,
             'tracker'          : ET,
             'colors'           : colors,
             'fusion'           : fusion,
             'fixation'         : False,
             'fixation_x'       : False,
             'blindspotmarkers' : blindspotmarkers,
             'paths'            : paths } )

def getColors(colors={}, task=None, ID=None):

    if task == None:
        print('warning: task must be specified to read calibrated colors, skipping')
        return(colors)

    if ID == None:
        print('warning: ID must be specified to read calibrated colors, skipping')
        return(colors)

    ## colour (eye) parameters
    all_files = glob('../data/' + task + '/color/' + ID + '_col_cal*.txt')
    if len(all_files) == 0:
        # no color calibration done, skip
        print('NO color calibration founc:')
        print('../data/' + task + '/color/' + ID + '_col_cal*.txt')
        return(colors)

    # find the largest color calibration file index:
    idx = np.argmax([int(os.path.splitext(os.path.basename(x))[0].split('_')[3]) for x in all_files])
    
    col_file = open(all_files[idx],'r')
    col_param = col_file.read().replace('\t','\n').split('\n')
    col_file.close()
    # print(col_param)
    # let's flip this depending on the task run, in each of the experiments?
    # col_ipsi = eval(col_param[3]) if hemifield == 'left' else eval(col_param[5]) # left or right
    # col_cont = eval(col_param[5]) if hemifield == 'left' else eval(col_param[3]) # right or left
    
    # so use the left / right things for now
    colors['left']  = eval(col_param[3])
    colors['right'] = eval(col_param[5])

    # 'both' should be defined in 1 way... up for grabs how, afaic
    # colors['both']  = [-0.7, -0.7, -0.7] # from 2nd FBE version of the distance task

    # this comes down to black in ALL cases:
    colors['both']  = [eval(col_param[3])[1], eval(col_param[5])[0], -1]
    # print(colors)
    return(colors)

    

def makeBlindSpotMarkers(task, ID, colors): # used to have 'win' argument

    if task == None:
        return({})

    if ID == None:
        return({})

    main_path = '../data/' + task + '/'
    
    hemifields = []

    ## read blindspot parameters... if any...
    left_files = glob(os.path.join('..', 'data', task, 'mapping', ID + '_LH_blindspot*.txt' ) )
    if len(left_files):
        idx = np.argmax([int(os.path.splitext(os.path.basename(x))[0].split('_')[3]) for x in left_files])
        bs_file = open(left_files[idx], 'r')
        bs_param = bs_file.read().replace('\t','\n').split('\n')
        bs_file.close()
        spot_left_cart = eval(bs_param[1])
        spot_left = cart2pol(spot_left_cart[0], spot_left_cart[1])
        spot_left_size = eval(bs_param[3])
        hemifields.append('left')

    right_files = glob(os.path.join('..', 'data', task, 'mapping', ID + '_RH_blindspot*.txt' ) )
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

        # not creating the actual psychopy stimuli:
        # blindspotmarkers[hemifield] = visual.Circle(win, radius = .5, pos = [7,0], units = 'deg', fillColor=colors[hemifield], lineColor = None, interpolate = True)
        blindspotmarkers[hemifield] = myCircle(win=False, radius = .5, pos = [7,0], units = 'deg', fillColor=colors[hemifield], lineColor = None, interpolate = True)
        blindspotmarkers[hemifield].pos = spot_cart
        blindspotmarkers[hemifield].size = spot_size

    # print(len(blindspotmarkers))

    return(blindspotmarkers)



class fusionStim:

    def __init__(self, 
                #  win, # there can NOT be a psychopy Window
                 pos     = [0,0],
                 colors  = [[-1,-1,-1],[1,1,1]],
                 rows    = 7,
                 columns = 3,
                 square  = 0.5,
                 units   = 'deg'):

        # self.win     = win
        self.pos     = pos
        self.colors  = colors
        self.rows    = rows
        self.columns = columns
        self.square  = square
        self.units   = units

        self.resetProperties()

    def resetProperties(self):
        self.nElements = (self.columns*2 + 1) * (self.rows*2 + 1)

        self.setColorArray()
        # self.setPositions()
        # self.createElementArray()

    def setColorArray(self):
        self.colorArray = (self.colors * int(np.ceil(((self.columns*2 + 1) * (self.rows*2 + 1))/len(self.colors))))
        random.shuffle(self.colorArray) # this is the only line that counts...
        # self.colorArray = self.colorArray[:self.nElements]

    def setPositions(self):
        return
        # self.xys = [[(i*self.square)+self.pos[0], (j*self.square)+self.pos[1]] for i in range(-self.columns, self.columns+1) for j in range(-self.rows, self.rows+1)]

    def createElementArray(self):
        return
        # self.elementArray = visual.ElementArrayStim( win         = self.win, 
        #                                              nElements   = self.nElements,
        #                                              sizes       = self.square, 
        #                                              xys         = self.xys, 
        #                                              colors      = self.colorArray, 
        #                                              units       = self.units, 
        #                                              elementMask = 'none', 
        #                                              sfs         = 0)

    def draw(self):
        return
        # self.elementArray.draw()
