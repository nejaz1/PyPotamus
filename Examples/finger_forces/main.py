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
from sys import platform

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
        ens  = self.gScreen.circle(pos=[0,0], radius=0.01, lineColor='black', fillColor='gray')
        # e  = self.gScreen.circle(pos=[0,0], radius=1, lineColor='black', fillColor='gray')
        fixation = self.gScreen.text(text='+', pos=(0,0.02), color='white', height=0.3)
        target = self.gScreen.circle(pos=[0,0], radius=0.1, lineWidth=4.0, lineColor='green', fillColor='lightgreen')
        finger = self.gScreen.circle(pos=[0,0], radius=0.05, lineWidth=3.0, lineColor='white', fillColor='lightblue')

        target.opacity = 0.0
        ens.opacity    = 0.4


        #   - save objects to dictionary for easy access
        self.gScreen['finger']          = finger
        self.gScreen['target']          = target
        self.gScreen['text']            = text
        self.gScreen['fixation']        = fixation        
        self.gScreen['enslaving']       = ens
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
        gText   = self.gScreen['text']
        gFinger = self.gScreen['finger']
        gTarget = self.gScreen['target']
        gEns    = self.gScreen['enslaving']        

        # update finger notification
        gText.text = self.gScreen['fingerLabels'][self.gTrial.Digit - 1]
        
        # update finger pos based on hardware readings
        gFinger.pos = self.gHardware['gHand'].getXY(self.gTrial.Digit - 1)
        
        # update target pos based on hardware readings
        x = self.gTrial.TargetX/10
        y = self.gTrial.TargetY/10
        gTarget.pos = (x,y)

        # update enslaving strength indicator
        rms         = self.gHardware['gHand'].getXY_RMSForces(self.gTrial.Digit - 1)
        gEns.radius = rms / 1.4

    # over-load experimental trial loop function
    def trial(self):
        # get handles for fast access
        gFixation   = self.gScreen['fixation']
        gFinger = self.gScreen['finger']
        gTarget = self.gScreen['target']
        
        # START_TRIAL
        if self.state == self.gStates.START_TRIAL:
            gTarget.opacity     = 0.0
            gFixation.color     = 'white'
            gFinger.fillColor   = 'lightblue'

            if self.gTimer[0] > self.gTrial.StartTime:
                # log trial start time
                self.gVariables['measStartTime']    = self.gTimer[0]
                gTarget.opacity                     = 1.0
                gFixation.color                     = 'black'
                self.state                          = self.gStates.WAIT_RESPONSE                

        # WAIT_RESPONSE
        elif self.state == self.gStates.WAIT_RESPONSE:
            # calculate distance from target
            euc_dist = np.linalg.norm(np.subtract(gFinger.pos,gTarget.pos))
            if euc_dist <= gTarget.radius:
                gTarget.opacity     = 0.3
                gFixation.color     = 'white'
                gFinger.fillColor   = 'green'
                self.state          = self.gStates.WAIT_RELEASE

            if self.gTimer[0] > self.gTrial.EndTime:
                # log trial end time
                gTarget.opacity     = 0.0
                gFixation.color     = 'white'                
                gFinger.fillColor   = 'red'
                self.state          = self.gStates.TRIAL_COMPLETE

        # WAIT_RELEASE
        elif self.state == self.gStates.WAIT_RELEASE:
            euc_dist = np.linalg.norm(np.subtract(gFinger.pos,gFixation.pos))

            if (euc_dist <= 0.05) or (self.gTimer[0] > self.gTrial.EndTime):
                gFixation.color                     = 'white'                
                gFinger.fillColor                   = 'lightblue'
                self.state          = self.gStates.TRIAL_COMPLETE

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
    gExp.diagnostic('on')

    # initialize data directory and format to save during experiment
    if platform == "darwin":
       gExp.set_data_directory('/Users/naveed/Dropbox/Code/toolboxes/PyPotamus/Examples/finger_forces/data/')
    elif platform == "win32":    
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
