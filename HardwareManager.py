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

    
    # spawn multiprocesses to start sampling from all the 
    # attached hardware devices
    # each hardware device needs to implement its own buffered reading
    # method called sample
    def startRecording(self):    
        for _,value in self.hardware_dict.items():
            value.startRecording()


    # terminate all processes gracefully on death of main thread
    def stopRecording(self):
        for _,value in self.hardware_dict.items():
            value.stopRecording()
    