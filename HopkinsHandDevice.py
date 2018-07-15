import multiprocessing
import hid
from struct import unpack
import numpy as np
import pdb

# Main Class to communication with all the hopkins hand device
#
# Created:
# Dec 10: Naveed Ejaz

# Class inherits from multiprocessing class so that it is able to spawn off 
# a child thread for polling at a faster interval
class HopkinsHandDeviceMultiproc(multiprocessing.Process):

    # constructor spawns of multiprocessing thread
    def __init__(self, params):
        multiprocessing.Process.__init__(self)  # inherited multiprocess constructor
        print('Opening thread...')        
        self.initialize()

    # initialize connection to hand device
    def initialize(self):
        self.handle = hid.device()
        self.handle.open(0x16c0, 0x486)
        self.handle.set_nonblocking(1)
        print('Opened hand device')

    # get readings from hand device
    def run(self):
        print('Thread running...')
        self.handle.write([0]*64)

        while True:
            d = bytearray(self.handle.read(46))
            if d:
                x = unpack('>LhHHHHHHHHHHHHHHHHHHHH', d)
                print(x)

    # shutdown thread
    def shutdown(self):
        print('Exiting thread')
        self.handle.close()
        self.exit.set()        

# Base class without multiprocessing
class HopkinsHandDevice:

    # constructor spawns of multiprocessing thread
    def __init__(self):
        self.initialize()
       

        self.multiplier = (1,1,1)

        self.rot        = np.pi / 4.0
        self.sinrot     = np.sin(self.rot)
        self.cosrot     = np.cos(self.rot)

        self.f_baseline  = np.zeros(15)
        self.last_data   = np.zeros(15)
        self.raw_data    = np.zeros(15)

        self.zerof(500)
        print('Calibrating zero baseline')

    # initialize connection to hand device
    def initialize(self):
        self.handle = hid.device()

        dev_path = ''
        for d in hid.enumerate():
            if d['product_id'] == 1158 and d['usage'] == 512:
                dev_path = d['path']
                print('Opened hand device')
        self.handle.open_path(dev_path)

    # initialize connection to hand device (this sometimes doesn't work)
    def initialize_alternative(self):
        self.handle = hid.device()
        self.handle.open(0x16c0, 0x486)
        self.handle.set_nonblocking(1)

        self.handle.write([0] * 64)
        print('Opened hand device')

    # set force baseline
    def set_force_baseline(self, fBaseline):
        self.f_baseline = fBaseline

    # set force multiplier
    def set_force_multiplier(self, mult):
        self.multiplier = mult        

    # update internal readings from hand device
    def update(self):
        d = self.handle.read(46)
        if d:
            d = unpack('>LhHHHHHHHHHHHHHHHHHHHH', bytearray(d))
            d = np.array(d, dtype='d')

            d[0]    /= 1000.0
            d[2:]   /= 65535.0

            self.raw_data[0::3] = d[2::4] * self.cosrot - d[3::4] * self.sinrot    # x
            self.raw_data[1::3] = d[2::4] * self.sinrot + d[3::4] * self.cosrot    # y
            self.raw_data[2::3] = d[4::4] + d[5::4]                                # z
     
            self.last_data = self.raw_data - self.f_baseline

    # get all readings from hand device
    def getRaw(self):
        self.update()
        return self.raw_data

    # get (X,Y) summated readings for all fingers except the i-th pair
    def getXY_RMSForces(self,i):
        self.update()
        x   = np.reshape(self.last_data,[5,3])
        x   = np.multiply(x,self.multiplier)
        x   = x[:,0:2]

        fin_i   = np.square(x[i,:]).sum()
        fin_all = np.square(x).sum()
        rms     = np.sqrt(fin_all-fin_i)
        rms_all = np.sqrt(fin_all)

        return rms, rms_all

    # get all (X,Y,Z) readings for i-th finger
    def getXYZ(self,i):
        self.update()
        i = i * 3
        return np.multiply(self.last_data[0+i:3+i],self.multiplier)
    
    # get all (X, Y, Z) readings for ALL fingers
    def getXYZ_ALL(self):
        self.update()
        mult = self.multiplier * 5
        return np.multiply(self.last_data, mult)        

    # get only (X,Y) readings for i-th finger
    def getXY(self,i):
        self.update()
        i = i * 3
        return np.multiply(self.last_data[0+i:2+i],self.multiplier[0:2])
    

    # zerof calibration of the device
    def zerof(self, num_samples):
        t = np.zeros([num_samples,15])
        for i in range(num_samples):
            t[i,:] = self.getRaw()

        self.f_baseline = np.mean(t,axis=0)
    # estimate enslaving