import multiprocessing

# Main Class to communication with all custom hardware used in experiment
#
# Created:
# Dec 10: Naveed Ejaz

# Class inherits from multiprocessing class so that it is able to spawn off 
# a child thread for polling at a faster interval
class HardwareManager(multiprocessing.Process):

    # constructor takes in an object defining the 
    def __init__(self):
        multiprocessing.Process.__init__(self)  # inherited multiprocess constructor
        print('Hopkins hand device opened')

    def run(self):
        while True:
            """start polling data here"""         

    def shutdown(self):
        print('Hopkins hand device closed')
        self.exit.set()        
