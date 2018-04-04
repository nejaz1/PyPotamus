# Class to set up timers for the experiment
#
# Created:
# Nov 17: Naveed Ejaz
from psychopy import core

class Timer:
    internal_counter    = 0    # USED FOR INTERNAL CLOCKING, DO NOT CHANGE
    internal_resettime  = []
    multiplier  = 1000      # pyschopy measures in sec, convert to millisec
    nCounter    = 0
    counter     = []
    resettime   = []

    # constructor
    def __init__(self, params):
        # 0. set up internal and external clocks
        self.internal_counter = core.MonotonicClock()

        for i in range(params['num_counter']):
            self.counter.append(core.MonotonicClock())
            self.resettime.append(self.counter[i].getTime())
            self.nCounter += 1

        # 1. reset both internal and external clocks
        self.reset_internal_counter()
        self.reset_all()

    # returns current time (overloading the [] operator for the class)
    def __getitem__(self, index):
        return (self.counter[index].getTime() - self.resettime[index]) * self.multiplier

    # returns current internal counter time
    def get_internal_time(self):
        return (self.internal_counter.getTime() - self.internal_resettime) * self.multiplier        

    # reset internal counter
    def reset_internal_counter(self):
        self.internal_resettime = self.internal_counter.getTime()        

    # reset counter i
    def reset(self, index):
        self.resettime[index] = self.counter[index].getTime()

    # reset all counters
    def reset_all(self):
        for i in range(self.nCounter):
            self.resettime[i] = self.counter[i].getTime()

    # delete the timers when the object is destroyed
    def __del__(self):
        # 0. delete external clocks
        self.counter    = [] 
        self.resettime  = []
        self.nCounter   = 0

        # 1. delete internal clocks
        self.internal_counter   = []
        self.internal_resettime = []
