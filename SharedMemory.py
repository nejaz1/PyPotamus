# Class to set up shared memory between multiprocesses in python
#
# Created:
# May 18: Naveed Ejaz

import multiprocessing as mp
from multiprocessing.sharedctypes import Value, Array
from ctypes import c_int, c_double
from Timer import Timer


class SharedMemory(object):
    # constructor
    def __init__(self, params):
        # parameters used for buffering data in multiprocess
        self.device_name    = params['device_name']             
        self.sampling_freq  = params['sampling_freq']     
        bf_size             = params['buffer_size']
        self.buffer_size    = bf_size[0] * bf_size[1]        

        self.timer          = Timer({'num_counter': 2})   

        # shared memory and locking        
        self.lock           = mp.RLock()
        self.nsamples       = Value(c_int, 0, lock=self.lock)
        self.logging        = Value(c_int, 0, lock=self.lock)        
        self.shared_mem     = Array(c_double,[0]*self.buffer_size, lock=self.lock)
        self.condition      = mp.Condition(self.lock)         

    # write to circular buffer
    def writeTo(self, values):
        with self.lock:
            self.nsamples.value                     %= self.buffer_size
            self.shared_mem[self.nsamples.value]    = values
            self.nsamples.value                     += 1

    # returns last valid item in buffer
    def getLastValue(self):
        with self.lock:
            return self.shared_mem[self.nsamples.value-1]

    # get copy of all valid items in buffer
    def getCopy(self):
        with self.lock:
            return self.shared_mem[0:self.nsamples.value].copy()
        
    # method that implement buffered sampling into shared memory
    def sampling_loop(self):
        print('Preparing to sample {} at {}ms'.format(self.device_name,self.sampling_freq))        
        
        t = self.timer
        t.reset_all()
        
        while True:
            with self.lock:
                if self.logging.value == 0:
                    print(self.device_name,' asleep')
                    self.condition.wait()
                    print(self.device_name,' awake')
                    t.reset_all()
                    continue
            
            if t[1] >= self.sampling_freq:
                t.reset(1)
                self.writeTo(t[0])                
#                print(t[0])
