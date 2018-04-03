# Main PyPotamus Class
#
# Created:
# Nov 24: Naveed Ejaz
import yaml
import abc
import pdb
import sys

# Load PyPotamus libraries
from ExperimentDisplay import ExperimentDisplay
from DiagnosticDisplay import DiagnosticDisplay
from Timer import Timer
from DataManager import DataManager
from Keyboard import Keyboard
from TargetFile import TargetFile


class Experiment:
    __metaclass__  = abc.ABCMeta

    # constructor
    def __init__(self):
        self.pythonver  = sys.version_info[:2]
        if self.pythonver < (3,6):
            print("Please run with python version 3.6 or higher")
            sys.exit(0)
        else:
            print("Current python version is " + str(self.pythonver))

    # initialize experiment with defaults provided in yaml file
    def initialize(self, filepath):
        self.gParams = yaml.load(open(filepath))                # load defaults
        self.gScreen = ExperimentDisplay(self.gParams)          # exp display
        self.gTimer  = Timer(self.gParams)                      # timers
        self.gData   = DataManager(self.gParams)                # data manager
        self.gDiagnostic    = DiagnosticDisplay(self.gParams)   # diagnostic window
        self.gKeyboard      = Keyboard(self.gParams)            # keyboard input polling
        self.gStates        = []                                # trial states 
        self.gHardware      = []                                # hardware used for experiment    

    # initialize data manager and provide format to expect data in
    def initialize_data_manager(self, dataformat):
        self.gData.init_data_manager(dataformat)

    # set subject id (used by data manager as file name to save data to disk)
    def set_subject_id(self, subject_id):
        self.gData.set_subject_id(subject_id)

    # set states used to progress through a trial
    def set_trial_states(self, *sequential, **named):
        enums           = dict(zip(sequential, range(len(sequential))), **named)
        self.gStates    = type('Enum', (), enums)       

    # get subject id
    def get_subject_id(self):
        return self.gData.subject_id

    # get run number
    def get_runno(self):
        return self.gData.run        

    # toggle diagnostic window
    def diagnostic(self,mode):
        self.gDiagnostic.diagnostic(mode,self.gParams)

    # start run in experiment
    def start_run(self):
        # posting run starting message  
        self.gData.add_dbg_event('starting run ' + str(self.get_runno()))

        # reset all timers at the start of the run
        self.gTimer.reset_all()

        # loop over all trials in the target file
        for i in range(self.gTrial.getTrialNum()):
            # run abstract function for each trial
            self.state = 0

            while self.state != self.gStates.END_TRIAL:
                self.trial()
                self.flip()

            # go to next trial
            self.gTrial.nextTrial()

        # posting run ending message  
        self.gData.add_dbg_event('run successfully completed')
        pdb.set_trace()

    # flip screen buffers
    def flip(self):
        if self.gScreen.handle != []:
            self.updateScreen()
            self.gScreen.handle.flip()

        if self.gDiagnostic.handle != []:
            self.updateDiagnostic()
            self.gDiagnostic.handle.flip()            

    # close all screens associated with experiment
    def close_screens(self):
        self.gScreen.close()
        self.gDiagnostic.close()

    def control(self):
        while True:
            resp = self.gKeyboard.poll(self.get_subject_id())

            if resp[0] == 'quit':
                self.exit()
                break        

            elif resp[0] == 'run':
                self.gData.run  = resp[1]
                self.gTrial     = TargetFile(resp[2])
                self.start_run()

            elif resp[0] == 'subj':
                self.set_subject_id(resp[1])

    # close all windows and clear memory
    def exit(self):
        self.close_screens()
        del self.gTimer
        del self.gData
        del self.gScreen
        del self.gDiagnostic
        del self.gKeyboard
        del self.gParams
        del self.gHardware

    # main experiment loop for each trial
    # provided as an abstract function to be overloaded by inheriting class
    @abc.abstractmethod
    def trial(self):
        """Main experiment trial loop provided by the base class"""

    # main drawing function to be called prior to screen refresh
    # provided as an abstract function to be overloaded by inheriting class
    @abc.abstractmethod
    def updateScreen(self):
        """main drawing function to be called prior to screen refresh"""         

    # main updating function to be called prior to diagnostic info refresh
    # provided as an abstract function to be overloaded by inheriting class
    def updateDiagnostic(self):
        """main drawing function to be called prior to diagnostic info refresh"""  
