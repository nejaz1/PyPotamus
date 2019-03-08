# Experiment for hand assessment using the hopkins hand device
#
# Created:
# Nov 17: Naveed Ejaz
# 
# IMPORTANT: Path to PyPotamus needs set to be in PYTHONPATH environment variable

import numpy as np
from scipy import linalg as la
import pandas as pd
from HopkinsHandDevice import HopkinsHandDevice
from PyPotamus import Experiment
from pygame import mixer

import pdb
import multiprocessing as mp

# ------------------------------------------------------------------------
# 1. Inherited Experiment class in PyPotamus module
class myExperiment(Experiment):
    # define user commands
    def define_command(self, cmd):
        if cmd == 'zerof':
            self.gHardware['gHand'].zerof(1000)
        else:
            print('unrecognized command')

    # quicker to pre-allocate drawing elements on the screen
    def initialize(self):
        # pre-allocate graphics for
        #   - fixation cross
        #   - text indicator for which finger to press
        #   - draw circles for moving fingers and target stimulus
        #   - draw rectangles for strength of enslaving
        # e  = self.gScreen.circle(pos=[0,0], radius=1, lineColor='black', fillColor='gray')
        warnings    = self.gScreen.text(text='', pos=(0,0.2), color='black')
        dim_box        = self.gScreen.rect(pos=[0,-0.8], width=1, height=0.05, lineWidth=5, 
                                        lineColor='white', fillColor='white')
        dim_bar        = self.gScreen.rect(pos=[0,-0.8], width=0, height=0.05, lineWidth=5, 
                                        lineColor='white', fillColor='yellow')
        fixation    = self.gScreen.text(text='+', pos=[0,0.02], color='white', height=0.3)
        text        = self.gScreen.text(text='', pos=(0,0.95), color='white')
        finger1 = self.gScreen.circle(pos=[-0.4,0],radius = 0.08, lineWidth = 3.0, lineColor = 'white', fillColor = '#AFADF5')
        finger2 = self.gScreen.circle(pos=[-0.2,0],radius = 0.08, lineWidth = 3.0, lineColor = 'white', fillColor = '#E3CBA0')
        finger3 = self.gScreen.circle(pos=[0,0],radius = 0.08, lineWidth = 3.0, lineColor = 'white', fillColor = '#DE4CBA')
        finger4 = self.gScreen.circle(pos=[0.2,0],radius = 0.08, lineWidth = 3.0, lineColor = 'white', fillColor = 'blue')
        finger5 = self.gScreen.circle(pos=[0.4,0],radius = 0.08, lineWidth = 3.0, lineColor = 'white', fillColor = 'yellow')

        posList     = [(-0.45,0.01),(-0.21, 0.42),(0.03,0.5),(0.22,0.48),(0.38,0.28)]
        colorList   = ['#AFADF5', '#E3CBA0', '#DE4CBA', 'blue', 'yellow']
        timebox = self.gScreen.rect(pos=[0,-1], width = 2, height = 4, lineWidth = 5, lineColor = 'white', fillColor = 'white')
        dim_matrix = np.zeros([10,10])
        dim_num = 0
        # for sound 
        mixer.init()
        
        # set time limits for trial phases
        CUE_TIME        = 1200
        PREP_TIME       = 400
        RESP_TIME       = 30000
        RETURN_TIME     = 3000
        FINGER_REMAIN   = 400
        FAIL_TIME       = 1200
        DEAD_TIME       = 2000
        RT_THRESH       = 0.25 #in N
        MAX_FORCE       = 4 # in N

        dim_box.opacity = 0.7
        dim_bar.opacity = 0.8
        timebox.opacity = 0.3
        text.color      = 'black'

        #   - save objects to dictionary for easy access
        self.gScreen['finger1']          = finger1 
        self.gScreen['finger2']          = finger2
        self.gScreen['finger3']          = finger3
        self.gScreen['finger4']          = finger4
        self.gScreen['finger5']          = finger5
        self.gScreen['time_box']        = timebox
        self.gScreen['dim_box']            = dim_box
        self.gScreen['dim_bar']            = dim_bar
        self.gScreen['text']            = text
        self.gScreen['warnings']        = warnings
        #self.gScreen['soundlist']       = soundlist
        #self.gScreen['audio']           = audio
        self.gScreen['fixation']        = fixation 
        self.gScreen['posList']         = posList
        self.gScreen['colorList']       = colorList
        self.gScreen['warnList']        = ['Too much movement!', "Time's up!", 'Relax Fingers...']
        self.gScreen['fingerLabels']    = ['THUMB','INDEX','MIDDLE','RING','LITTLE']

        self.gVariables['CUE_TIME']         = CUE_TIME
        self.gVariables['PREP_TIME']        = PREP_TIME
        self.gVariables['RESP_TIME']        = RESP_TIME
        self.gVariables['RETURN_TIME']      = RETURN_TIME
        self.gVariables['FINGER_REMAIN']    = FINGER_REMAIN
        self.gVariables['FAIL_TIME']        = FAIL_TIME
        self.gVariables['DEAD_TIME']        = DEAD_TIME
        self.gVariables['RT_THRESH']        = RT_THRESH
        self.gVariables['MOV_DATA']         = []
        self.gVariables['BLOP_SOUND']       = mixer.Sound('BLOP.wav')
        self.gVariables['BUZZ_SOUND']       = mixer.Sound('BUZZ.wav')
        self.gVariables['SCALING']  = (self.gParams['screen_scaling'][0]/self.gParams['screen_scaling'][1])
        self.gVariables['MAX_FORCE']        = MAX_FORCE

        self.gVariables['DIM_MATRIX'] = dim_matrix
        self.gVariables['DIM_NUMBER'] = dim_num

    # this function is called when diagnostic info is about to be updated
    def updateDiagnostic(self):        
        self.gDiagnostic[0] = 'Subj:' + self.get_subject_id()
        self.gDiagnostic[1] = 'Timer:' + str(round(self.gTimer[0],1))
        self.gDiagnostic[2] = 'Run:' + str(self.get_runno())
        self.gDiagnostic[3] = 'TN:' + str(self.gTrial.TN)        

    def updateDIM(self):
        e_vals,e_vecs = la.eig(self.gVariables['DIM_MATRIX'])
        top = np.square(np.sum(e_vals))
        bottom = np.sum(np.square(e_vals))
        if bottom != 0:
            dim = top/bottom
            self.gVariables['DIM_NUMBER'] = dim
    # this function is called when screen is about to be updated
    def updateScreen(self):     
        # get handles for fast access
        gFinger1     = self.gScreen['finger1']
        gFinger2     = self.gScreen['finger2']
        gFinger3     = self.gScreen['finger3']
        gFinger4     = self.gScreen['finger4']
        gFinger5     = self.gScreen['finger5']
        gDimBar     = self.gScreen['dim_bar']
        gDimBox     = self.gScreen['dim_box']
        gText       = self.gScreen['text']
        gScaling = self.gVariables['SCALING']
        gMaxForce = self.gVariables['MAX_FORCE']
        gTimeBox = self.gScreen['time_box']

        gRespTime = self.gVariables['RESP_TIME']

        # update finger pos and raidus based on hardware readings during the appropriate phases
        # #    # pos1             = self.gHardware['gHand'].getXYZ(0)
        # #     #gFinger1.pos     = [(pos1[0] - 0.4), (pos1[1])]
        # #     #gFinger1.radius  = 0.07 + pos1[2]/1.5

        # #     pos2             = self.gHardware['gHand'].getXYZ(1)
        #     gFinger2.pos     = [(pos2[0] - 0.2), (pos2[1])]
        #     gFinger2.radius  = 0.07 + pos2[2]/1.5

        #     pos3             = self.gHardware['gHand'].getXYZ(2)
        #     gFinger3.pos     = [pos3[0], pos3[1]]
        #     gFinger3.radius  = 0.07 + pos3[2]/1.5

        #     pos4             = self.gHardware['gHand'].getXYZ(3)
        #     gFinger4.pos     = [(pos4[0]+0.2), (pos4[1])]
        #     gFinger4.radius  = 0.07 + pos4[2]/1.5

        #     pos5             = self.gHardware['gHand'].getXYZ(4)
        #     gFinger5.pos     = [(pos5[0]+0.4), (pos5[1])]
        #     gFinger5.radius  = 0.07 + pos5[2]/1.5
           
        gDimBar.width = self.gVariables['DIM_NUMBER']/10
        if self.state == self.gStates.WAIT_RESPONSE:
            gTimeBox.height = (gRespTime - self.gTimer[1])*(4/gRespTime)

            
        # dcfrvgtbhynjmk,
    
    # over-load experimental trial loop function
    def trial(self):
        # get handles for fast access
        gFinger1     = self.gScreen['finger1']
        gFinger2     = self.gScreen['finger2']
        gFinger3     = self.gScreen['finger3']
        gFinger4     = self.gScreen['finger4']
        gFinger5     = self.gScreen['finger5']
        gFixation    = self.gScreen['fixation']
        gDimBar      = self.gScreen['dim_bar']
        gDimBox      = self.gScreen['dim_box']
        gText        = self.gScreen['text']
        gPoslist     = self.gScreen['posList']
        gColorlist   = self.gScreen['colorList']
        gWarnings    = self.gScreen['warnings']
        gWarnlist    = self.gScreen['warnList']
        gCueTime     = self.gVariables['CUE_TIME']
        gPrepTime    = self.gVariables['PREP_TIME']
        gRespTime    = self.gVariables['RESP_TIME']
        gReturnTime  = self.gVariables['RETURN_TIME']
        gFingRemain  = self.gVariables['FINGER_REMAIN']
        gFailTime    = self.gVariables['FAIL_TIME']
        gDeadTime    = self.gVariables['DEAD_TIME']
        gRTthresh    = self.gVariables['RT_THRESH']
        gBlopSound   = self.gVariables['BLOP_SOUND']
        gBuzzSound   = self.gVariables['BUZZ_SOUND']
        gScaling     = self.gVariables['SCALING']
        gDimMatrix   = self.gVariables['DIM_MATRIX']

                        
        # set state for hand device
        gHand.setState(self.get_runno(),round(self.gTrial.TN),self.state)

        # START TRIAL
        if self.state == self.gStates.START_TRIAL:          
                # set state to cue phase
                #   - log the start of the trial 
                #   - start logging data
                self.state                          = self.gStates.CUE_PHASE
                self.gVariables['measStartTime']    = self.gTimer[0]
                gHand.startRecording()

                # set target location for the trial, and hide from view 


                #gTarget.radius = self.gVariables['TargetZ']
                gFixation.color = 'black'
                #set up display to appear during the cue phase
        
                gWarnings.color = 'white' #*****change text
                gDimBar.opacity = 0.9
                gDimBox.opcaity = 0.8
                gFinger1.opacity   = 0
                gFinger2.opacity = 0       
                gFinger3.opacity = 0       
                gFinger4.opacity = 0       
                gFinger5.opacity = 0       

         

                #reset the internal between phase timer (gTimer1)
                self.gTimer.reset(1)
                self.gTimer.reset(2)
                

                self.gVariables['RT'] = 0
                self.gVariables['MT'] = 0
                self.gVariables['DIM_MATRIX']= np.zeros([10,10])
                self.gVariables['DIM_NUMBER'] = 0

        # CUE PHASE
        elif self.state == self.gStates.CUE_PHASE:
            if self.gTimer[1] > 500 and self.gTimer[1] < 550:
                gWarnings.text = '3'
                self.gTimer.reset(2)
            
            if self.gTimer[2] > 1000 and self.gTimer[2] < 2000:
                gWarnings.text = '2'
            if self.gTimer[2] > 2000: 
                gWarnings.text = '1'
            if self.gTimer[2] > 3000:
                gWarnings.text = "WIGGLE!"
                # hide hand
                #display the shapes involved in the next phase
                gFinger1.opacity     = 0
                gFinger2.opacity     = 0
                gFinger3.opacity     = 0
                gFinger4.opacity     = 0
                gFinger5.opacity     = 0
 
                # swtich phase and reset timer
                self.state                          = self.gStates.WAIT_RESPONSE
                self.gTimer.reset(1)


                                
        # WAIT_RESPONSE
        elif self.state == self.gStates.WAIT_RESPONSE:
            # calculate distance from target and keep track of the ens bars continually
            a = gHand.getBufferAsArrayLAST()
            cov = np.matmul(np.transpose(a),a)
            self.gVariables['DIM_MATRIX'] = self.gVariables['DIM_MATRIX'] + cov
            self.updateDIM()

            if self.gTimer[1] > gRespTime:
                self.state = self.gStates.TRIAL_COMPLETE
                gWarnings.text = 'COMPLETE!'

        # TRIAL_COMPLETE
        elif self.state == self.gStates.TRIAL_COMPLETE:
            if (self.gTimer[1] > gFingRemain):
                gFixation.color = 'black'

            #waits for between trial time to elapse, before ending trial
            if (self.gTimer[1] > gDeadTime):
                self.state          = self.gStates.END_TRIAL
                gWarnings.text = ''
                self.gVariables['measEndTime'] = self.gTimer[0]
                gHand.stopRecording()


    # adding trial data on trial end
    def onTrialEnd(self):
        # get data from hand device hardware thread and write to mov file
        m = gHand.getBufferAsArray()
        self.gData.add_mov_record_array(m)
        m = m[:,4:]
        a = np.matmul(np.transpose(m), m)
        e_vals,e_vecs = la.eig(a)
        top = np.square(np.sum(e_vals))
        bottom = np.sum(np.square(e_vals))
        dim = top/bottom
        print('full matrix')
        print(dim)

        print('no zs')
        print(self.gVariables['DIM_NUMBER'])


      

        # print sampling stats
        # m = gHand.getBufferAsDataFrame()
        # x = pd.DataFrame(np.diff(m[0]))
        # xmean   = x.mean()[0].round(2)
        # xstd    = x.std()[0].round(2)
        # print('Sampling resolution for trial is: {} pm {} ms'.format(xmean,xstd))

        # log data to file
        gTrial  = self.gTrial
        gVar    = self.gVariables
        gDat    = self.gData
        self.gData.add_data_record([gTrial.TN, gTrial.Hand, 
                                    gVar['measStartTime'], gVar['measEndTime']])
        # self.gData.add_mov_record(gVar['MOV_DATA'])
    
        self.gVariables['MOV_DATA'] = []
        # pdb.set_trace()

    # adding data on run end
    def onRunEnd(self):
        print('Run complete')
        # pd.DataFrame(self.gData.mov_data[0:self.gData.mov_idx], columns=self.gParams['data_format']['trial']).to_csv('s01_mov.txt')
        # pdb.set_trace()


# -------------------------------------------------------------------------
# 3. Main entry point of program
if __name__ == "__main__": 

    # 1. Set up experiment and initalize using default parameters in yaml file
    #   - all options are now available in the dictionary gExp.gParams 
    gExp = myExperiment()
    gExp.load_settings('finger_task.yaml')

    # setup experiment data formats
    #   - data_format sets format of data in .dat summary file
    #   - mov_format sets format of data in .mov file
    opt = gExp.gParams['data_format']
    gExp.set_summary_data_format(opt['summary'])
    gExp.set_trial_data_format(opt['trial'])

    # initialize trial states experiment cycles over
    gExp.set_trial_states('START_TRIAL', 'CUE_PHASE', 'WAIT_RESPONSE','TRIAL_COMPLETE','END_TRIAL')

    # initialize hopkins hand device (right handed) and add it to the hardware manager
    opt     = gExp.gParams['right_hand']
    gHand   = HopkinsHandDevice(opt)
    gExp.add_hardware('gHand',gHand)

    # hand over control to the game loop
    print('I am in : ' + gHand.processName())
    gExp.control()
    gHand.terminate()
