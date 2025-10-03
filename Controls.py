#!/usr/bin/env python3

# GUI elements, and interaction with OS
import wx, wx.adv, os

# we need to open webbrowsers to fill in the consent form:
import webbrowser as wb

# functions for Runner
from utilities import *

# psychophysics:
from calibration import *
from distHorizontal import *
# from distBinocular import *
# from distUpturned import *
from distAsynchronous import *
from distScaledAsynchronous import *
from distScaledAsynchronousOFS import *

# is this still used?
from distScaled import *



class MyFrame(wx.Frame):

    def __init__(self, *args, **kwds):

        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)

        self.SetSize(600, 480) ## too big?

        ### --- MAKE GUI ELEMENTS --- ###
        self.existingParticipants = findParticipantIDs()


        if os.sys.platform == 'linux':
            temp_location = 'Toronto'
        else:
            temp_location = 'Glasgow'
		  
        self.location_radiobox = wx.RadioBox(self, label = 'location:', pos = (80,10), choices = ['Glasgow', 'Toronto'], majorDimension = 1, style = wx.RA_SPECIFY_ROWS) 
        self.location_radiobox.SetStringSelection(temp_location)

        # participant elements:
        self.text_participant = wx.StaticText(self, -1, "Participant ID:")
        self.refresh_icon = wx.Bitmap('rotate.png') 
        self.refresh_button = wx.Button(self, wx.ID_ANY, "refresh")
        self.refresh_button.SetBitmap(self.refresh_icon) 
        self.text_existing = wx.StaticText(self, -1, "Existing:")
        self.pick_existing = wx.ComboBox(self, id=wx.ID_ANY, choices=self.existingParticipants, style=wx.CB_READONLY)
        self.random_generate = wx.Button(self, wx.ID_ANY, "generate random")
        self.participantID = wx.TextCtrl(self, wx.ID_ANY, "")

        self.hyperlink_demographics = wx.adv.HyperlinkCtrl(self, wx.ID_ANY, label="demographics", url="")


        # task elements:
        self.horizontal_count = wx.StaticText(self, -1, "#")
        self.horizontal_text = wx.StaticText(self, -1, "Horizontal:")
        self.horizontal_color = wx.Button(self, -1, "color")
        self.horizontal_mapping = wx.Button(self, -1, "mapping")
        self.horizontal_left = wx.Button(self, -1, "left")
        self.horizontal_right = wx.Button(self, -1, "right")

        self.scaled_count = wx.StaticText(self, -1, "#")
        self.scaled_text = wx.StaticText(self, -1, "Scaled:")
        self.scaled_color = wx.Button(self, -1, "color")
        self.scaled_mapping = wx.Button(self, -1, "mapping")
        self.scaled_left = wx.Button(self, -1, "left")
        self.scaled_right = wx.Button(self, -1, "right")

        # self.upturned_count = wx.StaticText(self, -1, "#")
        # self.upturned_text = wx.StaticText(self, -1, "Upturned:")
        # self.upturned_color = wx.Button(self, -1, "color")
        # self.upturned_mapping = wx.Button(self, -1, "mapping")
        # self.upturned_left = wx.Button(self, -1, "left")
        # self.upturned_right = wx.Button(self, -1, "right")

        self.asynchronous_count = wx.StaticText(self, -1, "#")
        self.asynchronous_text = wx.StaticText(self, -1, "Asynchronous:")
        self.asynchronous_color = wx.Button(self, -1, "color")
        self.asynchronous_mapping = wx.Button(self, -1, "mapping")
        self.asynchronous_left = wx.Button(self, -1, "left")
        self.asynchronous_right = wx.Button(self, -1, "right")

        self.scaledasynch_count = wx.StaticText(self, -1, "#")
        self.scaledasynch_text = wx.StaticText(self, -1, "Scal. Asynch:")
        self.scaledasynch_color = wx.Button(self, -1, "color")
        self.scaledasynch_mapping = wx.Button(self, -1, "mapping")
        self.scaledasynch_left = wx.Button(self, -1, "left")
        self.scaledasynch_right = wx.Button(self, -1, "right")

        self.scasynchofs_count = wx.StaticText(self, -1, "#")
        self.scasynchofs_text = wx.StaticText(self, -1, "Sc. Async. OFS:")
        self.scasynchofs_color = wx.Button(self, -1, "color")
        self.scasynchofs_mapping = wx.Button(self, -1, "mapping")
        self.scasynchofs_left = wx.Button(self, -1, "left")
        self.scasynchofs_right = wx.Button(self, -1, "right")

        # self.binocular_count = wx.StaticText(self, -1, "#")
        # self.binocular_text = wx.StaticText(self, -1, "Binocular:")
        # self.binocular_color = wx.Button(self, -1, "color")
        # self.binocular_mapping = wx.Button(self, -1, "mapping")
        # self.binocular_task = wx.Button(self, -1, "run")



        self.__set_properties()
        self.__do_layout()

        ### --- BIND BUTTONS TO FUNCTIONS --- ###
        
        # location functionality:
        self.location_radiobox.Bind(wx.EVT_RADIOBOX,self.selectLocation)

        # participant ID functionality:
        self.Bind(wx.EVT_BUTTON, self.refresh, self.refresh_button)
        self.Bind(wx.EVT_COMBOBOX, self.pickExisting, self.pick_existing)
        self.Bind(wx.EVT_BUTTON, self.generateRandomID, self.random_generate)

        self.Bind(wx.adv.EVT_HYPERLINK, self.onClickDemographics, self.hyperlink_demographics)

        # task button functionality:
        self.Bind(wx.EVT_BUTTON, self.runTask, self.horizontal_color)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.horizontal_mapping)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.horizontal_left)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.horizontal_right)
        
        # self.Bind(wx.EVT_BUTTON, self.runTask, self.binocular_color)
        # self.Bind(wx.EVT_BUTTON, self.runTask, self.binocular_mapping)
        # self.Bind(wx.EVT_BUTTON, self.runTask, self.binocular_task)
        # 

        self.Bind(wx.EVT_BUTTON, self.runTask, self.scaled_color)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.scaled_mapping)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.scaled_left)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.scaled_right)

        # self.Bind(wx.EVT_BUTTON, self.runTask, self.upturned_color)
        # self.Bind(wx.EVT_BUTTON, self.runTask, self.upturned_mapping)
        # self.Bind(wx.EVT_BUTTON, self.runTask, self.upturned_left)
        # self.Bind(wx.EVT_BUTTON, self.runTask, self.upturned_right)

        self.Bind(wx.EVT_BUTTON, self.runTask, self.asynchronous_color)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.asynchronous_mapping)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.asynchronous_left)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.asynchronous_right)

        self.Bind(wx.EVT_BUTTON, self.runTask, self.scaledasynch_color)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.scaledasynch_mapping)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.scaledasynch_left)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.scaledasynch_right)

        self.Bind(wx.EVT_BUTTON, self.runTask, self.scasynchofs_color)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.scasynchofs_mapping)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.scasynchofs_left)
        self.Bind(wx.EVT_BUTTON, self.runTask, self.scasynchofs_right)

        # self.Bind(wx.EVT_BUTTON, self.runTask, self.curve_color)
        # self.Bind(wx.EVT_BUTTON, self.runTask, self.curve_mapping)
        # self.Bind(wx.EVT_BUTTON, self.runTask, self.curve_left)
        # self.Bind(wx.EVT_BUTTON, self.runTask, self.curve_right)


        # control button functionality:        
        # self.Bind(wx.EVT_BUTTON, self.runTask, self.ori_color)
        # self.Bind(wx.EVT_BUTTON, self.runTask, self.ori_mapping)
        # self.Bind(wx.EVT_BUTTON, self.runTask, self.ori_task)
        # self.Bind(wx.EVT_BUTTON, self.runTask, self.hor_task)


        # # more advanced stuff ?
        # self.Bind(wx.EVT_BUTTON, self.makeDataFolders, self.folder_button)
        # self.Bind(wx.EVT_BUTTON, self.cloneGitHub, self.clone_button)
        # self.Bind(wx.EVT_BUTTON, self.pullGitHub, self.pull_button)

        # # UPLOAD functionality needs to be figured out still...




    def __set_properties(self):
        self.SetTitle("Intrepid-2a Experiment Controls")
        # self.disableChecks()
        self.selectLocation()
        # update list of choices for existing participants
        self.refresh()

        # count participants who already did the experiment?

    def __do_layout(self):

        # there will be 3 main sections, that each get a grid sizer:
        # - participant ID section
        # - task run setcion (with N counters)
        # - GitHub & OSF synchronization sections
        # these will be placed into the main grid afterwards

        main_grid        = wx.GridSizer(4, 1, 0, 0)
        
        # other grids, to put in main grid:
        # location thing is 1 item, no grid needed...
        participant_grid = wx.GridSizer(2, 4, 0, 0)

        taskrun_grid     = wx.GridSizer(6, 6, 0, 0) # 6 tasks, 6 elements per task

        # control_grid     = wx.GridSizer(1, 6, 0, 0)

        synch_grid       = wx.GridSizer(2, 4, 0, 0)  # too much?


        # fill main gird:
        main_grid.Add(self.location_radiobox, 0, wx.ALIGN_LEFT, 0)

        # add elements to participant grid:
        participant_grid.Add(self.text_participant, 0, wx.ALIGN_LEFT, 0)
        participant_grid.Add(self.text_existing, 0, wx.ALIGN_LEFT, 0)
        participant_grid.Add(self.random_generate, 0, wx.ALIGN_LEFT, 0)

        participant_grid.Add(self.hyperlink_demographics, 1, wx.ALIGN_RIGHT, 0)

        participant_grid.Add(self.refresh_button, 0, wx.ALIGN_LEFT, 0)
        participant_grid.Add(self.pick_existing, 0, wx.ALIGN_LEFT, 0)
        participant_grid.Add(self.participantID, 0, wx.ALIGN_LEFT, 0)
        # add participant grid to main grid:
        main_grid.Add(participant_grid)

        # add elements to task-run grid:
        taskrun_grid.Add(self.horizontal_count, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.horizontal_text, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.horizontal_color, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.horizontal_mapping, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.horizontal_left, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.horizontal_right, -1, wx.ALIGN_LEFT, 0)

        taskrun_grid.Add(self.scaled_count, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scaled_text, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scaled_color, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scaled_mapping, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scaled_left, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scaled_right, -1, wx.ALIGN_LEFT, 0)

        # taskrun_grid.Add(self.upturned_count, -1, wx.ALIGN_LEFT, 0)
        # taskrun_grid.Add(self.upturned_text, -1, wx.ALIGN_LEFT, 0)
        # taskrun_grid.Add(self.upturned_color, -1, wx.ALIGN_LEFT, 0)
        # taskrun_grid.Add(self.upturned_mapping, -1, wx.ALIGN_LEFT, 0)
        # taskrun_grid.Add(self.upturned_left, -1, wx.ALIGN_LEFT, 0)
        # taskrun_grid.Add(self.upturned_right, -1, wx.ALIGN_LEFT, 0)        

        taskrun_grid.Add(self.asynchronous_count, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.asynchronous_text, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.asynchronous_color, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.asynchronous_mapping, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.asynchronous_left, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.asynchronous_right, -1, wx.ALIGN_LEFT, 0)        

        taskrun_grid.Add(self.scaledasynch_count, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scaledasynch_text, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scaledasynch_color, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scaledasynch_mapping, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scaledasynch_left, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scaledasynch_right, -1, wx.ALIGN_LEFT, 0)

        taskrun_grid.Add(self.scasynchofs_count, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scasynchofs_text, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scasynchofs_color, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scasynchofs_mapping, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scasynchofs_left, -1, wx.ALIGN_LEFT, 0)
        taskrun_grid.Add(self.scasynchofs_right, -1, wx.ALIGN_LEFT, 0)          

        # taskrun_grid.Add(self.binocular_count, -1, wx.ALIGN_LEFT, 0)
        # taskrun_grid.Add(self.binocular_text, -1, wx.ALIGN_LEFT, 0)
        # taskrun_grid.Add(self.binocular_color, -1, wx.ALIGN_LEFT, 0)
        # taskrun_grid.Add(self.binocular_mapping, -1, wx.ALIGN_LEFT, 0)
        # taskrun_grid.Add(self.binocular_task, -1, wx.ALIGN_LEFT, 0)
        # #

        # add task-run grid to main grid:
        main_grid.Add(taskrun_grid)


        self.SetSizer(main_grid)
        self.Layout() # frame method from wx


    def selectLocation(self, event=0):
        self.location = self.location_radiobox.GetStringSelection().lower()

    def refresh(self, event=0):
        dataInfo = getGeneralDataInfo()
        self.existingParticipants = dataInfo['IDs']
        
        self.pick_existing.Clear()
        self.pick_existing.AppendItems(self.existingParticipants)
        self.toggleParticipantTaskButtons(event)

        counts = dataInfo['counts']
        self.horizontal_count.SetLabel( '%d (%d)'%(counts['distHorizontal'], counts['all']) )
        self.scaled_count.SetLabel( '%d (%d)'%(counts['distScaled'], counts['all']) )
        # self.upturned_count.SetLabel( '%d (%d)'%(counts['distUpturned'], counts['all']) )
        # self.binocular_count.SetLabel( '%d (%d)'%(counts['distBinocular'], counts['all']) )
        self.asynchronous_count.SetLabel( '%d (%d)'%(counts['distAsynchronous'], counts['all']) )
        self.scaledasynch_count.SetLabel( '%d (%d)'%(counts['distScaledAsynchronous'], counts['all']) )
        self.scasynchofs_count.SetLabel( '%d (%d)'%(counts['distScaledAsynchronousOFS'], counts['all']) )
        # self.dist_count.SetLabel( '%d (%d)'%(counts['distance'], counts['all']) )

    def pickExisting(self, event):
        self.participantID.SetValue(self.pick_existing.GetValue())
        self.toggleParticipantTaskButtons(event)


    def generateRandomID(self, event):
        newID = generateRandomParticipantID(prepend=self.location.lower()[:3]+'', nbytes=3)
        self.participantID.SetValue(newID)
        self.toggleParticipantTaskButtons(event)

    def onClickDemographics(self, e):
        wb.open( url = self.hyperlink_demographics.GetURL(),
                 new = 1,
                 autoraise = True )
        

    def toggleParticipantTaskButtons(self, event):

        newURL = 'https://docs.google.com/forms/d/e/1FAIpQLScwyXoXaymXpXOO7ZToVsHFpb8hwis1eMvQE5NNGt55ij9HGw/viewform?usp=pp_url&entry.1851916630=%s'%(self.participantID.GetValue())
        self.hyperlink_demographics.SetURL(newURL)


        info = getParticipantTaskInfo(self.participantID.GetValue())

        # new check 8 things, and toggle the 16 buttons:
        self.horizontal_color.Enable()
        self.horizontal_mapping.Disable()
        if info['distHorizontal']['color']:
            self.horizontal_mapping.Enable()
        self.horizontal_left.Disable()
        self.horizontal_right.Disable()
        if info['distHorizontal']['mapping']:
            self.horizontal_left.Enable()
            self.horizontal_right.Enable()
        
        self.scaled_color.Enable()
        self.scaled_mapping.Disable()
        if info['distScaled']['color']:
            self.scaled_mapping.Enable()
        self.scaled_left.Disable()
        self.scaled_right.Disable()
        if info['distScaled']['mapping']:
            self.scaled_left.Enable()
            self.scaled_right.Enable()

        # self.upturned_color.Enable()
        # self.upturned_mapping.Disable()
        # if info['distUpturned']['color']:
        #     self.upturned_mapping.Enable()
        # self.upturned_left.Disable()
        # self.upturned_right.Disable()
        # if info['distUpturned']['mapping']:
        #     self.upturned_left.Enable()
        #     self.upturned_right.Enable()

        self.asynchronous_color.Enable()
        self.asynchronous_mapping.Disable()
        if info['distAsynchronous']['color']:
            self.asynchronous_mapping.Enable()
        self.asynchronous_left.Disable()
        self.asynchronous_right.Disable()
        if info['distAsynchronous']['mapping']:
            self.asynchronous_left.Enable()
            self.asynchronous_right.Enable()

        self.scaledasynch_color.Enable()
        self.scaledasynch_mapping.Disable()
        if info['distScaledAsynchronous']['color']:
            self.scaledasynch_mapping.Enable()
        self.scaledasynch_left.Disable()
        self.scaledasynch_right.Disable()
        if info['distScaledAsynchronous']['mapping']:
            self.scaledasynch_left.Enable()
            self.scaledasynch_right.Enable()

        self.scasynchofs_color.Enable()
        self.scasynchofs_mapping.Disable()
        if info['distScaledAsynchronousOFS']['color']:
            self.scasynchofs_mapping.Enable()
        self.scasynchofs_left.Disable()
        self.scasynchofs_right.Disable()
        if info['distScaledAsynchronousOFS']['mapping']:
            self.scasynchofs_left.Enable()
            self.scasynchofs_right.Enable()

        # self.binocular_color.Enable()
        # self.binocular_mapping.Disable()
        # if info['distBinocular']['color']:
        #     self.binocular_mapping.Enable()
        # self.binocular_task.Disable()
        # if info['distBinocular']['mapping']:
        #     self.binocular_task.Enable()
        



    def runTask(self, event):

        if self.participantID.GetValue() == '':
            # no participant ID!
            return

        task = None
        subtask = None

        buttonId = event.Id
        offset = [0,0]
        if buttonId in [self.horizontal_color.Id, self.horizontal_mapping.Id, self.horizontal_left.Id, self.horizontal_right.Id]:
            task = 'distHorizontal'
        if buttonId in [self.scaled_color.Id, self.scaled_mapping.Id, self.scaled_left.Id, self.scaled_right.Id]:
            task = 'distScaled'
        # if buttonId in [self.binocular_color.Id, self.binocular_mapping.Id, self.binocular_task.Id]:
        #     task = 'distBinocular'
        # if buttonId in [self.upturned_color.Id, self.upturned_mapping.Id, self.upturned_left.Id, self.upturned_right.Id]:
        #     task = 'distUpturned'
        #     offset = [0,-10]
        if buttonId in [self.asynchronous_color.Id, self.asynchronous_mapping.Id, self.asynchronous_left.Id, self.asynchronous_right.Id]:
            task = 'distAsynchronous'
        if buttonId in [self.scaledasynch_color.Id, self.scaledasynch_mapping.Id, self.scaledasynch_left.Id, self.scaledasynch_right.Id]:
            task = 'distScaledAsynchronous'
         if buttonId in [self.scasynchofs_color.Id, self.scasynchofs_mapping.Id, self.scasynchofs_left.Id, self.scasynchofs_right.Id]:
            task = 'distScaledAsynchronousOFS'


        # if buttonId in [self.horizontal_color.Id, self.scaled_color.Id, self.upturned_color.Id, self.asynchronous_color.Id, self.scaledasynch_color.Id, self.binocular_color.Id]:
        if buttonId in [self.horizontal_color.Id, self.scaled_color.Id, self.asynchronous_color.Id, self.scaledasynch_color.Id, self.scasynchofs_color.Id]:
            subtask = 'color'
        # if buttonId in [self.horizontal_mapping.Id, self.scaled_mapping.Id, self.upturned_mapping.Id, self.asynchronous_mapping.Id, self.scaledasynch_mapping.Id, self.binocular_mapping.Id]:
        if buttonId in [self.horizontal_mapping.Id, self.scaled_mapping.Id, self.asynchronous_mapping.Id, self.scaledasynch_mapping.Id, self.scasynchofs_mapping.Id]:
            subtask = 'mapping'
        # if buttonId in [self.horizontal_left.Id, self.scaled_left.Id, self.upturned_left.Id, self.asynchronous_left.Id, self.scaledasynch_left.Id]:
        if buttonId in [self.horizontal_left.Id, self.scaled_left.Id, self.asynchronous_left.Id, self.scaledasynch_left.Id, self.scasynchofs_left.Id]:
            subtask = 'left'
        # if buttonId in [self.horizontal_right.Id, self.scaled_right.Id, self.upturned_right.Id, self.asynchronous_right.Id, self.scaledasynch_right.Id]:
        if buttonId in [self.horizontal_right.Id, self.scaled_right.Id, self.asynchronous_right.Id, self.scaledasynch_right.Id, self.scasynchofs_right.Id]:
            subtask = 'right'
        # if buttonId in [self.binocular_task.Id]:
        #     subtask = 'run'


        if subtask == None:
            print('no subtask')
            return
        if task == None:
            print('no task')
            return
        
        print([task, subtask])

        if subtask == 'color':
            print('do color calibration')
            doColorCalibration(ID=self.participantID.GetValue(), task=task, location=self.location)
            return

        if subtask == 'mapping':
            # print('do blind spot mpapping')
            doBlindSpotMapping(ID=self.participantID.GetValue(), task=task, location=self.location, offset=offset)
            return

        if task == 'distHorizontal':
            # print('do distance task')
            doDistHorizontalTask(ID=self.participantID.GetValue(), hemifield=subtask, location=self.location)
            return

        if task == 'distScaled':
            # print('do distance task')
            doDistScaledTask(ID=self.participantID.GetValue(), hemifield=subtask, location=self.location)
            return

        # if task == 'distUpturned':
        #     # print('do distance task')
        #     doDistUpturnedTask(ID=self.participantID.GetValue(), hemifield=subtask, location=self.location)
        #     return

        if task == 'distAsynchronous':
            # print('do distance task')
            doDistAsynchronousTask(ID=self.participantID.GetValue(), hemifield=subtask, location=self.location)
            return

        if task == 'distScaledAsynchronous':
            # print('do distance task')
            doDistScaledAsynchronousTask(ID=self.participantID.GetValue(), hemifield=subtask, location=self.location)
            return

        if task == 'distScaledAsynchronousOFS':
            doDistScaledAsynchronousOFSTask(ID=self.participantID.GetValue(), hemifield=subtask, location=self.location)
            return


        # if task == 'distBinocular':
        #     # print('do distance task')
        #     doDistBinocularTask(ID=self.participantID.GetValue(), location=self.location)
        #     return







class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

if __name__ == "__main__":
    app = MyApp(0)
    app.MainLoop()

