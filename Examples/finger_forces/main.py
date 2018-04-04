# Experiment for hand assessment using the hopkins hand device
#
# Created:
# Nov 17: Naveed Ejaz
# 
# IMPORTANT: Path to PyPotamus needs set to be in PYTHONPATH environment variable

from PyPotamus import Experiment
from HopkinsHandDevice import HopkinsHandDevice
import numpy as np
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
    def init_draw(self):
        # 0. draw circles for moving fingers and target stimulus
        target = self.gScreen.circle(pos=[0,0], radius=0.15, lineWidth=3.0, lineColor='red', fillColor='red')
        target.opacity = 0.0
        
        finger = self.gScreen.circle(pos=[0,0], radius=0.1, lineWidth=3.0, lineColor='white', fillColor='lightblue')

        # 1. add finger and target stimuli to dictionary of visual stimuli
        self.gScreen['finger']          = finger
        self.gScreen['target']          = target

    # this function is called when screen is about to be updated
    def updateScreen(self):     
        # update finger pos based on hardware readings
        self.gScreen['finger'].pos = self.gHardware['gHand'].getXY(self.gTrial.Digit - 1)
        
        # update target pos based on hardware readings
        self.gScreen['target'].pos = (self.gTrial.TargetX/10,self.gTrial.TargetY/10)

        euc_dist = np.linalg.norm(np.subtract(self.gScreen['finger'].pos,self.gScreen['target'].pos))
        if euc_dist <= self.gScreen['target'].radius:
            self.gScreen['target'].fillColor = 'green'
            self.gScreen['target'].lineColor = 'green'

    # this function is called when diagnostic info is about to be updated
    def updateDiagnostic(self):        
        self.gDiagnostic[0] = 'Subj:' + self.get_subject_id()
        self.gDiagnostic[1] = 'Timer:' + str(round(self.gTimer[0],1))
        self.gDiagnostic[2] = 'Run:' + str(self.get_runno())
        self.gDiagnostic[3] = 'TN:' + str(self.gTrial.TN)        

    # over-load experimental trial loop function
    def trial(self):
        forces      = self.gHardware['gHand'].getRaw()
        target      = self.gScreen['target']

        print(np.array_str(forces, max_line_width=1000, precision=1, suppress_small=True))
        
        # START_TRIAL
        if self.state == self.gStates.START_TRIAL:
            target.fillColor = 'red'
            target.lineColor = 'red'

            if self.gTimer[0] > self.gTrial.StartTime:
                # log trial start time
                self.gVariables['measStartTime']    = self.gTimer[0]
                self.state                          = self.gStates.WAIT_TRIAL
                target.opacity                      = 1.0

        # WAIT_TRIAL
        elif self.state == self.gStates.WAIT_TRIAL:

            if self.gTimer[0] > self.gTrial.EndTime:
                # log trial end time
                self.gVariables['measEndTime']      = self.gTimer[0]
                self.state                          = self.gStates.END_TRIAL
                target.opacity                      = 0.0

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
    gExp.initialize('defaults.yaml')

    # turn on diagnostic screen for messages/state variables etc
    gExp.diagnostic('on')

    # initialize data directory and format to save during experiment
    gExp.set_data_directory('/Users/naveed/Dropbox/Code/toolboxes/PyPotamus/Examples/finger_forces/data/')
    gExp.set_data_format(['TN','startTime','endTime','hand','digit','measStartTime','measEndTime'])

    # initialize trial states
    gExp.set_trial_states('START_TRIAL','WAIT_TRIAL','END_TRIAL')

    # initialize drawing elements on screen for speed (also for diagnostic messages)
    gExp.init_draw()

    # attached hopkins hand device as part of experiment (call it gHand)
    gExp.add_hardware('gHand',HopkinsHandDevice())
    gExp.gHardware['gHand'].set_force_multiplier((-3,3,3))

    # get user input via console
    # user commands starts/stops experiment
    gExp.control()
    # gHand.terminate()
    # gHand.join()
