"""
Multiprocessing example in python
"""

from SharedMemory import SharedMemory
from multiprocessing import Process
import multiprocessing as mp 
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

class HopkinsHandDevice(object):
    # constructor
    def __init__(self, params):
        self.name           = params['device_name']
        self.sampling_freq  = params['sampling_freq']
        self.buffer_size    = params['buffer_size']  

        # create memory buffer and spawn processes for sampling        
        self.buffer = SharedMemory(params)
        self.spawn()

    # spawn process to sample data
    def spawn(self):
        self.process = Process(target=self.buffer.sampling_loop) 
        self.process.start()            
        
    # terminate processes
    def terminate(self):
        if self.process.is_alive():
            self.process.terminate()
            
    # start recording data
    def startRecording(self):
        with self.buffer.lock:
            self.buffer.nsamples.value  = 0
            self.buffer.logging.value   = 1
            self.buffer.condition.notify()
            
    # stop recording data
    def stopRecording(self):
        with self.buffer.lock:
            self.buffer.logging.value = 0
    
# program entry point, assume this is pypotamus class 
if __name__ == "__main__":

    # Initialize handware manager, and add a device to sample
    gHand = HopkinsHandDevice({'device_name': 'hopkins hand device',
                               'sampling_freq': 1,
                               'buffer_size': [10000, 1]})

    # put main thread to sleep for 2s to show child is not running 
    print('main thread going to sleep')    
    time.sleep(2)
    print('main thread awake')

    # turn on child process for a few seconds
    gHand.startRecording()
    time.sleep(6)
    gHand.stopRecording()    

    # put main thread to sleep for 2s to show child is not running 
    print('main thread going to sleep')    
    time.sleep(2)
    print('main thread awake')

    # get data
    m = gHand.buffer.getCopy()
    y = pd.DataFrame(m).round(0)
    x = pd.DataFrame(np.diff(m))

    # gracefully exit processes    
    gHand.terminate()    

    
