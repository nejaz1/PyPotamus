# Class to set up a generic hardware device attached to PyPotamus class
# Provides multithreading, with read/writes to a shared circular buffer array
#
# Created:
# May 18: Naveed Ejaz

import multiprocessing as mp
from multiprocessing.sharedctypes import Value, Array
from ctypes import c_int, c_double
from Timer import Timer
import abc
import numpy as np
import pandas as pd

import pdb
class GenericHardware(object):
    # constructor
    def __init__(self, params):
        # parameters used for buffering data in multiprocess
        self.device_name    = params['device_name']             
        self.sampling_freq  = params['sampling_freq']
        self.shape          = params['buffer_size']     
        self.buffer_size    = self.shape[0] * self.shape[1]
        self.last = 0     

        # shared memory and locking        
        self.lock           = mp.RLock()
        self.nsamples       = Value(c_int, 0, lock=self.lock)
        self.logging        = Value(c_int, 0, lock=self.lock)
        self.shared_mem     = Array(c_double,[0] * self.buffer_size, lock=self.lock)
        self.condition      = mp.Condition(self.lock)         

        # state of the trial
        self.state          = Value(c_int, 0, lock=self.lock)
        self.BN             = Value(c_int, 0, lock=self.lock)        
        self.TN             = Value(c_int, 0, lock=self.lock)

        # spawn process for logging
        self.spawnProcess()

    # spawn process to sample data
    def spawnProcess(self):
        self.process = mp.Process(name=self.device_name, target=self.sampling_loop) 
        self.process.start()            

    # get process name
    def processName(self):
        return mp.current_process().name
        
    # terminate processes
    def terminate(self):
        if self.process.is_alive():
            self.process.terminate()
            
    # start recording data
    def startRecording(self):
        with self.lock:
            self.nsamples.value  = 0
            self.logging.value   = 1
            self.condition.notify()
            
    # stop recording data
    def stopRecording(self):
        with self.lock:
            self.logging.value = 0

    # write to circular buffer
    def writeToBuffer(self, values):
        with self.lock:
            self.nsamples.value                     %= self.buffer_size
            self.shared_mem[self.nsamples.value]    = values
            self.nsamples.value                     += 1

    # write record to buffer
    def writeRecord(self, time, raw_values):
        with self.lock:
            self.nsamples.value     %= self.buffer_size  # so that program does not crash

            idx     = self.nsamples.value
            n       = len(raw_values)
            state   = self.state.value
            bn      = self.BN.value
            tn      = self.TN.value

            self.shared_mem[idx]            = time
            self.shared_mem[idx+1]          = bn
            self.shared_mem[idx+2]          = tn
            self.shared_mem[idx+3]          = state

            self.shared_mem[idx+4:idx+4+n]  = raw_values

            self.nsamples.value                     += n+4

    # sets value of the state variable
    def setState(self, blockNo, trialNo, state):
        with self.lock:
            self.BN.value       = blockNo
            self.TN.value       = trialNo
            self.state.value    = state

    # returns last valid item in buffer
    def getLastValue(self):
        with self.lock:
            return self.shared_mem[self.nsamples.value - 1]

    # get copy of all valid items in buffer as a dataframe
    def getBufferAsDataFrame(self):
        with self.lock:
            d       = self.shared_mem[0:self.nsamples.value].copy()
            
            nrow    = round(len(d)/self.shape[1])
            ncol    = self.shape[1] 

            return pd.DataFrame(np.array(d).reshape((nrow,ncol)))

    # get copy of all valid items in buffer as a list
    def getBufferAsArray(self):
        with self.lock:
            d       = self.shared_mem[0:self.nsamples.value].copy()
            
            nrow    = round(len(d)/self.shape[1])
            ncol    = self.shape[1] 

            return np.array(d).reshape((nrow,ncol))

    def getBufferAsArrayLAST(self):
        with self.lock:
            d = self.shared_mem[self.last:self.nsamples.value].copy()
            self.last = self.nsamples.value    

            nrow = round(len(d)/self.shape[1])
            ncol = self.shape[1]

            matrix = np.array(d).reshape((nrow,ncol))             
            return matrix[:,4:]   


    # method that implement buffered sampling into shared memory
    def sampling_loop(self):
        print('Preparing to sample {} at {}ms'.format(self.processName(),self.sampling_freq))        
        self.initialize()

        # internal timer 
        t = Timer({'num_counter': 2})   
        t.reset_all()

        while True:
            with self.lock:
                if self.logging.value == 0:
                    print('{} stopped recording'.format(self.device_name))
                    self.condition.wait()
                    print('{} started recording'.format(self.device_name))
                    t.reset_all()
                    continue
            
            if t[1] >= self.sampling_freq:
                t.reset(1)
                # self.writeToBuffer(t[0]) 
                data = self.onUpdate() 
                self.writeRecord(t[0],data)           

    # virtual function provide device initialization capability 
    # put all custom initialization code here
    @abc.abstractmethod
    def initialize(self):
        """main function to be called to initialize hardware device"""                         

    # on update function called by base multiprocessing GenericHardware class 
    # put all custom data/writing to buffer here
    @abc.abstractmethod
    def onUpdate(self):
        """main function to be called to update buffer data"""         