# Main PyPotamus Class
#
# Created:
# Nov 24: Naveed Ejaz
import yaml
from psychopy import visual, core

# Load PyPotamus libraries
from ExperimentDisplay import ExperimentDisplay
from TextDisplay import TextDisplay
from Timer import Timer
from DataManager import DataManager

class Experiment:
    BN      = 0
    TN      = 0
    state   = 0

    # constructor
    def __init__(self, path):
        self.gParams = yaml.load(open(path + 'defaults.yaml'))  # load defaults
        self.gScreen = ExperimentDisplay(self.gParams)          # exp display
        self.gText   = TextDisplay(self.gParams)                # text display
        self.gTimer  = Timer(self.gParams)                      # timers
        self.gData   = DataManager(self.gParams)                # data manager

    # close all windows and clear memory
    def exit(self):
        self.gParams    = []
        self.gScreen.close()
        self.gText.close()
        del self.gTimer
        del self.gData

