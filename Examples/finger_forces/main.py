# Experiment for hand assessment using the hopkins hand device
#
# Created:
# Nov 17: Naveed Ejaz
# 
# IMPORTANT: Path to PyPotamus needs set to be in PYTHONPATH environment variable

from PyPotamus import Experiment
from HopkinsHandDevice import HopkinsHandDevice
import numpy as np
import math
import pdb

# ------------------------------------------------------------------------
# 1. Inherited Experiment class in PyPotamus module
class myExperiment(Experiment):
    # define user commands
    def define_command(self, cmd):
        if cmd == 'zerof':
            self.gHardware['gHand'].zerof(1000)
        else:
            print('unrecognized command')

    # quicker to pre-allocate drawing elements on the screen
    def initialize(self):
        # pre-allocate graphics for
        #   - fixation cross
        #   - text indicator for which finger to press
        #   - draw circles for moving fingers and target stimulus
        #   - draw rectangles for strength of enslaving
        text = self.gScreen.text(text='', pos=(0,0.9), color='white')
        # e  = self.gScreen.circle(pos=[0,0], radius=1, lineColor='black', fillColor='gray')
        img = self.gScreen.image(image = "hand.png", pos=(0,0), units = "pix")
        boxL = self.gScreen.rect(pos=[-0.95,0], width=0.05, height=1, lineWidth = 5, lineColor = 'white', fillColor = 'white')
        boxR = self.gScreen.rect(pos=[0.95,0], width=0.05, height=1, lineWidth = 5, lineColor = 'white', fillColor = 'white')
        fixation = self.gScreen.text(text='+', pos=[0,0.02], color='white', height=0.3)
        ensbarL = self.gScreen.rect(pos=[-0.95,0], width=0.05, height=0.0, lineWidth = 1, lineColor = 'black', fillColor = 'red')
        ensbarR = self.gScreen.rect(pos=[0.95,0], width=0.05, height=0.0, lineWidth = 1, lineColor = 'black', fillColor = 'red')
        target = self.gScreen.circle(pos=[0,0], radius = 0.05, lineWidth=4.0, lineColor='green', fillColor='green')
        finger = self.gScreen.circle(pos=[0,0],radius = 0.01, lineWidth = 3.0, lineColor = 'white', fillColor = 'grey')
        posList = [(-0.1,0),(-0.5, 0.4),(0,0.5),(-0.5,0.4),(-0.1,0.2)]
   
        #limit1 = self.gScreen.rect(pos=[-0.8,0], width=0.1, height=0.6, lineWidth = 5, lineColor = 'white', fillColor = 'grey')
        #limit2 = self.gScreen.rect(pos=[0.8,0], width=0.1, height=0.6, lineWidth = 5, lineColor = 'white', fillColor = 'grey')
        
        img.pos = (0.0, -0.5)
        '''
        size_x = img.size[0]
        size_y = img.size[1]
        img.size = [size_x * 1.5, size_y * 1.5]
        
        
        
        self.flip()
        
        psychopy.event.waitKeys()
        
        win.close()
        '''
        target.opacity = 0.0
        ensbarL.opacity = 0.5
        ensbarR.opacity = 0.5
        finger.opacity = 0.7
        boxL.opacity = 0.4
        boxR.opacity = 0.4
        img.opacity = 0.0
        #limit1.opacity = 0.3
        #limit2.opacity = 0.3

        #   - save objects to dictionary for easy access
        #self.gScreen['finger1']          = finger1
        self.gScreen['finger']          = finger
 
        self.gScreen['ensbarL']         = ensbarL
        self.gScreen['ensbarR']         = ensbarR
        self.gScreen['boxL']            = boxL
        self.gScreen['boxR']            = boxR
        self.gScreen['target']          = target
        self.gScreen['text']            = text
        self.gScreen['fixation']        = fixation 
        self.gScreen['handimage']       = img
        #self.gScreen['limit']           = limit

        self.gScreen['fingerLabels']    = ['THUMB','INDEX','MIDDLE','RING','LITTLE']

    # this function is called when diagnostic info is about to be updated
    def updateDiagnostic(self):        
        self.gDiagnostic[0] = 'Subj:' + self.get_subject_id()
        self.gDiagnostic[1] = 'Timer:' + str(round(self.gTimer[0],1))
        self.gDiagnostic[2] = 'Run:' + str(self.get_runno())
        self.gDiagnostic[3] = 'TN:' + str(self.gTrial.TN)        

    # this function is called when screen is about to be updated
    def updateScreen(self):     
        # get handles for fast access
        gText       = self.gScreen['text']
        gFinger     = self.gScreen['finger']
  
        gEnsbarL    = self.gScreen['ensbarL']
        gEnsbarR    =self.gScreen['ensbarR']
        gTarget     = self.gScreen['target']
        gBoxL       = self.gScreen['boxL']
        gBoxR       = self.gScreen['boxR']
        gHandimage  = self.gScreen['handimage']

        #gLimit  = self.gScreen['limit']       

        # update finger notification
        gText.text = self.gScreen['fingerLabels'][self.gTrial.Digit - 1]
        
        # update finger pos and raidus based on hardware readings
        pos             = self.gHardware['gHand'].getXYZ(self.gTrial.Digit - 1)
        gFinger.pos     = [(pos[0]), (pos[1])]
        gFinger.radius  = 0.05 + pos[2]/1.5
      
        #update ens bars based on hardware reading
        rms         = self.gHardware['gHand'].getXY_RMSForces(self.gTrial.Digit - 1)

        ens_perc    = self.gTrial.EnsPercent/100
        max_rms     = np.sqrt((2 * np.square(0.9)))
        rms_lim     = ens_perc*max_rms
        ens_visual  = ens_perc*(rms/rms_lim)
        
        gEnsbarL.height = min(ens_visual, gBoxL.height)
        gEnsbarR.height = min(ens_visual, gBoxR.height)

        # update target pos based on hardware readings
        x = self.gTrial.TargetX/10
        y = self.gTrial.TargetY/10
        gTarget.pos = (x,y)
        #z= self.gTrial.TargetZ
        #gTarget.radius = z
    
    # over-load experimental trial loop function
    def trial(self):
        # get handles for fast access
        gFixation   = self.gScreen['fixation']
        gFinger     = self.gScreen['finger']
        gEnsbarL     = self.gScreen['ensbarL']
        gEnsbarR     = self.gScreen['ensbarR']
        gTarget     = self.gScreen['target']
        gBoxL       = self.gScreen['boxL']
        gBoxR       = self.gScreen['boxR']
        gHandimage  = self.gScreen['handimage']
        timeMarker = 0
        start_time = 2000
        prep_time = 500
        resp_time  = 1500
        wait_time  = 1000
        dead_time  = 400
        gDigit      = self.gTrial.Digit - 1


        #gLimit      = self.gScreen['limit']

        # QUEUE PHASE
        if self.state == self.gStates.START_TRIAL:
            timeMarker = self.gTrial.StartTime
            gHandimage.opacity  = 1
            gFinger.opacity = 0.7
            if self.gTimer[0] > (timeMarker + start_time):
                timeMarker = self.gTimer[0]
                self.state = self.gStates.WAIT_PREPRATORY  
   

        # START_TRIAL
        elif self.state == self.gStates.WAIT_PREPRATORY:
            ens_perc            = self.gTrial.EnsPercent/100
            gBoxL.height        = ens_perc
            gBoxR.height        = ens_perc

            gTarget.opacity     = 1.0
            gTarget.fillColor   = 'black'
            gTarget.lineColor   = 'black'

            gFinger.opacity     = 0.7
            gFixation.color     = 'white'
            gFinger.fillColor   = 'blue'

            gEnsbarR.fillColor  = 'LightPink'
            gEnsbarL.fillColor  = 'LightPink'


            if self.gTimer[0] > (timeMarker + prep_time):
                # log trial start time
                self.gVariables['measStartTime']    = self.gTimer[0]
                gHandimage.opacity                  = 0.0
                gTarget.opacity                     = 1
                gTarget.fillColor                   = 'Lime'
                gTarget.lineColor                   = 'Lime'
                gFixation.color                     = 'black'
                timeMarker                          = self.gTimer[0]
                self.state                          = self.gStates.WAIT_RESPONSE                
        # WAIT_RESPONSE
        elif self.state == self.gStates.WAIT_RESPONSE:
            # ****** somewhere here, look to add while loop to end trial early if ens radius > finger radius
            # calculate distance from target
            euc_dist    = np.linalg.norm(np.subtract(gFinger.pos,gTarget.pos))
            bar_height  = gEnsbarL.height
            box_height  = gBoxL.height
            if bar_height >= box_height:
                gTarget.lineColor   = 'black'
                gTarget.fillColor   = 'black'
                gFixation.color     = 'white'                
                gFinger.fillColor   = 'red'
                gEnsbarL.fillColor  = 'red'
                gEnsbarR.fillColor  = 'red'
                timeMarker             = self.gTimer[0]
                self.state = self.gStates.WAIT_RELEASE

            if euc_dist <= gTarget.radius:
                gFixation.color     = 'white'
                gFinger.opacity     = 0.95
                gFinger.fillColor   = 'Lime'
                gTarget.lineColor   = 'black'
                gTarget.fillColor   = 'black'
                timeMarker             = self.gTimer[0]
                self.state          = self.gStates.WAIT_RELEASE

            if self.gTimer[0] > (timeMarker + resp_time):
                # log trial end time
                gTarget.opacity     = 0.95
                gFixation.color     = 'white'                
                gFinger.fillColor   = 'red'
                gTarget.lineColor   = 'black'
                gTarget.fillColor   = 'black'
                timeMarker             = self.gTimer[0]
                self.state          = self.gStates.WAIT_RELEASE

        # WAIT_RELEASE
        elif self.state == self.gStates.WAIT_RELEASE:
            euc_dist = np.linalg.norm(np.subtract(gFinger.pos,gFixation.pos))
            # *** seems to be issue with endtime being the same time as end of trial and end of time to get backk?
            if (euc_dist <= 0.05) or (self.gTimer[0] > (timeMarker + wait_time)):
                gFixation.color                     = 'white'                
                gFinger.fillColor                   = 'lightblue'
                timeMarker                          = self.gTimer[0]
                self.state                          = self.gStates.TRIAL_COMPLETE

        # TRIAL_COMPLETE
        elif self.state == self.gStates.TRIAL_COMPLETE:
            self.gVariables['measEndTime']      = self.gTimer[0]
            gFixation.opacity                   = 1

            if self.gTimer[0] > (timeMarker + dead_time):
                self.state                          = self.gStates.END_TRIAL
            

    # adding trial data on trial end
    def onTrialEnd(self):
        gTrial = self.gTrial
        gVar = self.gVariables
        self.gData.add_data_record([gTrial.TN, gTrial.StartTime, gTrial.Hand, gTrial.Digit, gVar['measStartTime'], gVar['measEndTime'], gTrial.EnsPercent])


