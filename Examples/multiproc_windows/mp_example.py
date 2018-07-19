"""
Multiprocessing example in python
"""

from GenericHardwareWindows import GenericHardware
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class HopkinsHandDevice(GenericHardware):
    # constructor
    def __init__(self, params):
        GenericHardware.__init__(self,params)
        print('init complete')

# program entry point, assume this is pypotamus class 
if __name__ == "__main__":
    # Initialize handware manager, and add a device to sample
    gHand = HopkinsHandDevice({'device_name': 'hopkins hand device',
                               'sampling_freq': 1000,
                               'buffer_size': [100000, 1]})
    print('back out')

    # put main thread to sleep for 2s to show child is not running 
    # time.sleep(3)

    # # turn on child process for a few seconds
    gHand.startRecording()
    time.sleep(10)
    gHand.stopRecording()    

    # put main thread to sleep for 2s to show child is not running 
    time.sleep(3)

    # get data
    m = gHand.getBufferCopy()
    y = pd.DataFrame(m).round(0)
    x = pd.DataFrame(np.diff(m))

    # gracefully exit processes    
    gHand.terminate()    

    
