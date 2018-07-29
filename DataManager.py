# Class to manage and export to disk data recorded during experiment
#
# Created:
# Nov 20: Naveed Ejaz
import pandas as pd
import numpy as np
import pdb
from datetime import datetime
import os
import pdb

# Class to manage data generated during experiment
class DataManager:
    sep             = '\t'
    subject_id      = ''
    nowtime         = ''
    fname           = []    # file name to save data to
    dbg_fname       = []    # file name to save debug data to
    mov_fname       = []

    data_dir        = ''    # directory where data will be stored
    data            = []    # experimental data in pandas format
    mov_data        = []    # raw time course data for the trial
    dbg_data        = []    # debug data for experiment

    BN              = 0     # block number
    TN              = 0     # trial number

    # constructor
    def __init__(self, params):
        self.update_date_string()
        self.subject_id = ''
        self.update_file_names()

        self.mov_nrows = 2000000 

        # setup data directory
        self.set_data_directory(params['data_dir'])

    # run this whenever subject name gets updated
    def update_file_names(self):
        if self.subject_id == '':
            self.fname      = '_.txt'
            self.dbg_fname  = '_debug.txt'
            self.mov_fname = '_.mov'
        else:
            self.fname      = self.subject_id + '.txt'
            self.dbg_fname  = self.subject_id + '_debug.txt'
            self.mov_fname  = self.subject_id + '.mov'                

    # set data directory
    def set_data_directory(self, data_dir_path):
        self.data_dir = os.path.dirname(data_dir_path)
        self.check_data_directory()
        print('Data directory is {}'.format(self.data_dir))

    # run this to make data directory if it does not exist
    def check_data_directory(self):
        if not os.path.exists(self.data_dir):
            print('Making data directory: ' + self.data_dir)
            os.makedirs(self.data_dir)

    # get date string
    def update_date_string(self):
        self.nowtime = datetime.now().strftime("%B %d, %Y at %I:%M%p")

    # set subject id (used as file name to save data to disk)
    def set_subject_id(self, subject_id):
        self.subject_id     = subject_id
        self.update_file_names()

    # add event to debug data store
    def add_dbg_event(self, event):
        self.update_date_string()
        self.dbg_data.loc[len(self.dbg_data)] = [self.nowtime, self.subject_id, event]

    # add experimental data record to data store
    def add_data_record(self, values):
        self.data.loc[len(self.data)] = values

    def add_mov_record(self, data):
        for row in data:
            self.mov_data.loc[len(self.mov_data)] = row

    def add_mov_record_array(self, data):
        (nrows,ncols) = data.shape

        self.mov_data[self.mov_idx:self.mov_idx + nrows] = data
        self.mov_idx = self.mov_idx + nrows
        # pdb.set_trace()
        # for row in data:
        #     self.mov_data.loc[len(self.mov_data)] = row

    # what is the data, and in which order should datamanager expect it
    def init_data_manager(self, dataformat):
        # initialize experimental data  
        self.summary_dataformat = dataformat
        self.data       = pd.DataFrame(columns=dataformat)
        self.dbg_data   = pd.DataFrame(columns=['time_stamp','subject_id','event'])
        # add debug event
        self.add_dbg_event('init')

    def init_mov_manager(self, dataformat):
        self.trial_dataformat = dataformat
        self.mov_ncols  = len(dataformat)
        # self.mov_data   = pd.DataFrame(columns=dataformat)

        self.mov_data   = np.array([0.0] * self.mov_nrows * self.mov_ncols).reshape(self.mov_nrows,self.mov_ncols)
        self.mov_idx    = 0

    # write debug data to file
    def write_dbg_data(self):
        dbg_fname = os.path.join(self.data_dir,self.dbg_fname)
        self.dbg_data.to_csv(dbg_fname, sep='\t', index=False)

    # write data to file
    # this should be done at the end of the block
    def write_data(self):
        data_fname = os.path.join(self.data_dir,self.fname)
        self.data.to_csv(data_fname, sep='\t', index=False)
           
        mov_dat = os.path.join(self.data_dir, self.mov_fname)
        d = pd.DataFrame(self.mov_data[0:self.mov_idx], columns=self.trial_dataformat)
        d.to_csv(mov_dat, sep='\t', index=False)
        # self.mov_data.to_csv(mov_dat, sep='\t', index=False)    
