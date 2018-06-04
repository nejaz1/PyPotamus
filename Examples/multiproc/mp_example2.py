"""
Multiprocessing example in python
"""

from Timer import Timer
from multiprocessing import Process, Value, Condition
from ctypes import c_int, c_double
import multiprocessing as mp 
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def consumer(lock,condition,logging):
    print('consumer started')    
    sampling_freq = 1000                        
    t = Timer({'num_counter': 2})   
    t.reset_all()
    
    while True:
#        lock.acquire()
        with lock:
            if logging.value == 0:
                print('child stopped')
                condition.wait()
                print('child awake')                
                t.reset_all()
                continue

 #       lock.release()

        
        if t[1] >= sampling_freq:
            t.reset(1)
            print(t[0])
    
# program entry point, assume this is pypotamus class 
if __name__ == "__main__":
    # locks and data types
    lock           = mp.RLock()
    logging        = Value(c_int, 0, lock=lock)   
    condition      = Condition(lock)     

    p = Process(target=consumer, args=(lock,condition,logging)) 
    p.start()
    
    # demonstrate child has not started
    print('Main thread going to sleep') 
    time.sleep(3)
    print('main thread awake')
    
    # run child for 6 seconds
    t = Timer({'num_counter': 1})  
    t.reset(0)
    with lock:
        logging.value = 1            
        condition.notify()
    x = t[0]
    print(x)    
    time.sleep(6)
    
    # stop child for 6 seconds
    with lock:
        logging.value = 0            


    print('Main thread going to sleep') 
    time.sleep(5)
    print('main thread awake, terminating child')
    
    p.terminate()
    
    
    
