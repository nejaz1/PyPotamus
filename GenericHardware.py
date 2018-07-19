# Class to set up a generic hardware device attached to PyPotamus class
# Provides multithreading, with read/writes to a shared circular buffer array
#
# Created:
# May 18: Naveed Ejaz

import multiprocessing as mp
from multiprocessing.sharedctypes import Value, Array
from ctypes import c_int, c_double
from Timer import Timer


class GenericHardware(object):
    # constructor
    def __init__(self, params):
        # parameters used for buffering data in multiprocess
        self.device_name    = params['device_name']             
        self.sampling_freq  = params['sampling_freq']     
        bf_size             = params['buffer_size']
        self.buffer_size    = bf_size[0] * bf_size[1]        

        # internal timer (moved to within update loop)
        # for windows this needs to be within update loop or multiproc doesn't work
        # self.timer          = Timer({'num_counter': 2})   

        # shared memory and locking        
        self.lock           = mp.RLock()
        self.nsamples       = Value(c_int, 0, lock=self.lock)
        self.logging        = Value(c_int, 0, lock=self.lock)        
        self.shared_mem     = Array(c_double,[0]*self.buffer_size, lock=self.lock)
        self.condition      = mp.Condition(self.lock)         
        
        # spawn process for logging
        self.spawnProcess()

    # spawn process to sample data
    def spawnProcess(self):
        self.process = mp.Process(target=self.sampling_loop) 
        self.process.start()            
        
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

    # returns last valid item in buffer
    def getLastValue(self):
        with self.lock:
            return self.shared_mem[self.nsamples.value-1]

    # get copy of all valid items in buffer
    def getBufferCopy(self):
        with self.lock:
            return self.shared_mem[0:self.nsamples.value].copy()
        
    # method that implement buffered sampling into shared memory
    def sampling_loop(self):
        print('Preparing to sample {} at {}ms'.format(self.device_name,self.sampling_freq))        
        
        t = Timer({'num_counter': 2})   
        t.reset_all()
        
        while True:
            with self.lock:
                if self.logging.value == 0:
                    print('{} is going to sleep'.format(self.device_name))
                    self.condition.wait()
                    print('{} woke up'.format(self.device_name))
                    t.reset_all()
                    continue
            
            if t[1] >= self.sampling_freq:
                t.reset(1)
                self.writeToBuffer(t[0])                
#                print(t[0])
                
