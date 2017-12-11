import multiprocessing

# Main Class to communication with Hopkins hand device
#
# Created:
# Dec 10: Naveed Ejaz

class HopkinsHandDevice(multiprocessing.Process):

    # constructor
    def __init__(self):
        multiprocessing.Process.__init__(self)  # inherited multiprocess constructor
        print 'Hopkins hand device opened'

    def run(self):
        while True:
            """start polling data here"""         
        
    def shutdown(self):
        print 'Hopkins hand device closed'
        self.exit.set()        
