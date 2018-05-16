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
        boxL = self.gScreen.rect(pos=[-0.85,0], width=0.05, height=0.8, lineWidth = 5, lineColor = 'white', fillColor = 'white')
        boxR = self.gScreen.rect(pos=[0.85,0], width=0.05, height=0.8, lineWidth = 5, lineColor = 'white', fillColor = 'white')
        fixation = self.gScreen.text(text='+', pos=(0,0.02), color='white', height=0.3)
        rmsbarL = self.gScreen.rect(pos=[-0.85,0], width=0.05, height=0.0, lineWidth = 1, lineColor = 'black', fillColor = 'red')
        rmsbarR = self.gScreen.rect(pos=[0.85,0], width=0.05, height=0.0, lineWidth = 1, lineColor = 'black', fillColor = 'red')
        target = self.gScreen.circle(pos=[0,0], radius = 0.05, lineWidth=4.0, lineColor='green', fillColor='lightgreen')
        finger = self.gScreen.circle(pos=[0,0],radius = 0.01, lineWidth = 3.0, lineColor = 'white', fillColor = 'grey')
        #limit1 = self.gScreen.rect(pos=[-0.8,0], width=0.1, height=0.6, lineWidth = 5, lineColor = 'white', fillColor = 'grey')
        #limit2 = self.gScreen.rect(pos=[0.8,0], width=0.1, height=0.6, lineWidth = 5, lineColor = 'white', fillColor = 'grey')
<<<<<<< HEAD
       
=======
        boxL = self.gScreen.rect(pos=[-0.85,0], width=0.05, height=0.8, lineWidth = 5, lineColor = 'white', fillColor = 'black')
        boxR = self.gScreen.rect(pos=[0.85,0], width=0.05, height=0.8, lineWidth = 5, lineColor = 'white', fillColor = 'black')
        #lowerlimit = self.gScreen.rect(pos=[-0.8,-0.5], width=5, height=0.0, lineWidth = 3.0, lineColor = 'white', fillColor = 'black')
        img = self.gScreen.image(win = self.handle, image = "hand.png", units = "pix")
        
        size_x = img.size[0]
        size_y = img.size[1]
        img.size = [size_x * 1.5, size_y * 1.5]
        
        img.draw()
        
        self.flip()
        
        psychopy.event.waitKeys()
        
        win.close()
