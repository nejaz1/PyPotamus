# Class to store variables generated during main experiment
#
# Created:
# Nov 17: Naveed Ejaz

class Variables:
    variable_dict   = []

    # constructor
    def __init__(self, params):
        self.variable_dict  = dict()

    # sets the current line to the diagnostic text
    def __setitem__(self, key, item):
        self.variable_dict[key] = item

    # sets the current line to the diagnostic text
    def __getitem__(self, key):
        return self.variable_dict[key]
