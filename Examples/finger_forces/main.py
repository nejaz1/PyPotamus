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
        warnings = self.gScreen.text(text='', pos=(0,-0.1), color='black')
        boxL = self.gScreen.rect(pos=[-0.95,0], width=0.05, height=1, lineWidth = 5, lineColor = 'white', fillColor = 'white')
        boxR = self.gScreen.rect(pos=[0.95,0], width=0.05, height=1, lineWidth = 5, lineColor = 'white', fillColor = 'white')
        fixation = self.gScreen.text(text='+', pos=[0,0.02], color='white', height=0.3)
        ensbarL = self.gScreen.rect(pos=[-0.95,0], width=0.05, height=0.0, lineWidth = 1, lineColor = 'black', fillColor = 'LightPink')
        ensbarR = self.gScreen.rect(pos=[0.95,0], width=0.05, height=0.0, lineWidth = 1, lineColor = 'black', fillColor = 'LightPink')
        text = self.gScreen.text(text='', pos=(0,0.95), color='white')
        target = self.gScreen.circle(pos=[0,0], radius = 0.1, lineWidth=4.0, lineColor='black', fillColor='black')
        finger = self.gScreen.circle(pos=[0,0],radius = 0.08, lineWidth = 3.0, lineColor = 'white', fillColor = 'grey')
        digit = self.gScreen.circle(pos=[0,0],radius = 0.05, lineWidth = 3.0, lineColor = 'white', fillColor = 'blue')
        posList = [(-0.45,0.01),(-0.21, 0.42),(0.03,0.5),(0.22,0.48),(0.38,0.28)]
        colorList = ['#AFADF5', '#E3CBA0', '#DE4CBA', 'blue', 'yellow']

    
        target.opacity = 0.0
        ensbarL.opacity = 0.0
        ensbarR.opacity = 0.0
        finger.opacity = 0.0
        boxL.opacity = 0.0
        boxR.opacity = 0.0
        img.opacity = 0.0
        digit.opacity = 0.0
        text.color  = 'black'

        #   - save objects to dictionary for easy access
        #self.gScreen['finger1']          = finger1
        self.gScreen['finger']          = finger
        self.gScreen['digit']           = digit
        self.gScreen['ensbarL']         = ensbarL
        self.gScreen['ensbarR']         = ensbarR
        self.gScreen['boxL']            = boxL
        self.gScreen['boxR']            = boxR
        self.gScreen['target']          = target
        self.gScreen['text']            = text
        self.gScreen['warnings']         = warnings
        
        self.gScreen['fixation']        = fixation 
        self.gScreen['handimage']       = img
        self.gScreen['posList']         = posList
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
        gFinger     = self.gScreen['finger']
        gEnsbarL    = self.gScreen['ensbarL']
        gEnsbarR    = self.gScreen['ensbarR']
        gTarget     = self.gScreen['target']
        gBoxL       = self.gScreen['boxL']
        gBoxR       = self.gScreen['boxR']
        gHandimage  = self.gScreen['handimage']
        gText       = self.gScreen['text']
        dig = int(self.gTrial.Digit)
        
        # update finger pos and raidus based on hardware readings during the appropriate phases
        if self.state == self.gStates.WAIT_PREPRATORY or self.gStates.WAIT_RESPONSE or self.gStates.WAIT_RELEASE: 
            
            pos             = self.gHardware['gHand'].getXYZ(dig - 1)
            gFinger.pos     = [(pos[0]), (pos[1])]
             #gFinger.radius  = 0.05 + pos[2]/1.5

            #update ens bars based on hardware reading
            rms         = self.gHardware['gHand'].getXY_RMSForces(dig - 1)
            ens_perc    = self.gTrial.EnsPercent/100
            max_rms     = np.sqrt((2 * np.square(0.9)))
            rms_lim     = ens_perc*max_rms
            ens_visual  = ens_perc*(rms/rms_lim)
        
            gEnsbarL.height = min(ens_visual, gBoxL.height)
            gEnsbarR.height = min(ens_visual, gBoxR.height)

      
    
        # update target pos based on hardware readings
     
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
        gText       = self.gScreen['text']
        gDigit      = self.gScreen['digit']
        gPoslist       = self.gScreen['posList']
        gColorlist  = self.gScreen['colorList']
        gWarnings   = self.gScreen['warnings']
        gWarnlist   = self.gScreen['warnList']
        dig = int(self.gTrial.Digit)

        # set time limits for different phases of the trial
        cue_time = 3000
        prep_time = 1000
        resp_time  = 10000
        return_time  = 5000
        target_remain = 750
        finger_remain = 750
        dead_time  = 3000
        '''
        within loop, find pos
        '''

        # START TRIAL
        if self.state == self.gStates.START_TRIAL:          
                #set state to cue phase, and log the start of the trial 
                self.state = self.gStates.CUE_PHASE
                self.gVariables['measStartTime']    = self.gTimer[0]
                # set target location for the trial, and hide from view 
                gTarget.opacity = 0

                x = self.gTrial.TargetX/10
                
                y = self.gTrial.TargetY/10

                gTarget.pos = (x,y)
                gFixation.color = 'black'
                #set up display to appear during the cue phase
        
                gText.text = self.gScreen['fingerLabels'][dig - 1]
                gText.color = 'white'
                gHandimage.opacity  = 0.9
                gDigit.pos = gPoslist[(dig - 1)]
                gDigit.fillColor   = gColorlist[dig - 1]
                gDigit.opacity = 1

                #reset the internal between phase timer (gTimer2)
                self.gTimer.reset(1)


        # CUE PHASE
        elif self.state == self.gStates.CUE_PHASE:
            if self.gTimer[1] > cue_time:
                # hide hand
                gHandimage.opacity                  = 0.0
                gDigit.opacity                      = 0.0
                gText.color = 'black'
                #display the shapes involved in the next phase
                ens_perc            = self.gTrial.EnsPercent/100
                gBoxL.opacity       = 0.4
                gBoxR.opacity       = 0.4
                gBoxL.height        = ens_perc
                gBoxR.height        = ens_perc
                gEnsbarR.opacity  = 0.5
                gEnsbarL.opacity  = 0.5
                gEnsbarL.fillColor = 'LightPink'
                gEnsbarR.fillColor = 'LightPink'
                gFinger.opacity     = 0.7
                gFinger.fillColor   = gColorlist[dig - 1]         
                gFixation.color     = 'white'
 
                # swtich phase and reset timer
                self.state                          = self.gStates.WAIT_PREPRATORY
                self.gTimer.reset(1)

   
        # PREPRATORY PHASE
        elif self.state == self.gStates.WAIT_PREPRATORY:
            #wait for the time period to be over
            if self.gTimer[1] > prep_time:
                # update what is to be shown on screen for next phase
                gFixation.color                     = 'black'
                gTarget.opacity                     = 1
                gTarget.fillColor                   = 'grey'
                gTarget.lineColor                   = 'white'

                #change phase and reset timer
                self.state                          = self.gStates.WAIT_RESPONSE
                self.gTimer.reset(1)

                                
        # WAIT_RESPONSE
        elif self.state == self.gStates.WAIT_RESPONSE:
            # calculate distance from target and keep track of the ens bars continually
            euc_dist    = np.linalg.norm(np.subtract(gFinger.pos,gTarget.pos))
            bar_height  = gEnsbarL.height
            box_height  = gBoxL.height
            #if the finger reaches the target
            if euc_dist <= gTarget.radius:
                gFinger.opacity     = 0.95
                gFixation.color = 'white'
                gFinger.fillColor   = 'green'
                self.state          = self.gStates.WAIT_RELEASE
                self.gTimer.reset(1)

            # if the ens bars get to large
            if bar_height >= box_height:
                gFinger.opacity    = 0.95
                gFinger.fillColor   = 'red'
                gEnsbarL.fillColor  = 'red'
                gEnsbarR.fillColor  = 'red'
                gTarget.opacity     = 0
                self.state = self.gStates.TRIAL_FAILED
            # if the resp time is up
            if self.gTimer[1] > resp_time:
                gFinger.opacity     = 0.95
                gFinger.fillColor   = 'red'
                gTarget.opacity     = 0
                self.state          = self.gStates.TRIAL_FAILED
            #checks if we have trigged a failed trial
            if self.state == self.gStates.TRIAL_FAILED:
                #if so, what is the reason, and display the appropriate text, and hide the appropriate shapes (and resetting timer)
                if gEnsbarL.fillColor == 'red':
                    gFinger.opacity = 0
                    gWarnings.text = gWarnlist[0]
                    gWarnings.color = 'white'
                    self.gTimer.reset(1)

                else:
                    gFinger.opacity = 0
                    gWarnings.text = gWarnlist[1]
                    gWarnings.color = 'white'
                    gBoxL.opacity = 0
                    gBoxR.opacity = 0
                    gEnsbarL.opacity = 0
                    gEnsbarR.opacity = 0
                    gFinger.opacity = 0
                    gTarget.opacity = 0
                    self.gTimer.reset(1)


        # WAIT_RELEASE
        elif self.state == self.gStates.WAIT_RELEASE:
            #calculate euclidian distance from finger to fixation cross continually
            euc_dist = np.linalg.norm(np.subtract(gFinger.pos,gFixation.pos))

            #this allows for the target to remain on screen breifly, before leaving
            if self.gTimer[1] > target_remain:
                gTarget.opacity = 0

            #check to see if the finger has returned to the cross, and locks finger position 
            if (euc_dist <= 0.05):  
                pos = self.gHardware['gHand'].getXY(dig - 1)
                gFinger.pos                         = pos
                gTarget.opacity = 0
                gBoxL.opacity       = 0
                gBoxR.opacity       = 0
                gEnsbarR.opacity  = 0
                gEnsbarL.opacity  = 0
                self.state                          = self.gStates.TRIAL_COMPLETE
                self.gVariables['measEndTime']      = self.gTimer[0]
                self.gTimer.reset(1)


            # if the time for the phase is over, hide finger and move to next
            if (self.gTimer[1] > return_time):
                gFinger.opacity = 0
                gFixation.color = 'black'
                gBoxL.opacity       = 0
                gBoxR.opacity       = 0
                gEnsbarR.opacity  = 0
                gEnsbarL.opacity  = 0
                self.state                          = self.gStates.TRIAL_COMPLETE
                self.gVariables['measEndTime']      = self.gTimer[0]
                self.gTimer.reset(1)


        # TRIAL_FAILED
        elif self.state == self.gStates.TRIAL_FAILED:
            # checks to see if time has run out for the phase
            if self.gTimer[1] > return_time:
                #hide shapes on screen
                gWarnings.text = ''
                gBoxL.opacity = 0
                gBoxR.opacity = 0
                gEnsbarL.opacity = 0
                gEnsbarR.opacity = 0
                #swtiches state, logs end of the trial time and resests internal timer
                self.state = self.gStates.TRIAL_COMPLETE
                self.gVariables['measEndTime']      = self.gTimer[0]
                self.gTimer.reset(1)


        # TRIAL_COMPLETE
        elif self.state == self.gStates.TRIAL_COMPLETE:
            if self.gTimer[1] > finger_remain:
                gFinger.opacity = 0
                gFixation.color = 'black'
             
            #waits for between trial time to elapse, before ending trial
            if self.gTimer[1] > dead_time:
                self.state          = self.gStates.END_TRIAL


            

    # adding trial data on trial end
    def onTrialEnd(self):
        gTrial = self.gTrial
        gVar = self.gVariables
        self.gData.add_data_record([gTrial.TN, gTrial.Hand, gTrial.Digit, gVar['measStartTime'], gVar['measEndTime'], gTrial.EnsPercent])


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
    gExp.set_data_format(['TN','hand','digit','measStartTime','measEndTime', 'EnsPercent'])

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

