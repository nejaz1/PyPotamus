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
        # e  = self.gScreen.circle(pos=[0,0], radius=1, lineColor='black', fillColor='gray')
        img = self.gScreen.image(image = "hand.png", pos=(0,0), units = "pix")
        #boxL = self.gScreen.rect(pos=[-0.95,0], width=0.05, height=1, lineWidth = 5, lineColor = 'white', fillColor = 'white')
        #boxR = self.gScreen.rect(pos=[0.95,0], width=0.05, height=1, lineWidth = 5, lineColor = 'white', fillColor = 'white')
        fixation = self.gScreen.text(text='+', pos=[0,0.02], color='white', height=0.3)
        #ensbarL = self.gScreen.rect(pos=[-0.95,0], width=0.05, height=0.0, lineWidth = 1, lineColor = 'black', fillColor = 'LightPink')
        #ensbarR = self.gScreen.rect(pos=[0.95,0], width=0.05, height=0.0, lineWidth = 1, lineColor = 'black', fillColor = 'LightPink')
        text = self.gScreen.text(text='', pos=(0,0.95), color='black')
        warnings = self.gScreen.text(text='', pos=(0,0), color='black')
        target = self.gScreen.circle(pos=[0,0], radius = 0.1, lineWidth=4.0, lineColor='black', fillColor='black')
        #finger = self.gScreen.circle(pos=[0,0],radius = 0.08, lineWidth = 3.0, lineColor = 'white', fillColor = 'grey')
        finger1 = self.gScreen.circle(pos=[-0.4,0],radius = 0.08, lineWidth = 3.0, lineColor = 'white', fillColor = '#AFADF5')
        finger2 = self.gScreen.circle(pos=[-0.2,0],radius = 0.08, lineWidth = 3.0, lineColor = 'white', fillColor = '#E3CBA0')
        finger3 = self.gScreen.circle(pos=[0,0],radius = 0.08, lineWidth = 3.0, lineColor = 'white', fillColor = '#DE4CBA')
        finger4 = self.gScreen.circle(pos=[0.2,0],radius = 0.08, lineWidth = 3.0, lineColor = 'white', fillColor = 'blue')
        finger5 = self.gScreen.circle(pos=[0.4,0],radius = 0.08, lineWidth = 3.0, lineColor = 'white', fillColor = 'yellow')
        #digit = self.gScreen.circle(pos=[0,0],radius = 0.05, lineWidth = 3.0, lineColor = 'white', fillColor = 'blue')
        #posList = [(-0.45,0.01),(-0.21, 0.42),(0.03,0.5),(0.22,0.48),(0.38,0.28)]
        colorList = ['#AFADF5', '#E3CBA0', '#DE4CBA', 'blue', 'yellow']
    
        target.opacity = 0.0
        img.opacity = 0.0
        finger1.opacity = 0.7
        finger2.opacity = 0.7
        finger3.opacity = 0.7
        finger4.opacity = 0.7
        finger5.opacity = 0.7

        text.color  = 'black'

        #   - save objects to dictionary for easy access
        #self.gScreen['finger1']          = finger1
        #self.gScreen['finger']          = finger
        #self.gScreen['digit']           = digit
        #self.gScreen['ensbarL']         = ensbarL
        #self.gScreen['ensbarR']         = ensbarR
        #self.gScreen['boxL']            = boxL
        #self.gScreen['boxR']            = boxR
        self.gScreen['target']          = target
        self.gScreen['text']            = text
        self.gScreen['warnings']         = warnings
        self.gScreen['finger1']          = finger1
        self.gScreen['finger2']          = finger2
        self.gScreen['finger3']          = finger3
        self.gScreen['finger4']          = finger4
        self.gScreen['finger5']          = finger5
        self.gScreen['fixation']        = fixation 
        self.gScreen['handimage']       = img
        self.gScreen['fingers']         = [finger1, finger2, finger3, finger4, finger5]
        #self.gScreen['posList']         = posList
        self.gScreen['colorList']       = colorList
        self.gScreen['warnList']        = ['Too much movement!', "Time's up!"]
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
        #gFinger     = self.gScreen['finger']
        #gEnsbarL    = self.gScreen['ensbarL']
        #gEnsbarR    = self.gScreen['ensbarR']
        gTarget      = self.gScreen['target']
        #gBoxL       = self.gScreen['boxL']
        #gBoxR       = self.gScreen['boxR']
        gHandimage   = self.gScreen['handimage']
        gText        = self.gScreen['text']
        gFinger1     = self.gScreen['finger1']
        gFinger2     = self.gScreen['finger2']
        gFinger3     = self.gScreen['finger3']
        gFinger4     = self.gScreen['finger4']
        gFinger5     = self.gScreen['finger5']
        #gDigit      = self.gScreen['digit']
        #gPoslist       = self.gScreen['posList']

        gText.text = self.gScreen['fingerLabels'][self.gTrial.Digit - 1]

        # update finger pos and raidus based on hardware readings
        if self.state != self.gStates.TRIAL_COMPLETE or self.gStates.END_TRIAL:
            
            pos1             = self.gHardware['gHand'].getXYZ(0)
            gFinger1.pos     = [(pos1[0] - 0.4), (pos1[1])]
            gFinger1.radius  = 0.07 + pos1[2]/1.5

            pos2             = self.gHardware['gHand'].getXYZ(1)
            gFinger2.pos     = [(pos2[0] - 0.2), (pos2[1])]
            gFinger2.radius  = 0.07 + pos2[2]/1.5

            pos3             = self.gHardware['gHand'].getXYZ(2)
            gFinger3.pos     = [pos3[0], pos3[1]]
            gFinger3.radius  = 0.07 + pos3[2]/1.5

            pos4             = self.gHardware['gHand'].getXYZ(3)
            gFinger4.pos     = [(pos4[0]+0.2), (pos4[1])]
            gFinger4.radius  = 0.07 + pos4[2]/1.5

            pos5             = self.gHardware['gHand'].getXYZ(4)
            gFinger5.pos     = [(pos5[0]+0.4), (pos5[1])]
            gFinger5.radius  = 0.07 + pos5[2]/1.5


      
        #update ens bars based on hardware reading
        #if self.state != self.gStates.TRIAL_COMPLETE or self.gStates.END_TRIAL:
            #rms         = self.gHardware['gHand'].getXY_RMSForces(self.gTrial.Digit - 1)
            #ens_perc    = self.gTrial.EnsPercent/100
            #max_rms     = np.sqrt((2 * np.square(0.9)))
            #rms_lim     = ens_perc*max_rms
            #ens_visual  = ens_perc*(rms/rms_lim)
        
            #gEnsbarL.height = min(ens_visual, gBoxL.height)
            #gEnsbarR.height = min(ens_visual, gBoxR.height)

        #gDigit.pos = gPoslist[(self.gTrial.Digit - 1)]
      

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
        gFinger1     = self.gScreen['finger1']
        gFinger2     = self.gScreen['finger2']
        gFinger3     = self.gScreen['finger3']
        gFinger4     = self.gScreen['finger4']
        gFinger5     = self.gScreen['finger5']
        gFingers     = self.gScreen['fingers']
        gFinger      = gFingers[self.gTrial.Digit - 1]
        #gEnsbarL     = self.gScreen['ensbarL']
        #gEnsbarR     = self.gScreen['ensbarR']
        gTarget     = self.gScreen['target']
        #gBoxL       = self.gScreen['boxL']
        #gBoxR       = self.gScreen['boxR']
        gHandimage  = self.gScreen['handimage']
        gText       = self.gScreen['text']
        #gDigit      = self.gScreen['digit']
        gColorlist  = self.gScreen['colorList']
        #gWarnings   = self.gScreen['warnings']
        #gWarnlist   = self.gScreen['warnList']

        # set time limits for different phases of the trial
        cue_time = 2000
        prep_time = 500
        resp_time  = 1500
        wait_time  = 1000
        target_remain = 200
        dead_time  = 400

        # START TRIAL
        if self.state == self.gStates.START_TRIAL:
            if self.gTimer[0] > self.gTrial.StartTime:
                self.state = self.gStates.CUE_PHASE
                self.gTimer.reset(2)

        if self.state == self.gStates.CUE_PHASE:
           # gEnsbarL.opacity = 0.0
           # gEnsbarR.opacity = 0.0
            for i in range(0,5):
                gFingers[i].opacity = 0
                gFingers[i].fillColor = gColorlist[i] 
            gText.color = 'white'
            gHandimage.opacity  = 0.9
            #gDigit.opacity = 1
            #gDigit.fillColor   = gColorlist[self.gTrial.Digit - 1]
           
            #gBoxR.opacity   = 0.0
            #gBoxL.opacity   = 0.0
            gFixation.color = 'black'
            gTarget.opacity     = 0

            if self.gTimer[2] > cue_time:
                # log trial start time
                self.gVariables['measStartTime']    = self.gTimer[0]
                gHandimage.opacity                  = 0.0

                #gDigit.opacity                      = 0.0
                self.state                          = self.gStates.WAIT_PREPRATORY 
                self.gTimer.reset(2)
   
        # PREPRATORY PHASE
        elif self.state == self.gStates.WAIT_PREPRATORY:
            #ens_perc            = self.gTrial.EnsPercent/100
            #gBoxL.opacity       = 0.4
            #gBoxR.opacity       = 0.4
            #gBoxL.height        = ens_perc
            #gBoxR.height        = ens_perc
            #gEnsbarR.opacity  = 0.5
            #gEnsbarL.opacity  = 0.5
            #gEnsbarL.fillColor = 'LightPink'
            #gEnsbarR.fillColor = 'LightPink'
            gFixation.color     = 'white'
            for i in gFingers:
                i.opacity = 0.7

            if self.gTimer[2] > prep_time:
                gFixation.color                     = 'black'
                gTarget.opacity                     = 1
                gTarget.fillColor                   = 'grey'
                gTarget.lineColor                   = 'white'
                self.state                          = self.gStates.WAIT_RESPONSE
                self.gTimer.reset(2)
                                
        # WAIT_RESPONSE
        elif self.state == self.gStates.WAIT_RESPONSE:
            # calculate distance from target
            euc_dist    = np.linalg.norm(np.subtract(gFinger.pos,gTarget.pos))
            '''
            if bar_height >= box_height:
                gFinger.opacity    = 1
                gFinger.fillColor   = 'red'
                gEnsbarL.fillColor  = 'red'
                gEnsbarR.fillColor  = 'red'
                gTarget.opacity     = 0
                self.state = self.gStates.TRIAL_FAILED
                self.gTimer.reset(2)
            '''

            if self.gTimer[2] > resp_time:
                gFinger.opacity     = 0.95
                gFinger.fillColor   = 'red'
                gTarget.opacity     = 0
                self.state          = self.gStates.WAIT_RELEASE
                self.gTimer.reset(2)

            if euc_dist <= gTarget.radius:
                gFinger.opacity     = 0.95
                gFinger.fillColor   = 'green'
                self.state          = self.gStates.WAIT_RELEASE
                self.gTimer.reset(2)

        # WAIT_RELEASE
        elif self.state == self.gStates.WAIT_RELEASE:
            gFixation.color = 'white'
            euc_dist = np.linalg.norm(np.subtract(gFinger.pos,gFixation.pos))
            if self.gTimer[2] > target_remain:
                gTarget.opacity = 0

            if (euc_dist <= 0.05) or (self.gTimer[2] > wait_time):
                gTarget.opacity = 0
                self.state                          = self.gStates.TRIAL_COMPLETE
                self.gTimer.reset(2)
        # TRIAL_FAILED
        elif self.state == self.gStates.TRIAL_FAILED:
            '''
            gBoxL.opacity = 0
            gBoxR.opacity = 0
            gEnsbarL.opacity = 0
            gEnsbarRL.opacity = 0
            gBoxL.opacity = 0
            gBoxL.opacity = 0
            gFinger.opacity = 0
            gTarget.opacity = 0

            if gEnsbarL.fillColor == 'red':
                gWarnings.text = gWarnlist[0]
                gWarnings.color = 'white'
            else:
                gWarnings.text = gWarnlist[1]
                gWarnings.color = 'white'
            
            if gTimer[2] > wait_time:
                gWarnings.color = 'black'
                self.state = self.gStates.TRIAL_COMPLETE
                self.gTimer.reset(2)
            
            '''

        # TRIAL_COMPLETE
        elif self.state == self.gStates.TRIAL_COMPLETE:
            self.gVariables['measEndTime']      = self.gTimer[0]

            if self.gTimer[2] > dead_time:
                self.state          = self.gStates.END_TRIAL

            

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
    gExp.set_data_format(['TN','startTime','hand','digit','measStartTime','measEndTime', 'EnsPercent'])

    # initialize trial states
    gExp.set_trial_states('START_TRIAL', 'CUE_PHASE', 'WAIT_PREPRATORY', 'WAIT_RESPONSE','WAIT_RELEASE', 'TRIAL_FAILED', 'TRIAL_COMPLETE','END_TRIAL')

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