# ------------------------------------------------------------------------
# 3. Main entry point of program
if __name__ == "__main__":

    # 1. Set up experiment and initalize using default parameters in yaml file
    gExp = myExperiment()
    gExp.load_settings('finger_task.yaml')

    # turn on diagnostic screen for messages/state variables etc
    if gExp.gPlatform.isMac():
        gExp.diagnostic('on')

    # initialize data directory and format to save during experiment
    if gExp.gPlatform.isMac():
        gExp.set_data_directory('/Users/naveed/Dropbox/Code/toolboxes/PyPotamus/Examples/finger_forces/data/')
    else:
        gExp.set_data_directory('C:\\Users\DiedrichsenLab\\PyPotamus\\Examples\\finger_forces\\data')
    gExp.set_data_format(['TN','startTime','endTime','hand','digit','measStartTime','measEndTime'])

    # initialize trial states
    gExp.set_trial_states('START_TRIAL', 'WAIT_PREPRATORY', 'WAIT_RESPONSE','WAIT_RELEASE','TRIAL_COMPLETE','END_TRIAL')

    # initialize drawing elements on screen for speed (also for diagnostic messages)
    gExp.initialize()

    # attached hopkins hand device as part of experiment (call it gHand)
    gExp.add_hardware('gHand',HopkinsHandDevice())
    gExp.gHardware['gHand'].set_force_multiplier((-3,3,3))

    # get user input via console
    # user commands starts/stops experiment
    gExp.control()
    # gHand.terminate()
    # gHand.join()
    # gHand.join()

