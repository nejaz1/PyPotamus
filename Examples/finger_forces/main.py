# Experiment for hand assessment using the hopkins hand device
#
# Created:
# Nov 17: Naveed Ejaz


# 0. Import required modules
import sys
path    = '/Users/naveed/Dropbox/Code/experimentcode/PyPotamus/'
sys.path.append(path)

from PyPotamus import Experiment
import pdb

# 1. Inherited Experiment class in PyPotamus module
class myExperiment(Experiment):
    
    # quicker to pre-allocate drawing elements on the screen
    def init_draw(self):
        # draw gabor function in experimental window
        self.gabor = self.gScreen.grating(tex='sin', mask='gauss', sf=10, name='gabor')

        # print timer on screen
        self.txt = self.gDiagnostic.write('init')

    # over-load experimental trial loop function
    def trial(self):
        self.gTimer.reset_all()

        while self.gTimer[0] < 5000.0:  # clock times are in seconds
            if 1000.0 <= self.gTimer[0] < 4000.0:
                self.gabor.setPhase(0.1, '+')  # increment by 10th of cycle
                self.gData.add_dbg_event('tick')
            self.txt.setText(self.gTimer[0])
            self.gDiagnostic.flip()
            self.gScreen.flip()


# 2. Main entry point of experiment
if __name__ == "__main__":
    
    # 1. Set up experiment and initalize using default parameters in yaml file
    gExp = myExperiment()
    gExp.initialize(path + 'defaults.yaml')

    # turn on diagnostic screen for messages/state variables etc
    gExp.diagnostic('on')

    # initialize data format to save during experiment
    gExp.set_subject_id('s01')
    gExp.initialize_data_manager(['TN','startTime'])

    # initialize drawing elements on screen for speed
    gExp.init_draw()

    # start main experiment
    gExp.start()
    gExp.close_screens()
    pdb.set_trace()
        
    # stop experiment, cleanup memory and look at data generated
    gExp.stop()

