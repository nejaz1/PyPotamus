# Experiment for hand assessment using the hopkins hand device
#
# Created:
# Nov 17: Naveed Ejaz


# 0. Import required modules
import sys
path    = '/Users/naveed/Dropbox/Code/experimentcode/PyPotamus/'
sys.path.append(path)

from PyPotamus import Experiment
from HopkinsHandDevice import HopkinsHandDevice

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
        f           = self.gTrial.Digit-1
        d           = self.gTrial.Dir                       

        if 1000.0 <= self.gTimer[0] < 4000.0:
            if d==1:
                fingers[f].pos += (0,0.01)
            elif d==2:
                fingers[f].pos -= (0,0.01)

    # this function is called when diagnostic info is about to be updated
    def updateDiagnostic(self):        
        self.gDiagnostic[0] = 'Subj:' + self.get_subject_id()
        self.gDiagnostic[1] = 'Timer:' + str(round(self.gTimer[0],1))
        self.gDiagnostic[2] = 'run:' + str(self.get_runno())
        self.gDiagnostic[3] = 'TN:' + str(self.gTrial.TN)        

    # over-load experimental trial loop function
    def trial(self):
        self.gTimer.reset_all()

        while self.gTimer[0] < 5000.0:  # clock times are in seconds
            self.flip()


# 3. Main entry point of program
if __name__ == "__main__":

    gHand  = HopkinsHandDevice()
    gHand.start()

    # 1. Set up experiment and initalize using default parameters in yaml file
    gExp = myExperiment()
    gExp.initialize(path + 'defaults.yaml')

    # turn on diagnostic screen for messages/state variables etc
    gExp.diagnostic('on')

    # initialize data format to save during experiment
    gExp.initialize_data_manager(['TN','startTime'])

    # initialize drawing elements on screen for speed (also for diagnostic messages)
    gExp.init_draw()

    # get user input via console
    # user commands starts/stops experiment
    gExp.control()
    gHand.terminate()
    gHand.join()

