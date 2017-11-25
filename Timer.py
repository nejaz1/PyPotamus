# Class to set up timers for the experiment
#
# Created:
# Nov 17: Naveed Ejaz
from psychopy import core

class Timer:
    nCounter    = 0
    counter     = []
    resettime   = []

    # constructor
    def __init__(self, params):
        for i in range(params['num_counter']):
            self.counter.append(core.MonotonicClock())
            self.resettime.append(self.counter[i].getTime())
            self.nCounter += 1
        self.reset_all()

    # returns current time (overloading the [] operator for the class)
    def __getitem__(self, index):
        return (self.counter[index].getTime() - self.resettime[index])

    # reset counter i
    def reset(self, index):
        self.resettime[index] = self.counter[index].getTime()

    # reset all counters
    def reset_all(self):
        for i in range(self.nCounter):
            self.resettime[i] = self.counter[i].getTime()

    # delete the timers when the object is destroyed
    def __del__(self):
        counter     = []
        resettime   = []
        nCounter    = 0
