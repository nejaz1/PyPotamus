# Experiment for hand assessment using the hopkins hand device
#
# Created:
# Nov 17: Naveed Ejaz

# 0. Import required modules
import sys
path    = '/Users/naveed/Dropbox/Code/toolboxes/PyPotamus/'
sys.path.append(path)

from PyPotamus import Experiment
from Hardware import HardwareManager

# ------------------------------------------------------------------------
# 1. Inherited Experiment class in PyPotamus module
class myExperiment(Experiment):
    # quicker to pre-allocate drawing elements on the screen
    def init_draw(self):
        # 0. draw circles for fingers
        fingers = list()
        pos     = [[-0.8,0], [-0.4,0], [0,0], [0.4,0], [0.8,0]]

        for i in range(5):
            f = self.gScreen.circle(pos=pos[i], radius=0.1, lineWidth=3.0, lineColor='white', fillColor='lightblue')
            fingers.append(f)

        # 1. add fingers stimulus to dictionary of visual stimuli
        self.gScreen['fingers'] = fingers

    # this function is called when screen is about to be updated
    def updateScreen(self):        
        fingers     = self.gScreen['fingers']
        f           = self.gTrial.Digit - 1

        fingers[f].pos += self.update_pos

    # this function is called when diagnostic info is about to be updated
    def updateDiagnostic(self):        
        self.gDiagnostic[0] = 'Subj:' + self.get_subject_id()
        self.gDiagnostic[1] = 'Timer:' + str(round(self.gTimer[0],1))
        self.gDiagnostic[2] = 'Run:' + str(self.get_runno())
        self.gDiagnostic[3] = 'TN:' + str(self.gTrial.TN)        

    # over-load experimental trial loop function
    def trial(self):
        d           = self.gTrial.Dir                       

        # trial states here
        if self.state == self.gStates.START_TRIAL:

            self.update_pos = (0,0)

            if self.gTimer[0] > self.gTrial.StartTime:
                self.state = self.gStates.WAIT_TRIAL

        # trial ends here
        elif self.state == self.gStates.WAIT_TRIAL:

            if d == 1:
                self.update_pos = (0,0.01)
            elif d == 2:
                self.update_pos = (0,-0.01)

            if self.gTimer[0] > self.gTrial.EndTime:
                self.state = self.gStates.END_TRIAL


# ------------------------------------------------------------------------
# 3. Main entry point of program
if __name__ == "__main__":

    gHand = HardwareManager()
    gHand.start()

    # 1. Set up experiment and initalize using default parameters in yaml file
    gExp = myExperiment()
    gExp.initialize(path + 'defaults.yaml')

    # turn on diagnostic screen for messages/state variables etc
    gExp.diagnostic('on')

    # initialize data format to save during experiment
    gExp.initialize_data_manager(['TN','startTime'])

    # initialize trial states
    gExp.set_trial_states('START_TRIAL','WAIT_TRIAL','END_TRIAL')

    # initialize drawing elements on screen for speed (also for diagnostic messages)
    gExp.init_draw()

    # get user input via console
    # user commands starts/stops experiment
    gExp.control()
    gHand.terminate()
    gHand.join()
