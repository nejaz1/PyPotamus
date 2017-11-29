# Main PyPotamus Class
#
# Created:
# Nov 24: Naveed Ejaz
import yaml
import abc

# Load PyPotamus libraries
from ExperimentDisplay import ExperimentDisplay
from DiagnosticDisplay import DiagnosticDisplay
from Timer import Timer
from DataManager import DataManager

class Experiment:
    __metaclass__  = abc.ABCMeta

    # constructor
    def __init__(self):
        """Constructor purposely left empty"""

    # initialize experiment with defaults provided in yaml file
    def initialize(self, filepath):
        self.gParams = yaml.load(open(filepath))                # load defaults
        self.gScreen = ExperimentDisplay(self.gParams)          # exp display
        self.gTimer  = Timer(self.gParams)                      # timers
        self.gData   = DataManager(self.gParams)                # data manager
        self.gDiagnostic    = DiagnosticDisplay(self.gParams)   # diagnostic window

    # initialize data manager and provide format to expect data in
    def initialize_data_manager(self, dataformat):
        self.gData.init_data_manager(dataformat)

    # set subject id (used by data manager as file name to save data to disk)
    def set_subject_id(self, subject_id):
        self.gData.set_subject_id(subject_id)

    # get subject id
    def get_subject_id(self):
        return self.gData.subject_id

    # toggle diagnostic window
    def diagnostic(self,mode):
        self.gDiagnostic.diagnostic(mode,self.gParams)

    # start main experiment
    def start(self):
        self.gData.add_dbg_event('start')
        self.trial()

    # stop main experiment
    def stop(self):
        self.gData.add_dbg_event('stop')
        self.exit()        

    # flip screen buffers
    def flip(self):
        if self.gScreen.handle != []:
            self.gScreen.handle.flip()

        if self.gDiagnostic.handle != []:
            self.gDiagnostic.handle.flip()            

    # close all screens associated with experiment
    def close_screens(self):
        self.gScreen.close()
        self.gDiagnostic.close()

    # close all windows and clear memory
    def exit(self):
        self.gParams    = []
        self.gScreen.close()
        self.gDiagnostic.close()
        del self.gTimer
        del self.gData

    # main experiment loop for each trial
    # provided as an abstract function to be overloaded by inheriting class
    @abc.abstractmethod
    def trial(self):
         """Main experiment trial loop provided by the base class"""
