# Class to store hardware associated with the main experiment
#
# Created:
# Nov 17: Naveed Ejaz

class HardwareManager:
    hardware_dict   = []

    # constructor
    def __init__(self, params):
        self.hardware_dict  = dict()

    # sets the current line to the diagnostic text
    def __setitem__(self, key, item):
        self.hardware_dict[key] = item

    # sets the current line to the diagnostic text
    def __getitem__(self, key):
        return self.hardware_dict[key]