>>>>>>> 59757662aa8db8826d46c8b2b78f978adea03b2d
        




        target.opacity = 0.0
        rmsbarL.opacity = 0.5
        rmsbarR.opacity = 0.5
        finger.opacity = 0.7
        boxL.opacity = 0.4
        boxR.opacity = 0.4
        #limit1.opacity = 0.3
        #limit2.opacity = 0.3

        


        #   - save objects to dictionary for easy access
        #self.gScreen['finger1']          = finger1
        self.gScreen['finger']          = finger
        self.gScreen['rmsbarL']         = rmsbarL
        self.gScreen['rmsbarR']         = rmsbarR
        self.gScreen['boxL']            = boxL
        self.gScreen['boxR']            = boxR
        self.gScreen['target']          = target
        self.gScreen['text']            = text
        self.gScreen['fixation']        = fixation        
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
        gRMSbarL    = self.gScreen['rmsbarL']
        gRMSbarR    =self.gScreen['rmsbarR']
        gTarget     = self.gScreen['target']
        #gLimit  = self.gScreen['limit']       

        # update finger notification
        gText.text = self.gScreen['fingerLabels'][self.gTrial.Digit - 1]
        
        # update finger pos and raidus based on hardware readings
        pos             = self.gHardware['gHand'].getXYZ(self.gTrial.Digit - 1)
        gFinger.pos     = [(pos[0]), (pos[1])]
        gFinger.radius  = 0.05 + pos[2]/1.5
      
        #update ens bars based on hardware reading
        rms         = self.gHardware['gHand'].getXY_RMSForces(self.gTrial.Digit - 1) 
        fingxy      = (np.square(self.gTrial.TargetX/10)) + (np.square(self.gTrial.TargetY/10))
        rms_perc    = self.gTrial.EnsPercent
        rms_fing    = np.sqrt(fingxy)

        rms_lim         = rms_fing*rms_perc
        rms_visual       = 50*(rms/rms_lim)

        gRMSbarL.height = rms_visual
        gRMSbarR.height = rms_visual

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
        gRMSbarL     = self.gScreen['rmsbarL']
        gRMSbarR     = self.gScreen['rmsbarR']
        gTarget     = self.gScreen['target']
        #gLimit      = self.gScreen['limit']

        # START_TRIAL
        if self.state == self.gStates.START_TRIAL:
            gTarget.opacity     = 1.0
            gTarget.fillColor   = 'black'
            gTarget.lineColor   = 'black'

            gFinger.opacity     = 0.7
            gFixation.color     = 'white'
            gFinger.fillColor   = 'blue'

            gRMSbarR.fillColor  = 'LightPink'
            gRMSbarL.fillColor  = 'LightPink'


            if self.gTimer[0] > self.gTrial.StartTime:
                # log trial start time
                self.gVariables['measStartTime']    = self.gTimer[0]
                gTarget.opacity                     = 1.0
                gTarget.fillColor                   = 'green'
                gTarget.lineColor                   = 'green'
                gFixation.color                     = 'black'
                self.state                          = self.gStates.WAIT_RESPONSE                

        # WAIT_RESPONSE
        elif self.state == self.gStates.WAIT_RESPONSE:
            # ****** somewhere here, look to add while loop to end trial early if ens radius > finger radius
            # calculate distance from target
            euc_dist    = np.linalg.norm(np.subtract(gFinger.pos,gTarget.pos))
            bar_height  = gRMSbarL.height
            box_height  = 0.8 # ** change later
            if bar_height > box_height:
                gTarget.lineColor   = 'black'
                gTarget.fillColor   = 'black'
                gFixation.color     = 'white'                
                gFinger.fillColor   = 'red'
                gRMSbarL.fillColor  = 'red'
                gRMSbarR.fillColor  = 'red'
                
                self.state = self.gStates.TRIAL_COMPLETE

            if euc_dist <= gTarget.radius:
                gFixation.color     = 'white'
                gFinger.opacity     = 0.95
                gFinger.fillColor   = 'green'
                gTarget.lineColor   = 'black'
                gTarget.fillColor   = 'black'
                self.state          = self.gStates.WAIT_RELEASE

            if self.gTimer[0] > self.gTrial.EndTime:
                # log trial end time
                gTarget.opacity     = 0.95
                gFixation.color     = 'white'                
                gFinger.fillColor   = 'red'
                gTarget.lineColor   = 'black'
                gTarget.fillColor   = 'black'
                self.state          = self.gStates.TRIAL_COMPLETE

        # WAIT_RELEASE
        elif self.state == self.gStates.WAIT_RELEASE:
            euc_dist = np.linalg.norm(np.subtract(gFinger.pos,gFixation.pos))
            # *** seems to be issue with endtime being the same time as end of trial and end of time to get backk?
            if (euc_dist <= 0.05) or (self.gTimer[0] > self.gTrial.EndTime):
                gFixation.color                     = 'white'                
                gFinger.fillColor                   = 'lightblue'
                self.state                          = self.gStates.TRIAL_COMPLETE

        # TRIAL_COMPLETE
        elif self.state == self.gStates.TRIAL_COMPLETE:
            self.gVariables['measEndTime']      = self.gTimer[0]
            self.state                          = self.gStates.END_TRIAL
            

    # adding trial data on trial end
    def onTrialEnd(self):
        gTrial = self.gTrial
        gVar = self.gVariables
        self.gData.add_data_record([gTrial.TN, gTrial.StartTime, gTrial.EndTime, gTrial.Hand, gTrial.Digit, gVar['measStartTime'], gVar['measEndTime']])


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
    gExp.set_trial_states('START_TRIAL','WAIT_RESPONSE','WAIT_RELEASE','TRIAL_COMPLETE','END_TRIAL')

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