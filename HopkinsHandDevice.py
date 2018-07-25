from GenericHardware import GenericHardware
import hid
from struct import unpack
import numpy as np
import pdb

# Main Class to communication with all the hopkins hand device
#
# Created:
# Dec 10: Naveed Ejaz

# Base class without multiprocessing
class HopkinsHandDevice(GenericHardware):
    # constructor
    def __init__(self, params):
        self.multiplier = params['multiplier']

        self.rot        = np.pi / 4.0
        self.sinrot     = np.sin(self.rot)
        self.cosrot     = np.cos(self.rot)

        self.f_baseline  = np.zeros(15)
        self.last_data   = np.zeros(15)
        self.raw_data    = np.zeros(15)
        
        # call base constructor
        GenericHardware.__init__(self,params)
        
        self.initialize()

    # implementation of virtual initialization function
    # DO NOT CALL, WILL BE CALLED IMPLICITLY
    def initialize(self):
        # make connection to hand device and calibrate zero value
        self.connect()

        self.zerof(500)
        print('Calibrating zero baseline')
 
    # make connection to hand device
    def connect(self):
        self.handle = hid.device()

        dev_path = ''
        for d in hid.enumerate():
            if d['product_id'] == 1158 and d['usage'] == 512:
                dev_path = d['path']
                print('Opened hand device')
        
        self.handle.open_path(dev_path)

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
    def getRaw(self,i):
        self.update()
        i = i*3
        return self.last_data[0+i:3+i]

    # get (X,Y) summated readings for all fingers except the i-th pair
    def getXY_RMSForces(self,i):
        self.update()
        x   = np.multiply(self.last_data,self.multiplier)
        x   = np.reshape(x,[5,3])
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
        return np.multiply(self.last_data[0+i:3+i],self.multiplier[0+i:3+i])
    
    # get all (X, Y, Z) readings for ALL fingers
    def getXYZ_ALL(self):
        self.update()
        return np.multiply(self.last_data, self.multiplier)        

    # get only (X,Y) readings for i-th finger
    def getXY(self,i):
        self.update()
        i = i * 3
        return np.multiply(self.last_data[0+i:2+i],self.multiplier[0+i:2+i])

    # zerof calibration of the device
    def zerof(self, num_samples):
        t = np.zeros([num_samples,15])
        for i in range(num_samples):
            self.update()
            t[i,:] = self.raw_data

        self.f_baseline = np.mean(t,axis=0)
    # estimate enslaving

    # this function is called every time GenericHardware multiprocessing loop is updated
    # return the data to be written to buffer
    def onUpdate(self):
        return self.getXYZ_ALL()
        
