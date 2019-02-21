# Experiment for hand assessment using the hopkins hand device
#
# Created:
# Nov 17: Naveed Ejaz
# 
# IMPORTANT: Path to PyPotamus needs set to be in PYTHONPATH environment variable

import numpy as np
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
            self.gHardware['gHand_R'].zerof(1000)
            self.gHardware['gHand_L'].zerof(1000)
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
        img_r         = self.gScreen.image(image="hand_r.png", pos=(0,0), units="pix")
        img_l         = self.gScreen.image(image="hand_l.png", pos=(0,0), units="pix")
        img = [img_l, img_r]

        warnings    = self.gScreen.text(text='', pos=(0,-0.15), color='black')
        boxL        = self.gScreen.rect(pos=[-0.95,0], width=0.05, height=1, lineWidth=5, 
                                        lineColor='white', fillColor='white')
        boxR        = self.gScreen.rect(pos=[0.95,0], width=0.05, height=1, lineWidth=5, 
                                        lineColor='white', fillColor='white')
        fixation    = self.gScreen.text(text='+', pos=[0,0.02], color='white', height=0.3)
        ensbarL     = self.gScreen.rect(pos=[-0.95,0], width=0.05, height=0.0, lineWidth=1, 
                                        lineColor='black', fillColor='LightPink')
        ensbarR     = self.gScreen.rect(pos=[0.95,0], width=0.05, height=0.0, lineWidth=1, 
                                        lineColor='black', fillColor='LightPink')
        text        = self.gScreen.text(text='', pos=(0,0.95), color='white')
        target      = self.gScreen.circle(pos=[0,0], radius=0.08, lineWidth=4.0, lineColor='black', 
                                          fillColor='black')
        finger      = self.gScreen.circle(pos=[0,0], radius=0.07, lineWidth=3.0, lineColor='white',
                                          fillColor='grey')
        cuefing     = self.gScreen.circle(pos=[0,0], radius=0.05, lineWidth=3.0, lineColor='white', 
                                          fillColor='blue')

        posList     = [ [(0.45,0.01),(0.21, 0.42),(-0.03,0.5),(-0.22,0.48),(-0.38,0.28)], [(-0.45,0.01),(-0.21, 0.42),(0.03,0.5),(0.22,0.48),(0.38,0.28)]]
        colorList   = ['#AFADF5', '#E3CBA0', '#DE4CBA', 'blue', 'yellow']
        
        # for sound 
        mixer.init()
        
        # set time limits for trial phases
        CUE_TIME        = 1200
        PREP_TIME       = 400
        RESP_TIME       = 6000
        RETURN_TIME     = 3000
        FINGER_REMAIN   = 250
        FAIL_TIME       = 1200
        DEAD_TIME       = 2500
        RT_THRESH       = 0.25 #in N
        MAX_FORCE       = 4 # in N

        target.opacity  = 0.0
        ensbarL.opacity = 0.0
        ensbarR.opacity = 0.0
        finger.opacity  = 0.0
        boxL.opacity    = 0.0
        boxR.opacity    = 0.0
        img_r.opacity     = 0.0
        img_l.opacity     = 0.0 
        cuefing.opacity = 0.0
        text.color      = 'black'

        #   - save objects to dictionary for easy access
        #self.gScreen['finger1']          = finger1
        self.gScreen['finger']          = finger
        self.gScreen['cuefing']         = cuefing
        self.gScreen['ensbarL']         = ensbarL
        self.gScreen['ensbarR']         = ensbarR
        self.gScreen['boxL']            = boxL
        self.gScreen['boxR']            = boxR
        self.gScreen['target']          = target
        self.gScreen['text']            = text
        self.gScreen['warnings']        = warnings
        #self.gScreen['soundlist']       = soundlist
        #self.gScreen['audio']           = audio
        self.gScreen['fixation']        = fixation 
        self.gScreen['handimage']       = img
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
        righthand =  self.gHardware['gHand_R']
        lefthand = self.gHardware['gHand_L']
        hands = {1:lefthand, 2:righthand}
        
        self.gVariables['HAND_DEVICES'] = hands

        
    # this function is called when diagnostic info is about to be updated
    def updateDiagnostic(self):        
        self.gDiagnostic[0] = 'Subj:' + self.get_subject_id()
        self.gDiagnostic[1] = 'Timer:' + str(round(self.gTimer[0],1))
        self.gDiagnostic[2] = 'Run:' + str(self.get_runno())
        self.gDiagnostic[3] = 'TN:' + str(self.gTrial.TN)        

    # this function is called when screen is about to be updated
    def updateScreen(self):     
        # get handles for fast access
        gFinger     = self.gScreen['finger']
        gEnsbarL    = self.gScreen['ensbarL']
        gEnsbarR    = self.gScreen['ensbarR']
        gTarget     = self.gScreen['target']
        gBoxL       = self.gScreen['boxL']
        gBoxR       = self.gScreen['boxR']
        gText       = self.gScreen['text']
        gDigit      = int(self.gTrial.Digit)
        gHand = int(self.gTrial.Hand)
        gInstHand   = self.gVariables['HAND_DEVICES'][gHand]
        gScaling = self.gVariables['SCALING']
        gMaxForce = self.gVariables['MAX_FORCE']
        gHandimage  = self.gScreen['handimage'][gHand-1]


        
 
        


        # update finger pos and raidus based on hardware readings during the appropriate phases
        if self.state == self.gStates.WAIT_PREPRATORY or self.gStates.WAIT_RESPONSE or self.gStates.WAIT_RELEASE: 
            
            pos             = gInstHand.getXYZ(gDigit - 1)
            if gDigit == 1:
                X = pos[0] * gScaling
                Y = pos[2] * gScaling
            else:
                X = gScaling * pos[0]
                Y = gScaling * pos[1]     
            gFinger.pos     = [X,Y]

            # update ens bars based on hardware reading
            rms         = gInstHand.getXY_RMSForces(gDigit - 1)
            ens_perc    = self.gTrial.EnsPercent
            max_rms     = np.sqrt((2 * np.square(gMaxForce)))
            rms_lim     = ens_perc * max_rms
            ens_visual  = ens_perc * (rms[0] / rms_lim)

            gEnsbarL.height = min(ens_visual, gBoxL.height)
            gEnsbarR.height = min(ens_visual, gBoxR.height)
    
    # over-load experimental trial loop function
    def trial(self):
        # get handles for fast access
        gFixation   = self.gScreen['fixation']
        gFinger     = self.gScreen['finger']
        gEnsbarL    = self.gScreen['ensbarL']
        gEnsbarR    = self.gScreen['ensbarR']
        gTarget     = self.gScreen['target']
        gBoxL       = self.gScreen['boxL']
        gBoxR       = self.gScreen['boxR']
        gText       = self.gScreen['text']
        gCueFing    = self.gScreen['cuefing']
        gPoslist    = self.gScreen['posList']
        gColorlist  = self.gScreen['colorList']
        gWarnings   = self.gScreen['warnings']
        gWarnlist   = self.gScreen['warnList']
        gDigit      = int(self.gTrial.Digit)
        gHand       = int(self.gTrial.Hand)
        gInstHand = self.gVariables['HAND_DEVICES'][gHand]
        gCueTime    = self.gVariables['CUE_TIME']
        gPrepTime   = self.gVariables['PREP_TIME']
        gRespTime   = self.gVariables['RESP_TIME']
        gReturnTime = self.gVariables['RETURN_TIME']
        gFingRemain = self.gVariables['FINGER_REMAIN']
        gFailTime   = self.gVariables['FAIL_TIME']
        gDeadTime   = self.gVariables['DEAD_TIME']
        gRTthresh   = self.gVariables['RT_THRESH']
        gBlopSound  = self.gVariables['BLOP_SOUND']
        gBuzzSound  = self.gVariables['BUZZ_SOUND']
        gScaling    = self.gVariables['SCALING']
        gHandimage  = self.gScreen['handimage'][gHand-1]


                        
        # set state for hand device
        gHand_R.setState(self.get_runno(),round(self.gTrial.TN),self.state)
        gHand_L.setState(self.get_runno(),round(self.gTrial.TN),self.state)

        # START TRIAL
        if self.state == self.gStates.START_TRIAL:          
                # set state to cue phase
                #   - log the start of the trial 
                #   - start logging data
                self.state                          = self.gStates.CUE_PHASE
                self.gVariables['measStartTime']    = self.gTimer[0]
                gHand_R.startRecording()
                gHand_L.startRecording()
                    
                

                # set target location for the trial, and hide from view 
                gTarget.opacity     = 0
                gTarget.radius      = 0.08

                self.gVariables['TargetX'] = self.gTrial.TargetX
                self.gVariables['TargetY'] = self.gTrial.TargetY
                #self.gVariables['TargetZ'] = self.gTrial.TargetZ




                gTarget.pos = (self.gVariables['TargetX'] * gScaling, self.gVariables['TargetY'] * gScaling)
                #gTarget.radius = self.gVariables['TargetZ']
                gFixation.color = 'black'
                #set up display to appear during the cue phase
        
                gText.text = self.gScreen['fingerLabels'][gDigit - 1]
                gText.color = 'white'
                gHandimage.opacity  = 0.9
                gCueFing.pos = gPoslist[gHand-1][(gDigit - 1)]
                gCueFing.fillColor   = gColorlist[gDigit - 1]
                gCueFing.opacity = 1

                #reset the internal between phase timer (gTimer1)
                self.gTimer.reset(1)
                

                self.gVariables['RT'] = 0
                self.gVariables['MT'] = 0

        # CUE PHASE
        elif self.state == self.gStates.CUE_PHASE:
            if self.gTimer[1] > gCueTime:
                # hide hand
                gHandimage.opacity                  = 0.0
                gCueFing.opacity                      = 0.0
                #display the shapes involved in the next phase
                gBoxL.opacity       = 0.4
                gBoxR.opacity       = 0.4
                gBoxL.height        = self.gTrial.EnsPercent
                gBoxR.height        = self.gTrial.EnsPercent
                gEnsbarR.opacity  = 0.5
                gEnsbarL.opacity  = 0.5
                gFinger.opacity     = 0.7
                gFinger.fillColor   = gColorlist[gDigit - 1]         
                gFixation.color     = 'white'
 
                # swtich phase and reset timer
                self.state                          = self.gStates.WAIT_PREPRATORY
                self.gTimer.reset(1)

   
        # PREPRATORY PHASE
        elif self.state == self.gStates.WAIT_PREPRATORY:
            #wait for the time period to be over
            if self.gTimer[1] > gPrepTime:
                # update what is to be shown on screen for next phase
                gFixation.color                     = 'black'
                gTarget.opacity                     = 1
                gTarget.fillColor                   = 'grey'
                gTarget.lineColor                   = 'white'

                #change phase and reset timer
                self.state                          = self.gStates.WAIT_RESPONSE
                self.gTimer.reset(1)
                #for RT and movement time
                self.gTimer.reset(2)

                                
        # WAIT_RESPONSE
        elif self.state == self.gStates.WAIT_RESPONSE:
            # calculate distance from target and keep track of the ens bars continually
            euc_dist    = np.linalg.norm(np.subtract(gFinger.pos,gTarget.pos))
            RT_dist    = np.linalg.norm(np.subtract(gFinger.pos, gFixation.pos))
            bar_height  = gEnsbarL.height
            box_height  = gBoxL.height
            #mov_dat = list(self.gHardware['gHand'].getXYZ_ALL())
            #mov_dat = mov_dat + [self.gTrial.TN] + [self.gData.run] + [self.gTimer[0]]
            #self.gVariables['MOV_DATA'].append(mov_dat)

            if (RT_dist > gRTthresh * gScaling) and (self.gVariables['RT']==0):
                self.gVariables['RT'] = self.gTimer[2]

            #if the finger reaches the target
            if euc_dist <= (1/2)*gTarget.radius:
                gBlopSound.play()
                #save data for finger forces with scalar applied and show corr trial
                pos             = gInstHand.getXYZ(gDigit - 1)
                self.gVariables['ForceX'] = pos[0]
                self.gVariables['ForceY'] = pos[1]
                self.gVariables['ForceZ'] = pos[2]
                rms = gInstHand.getXY_RMSForces(gDigit - 1)
                self.gVariables['EnsForce'] = rms[0]
                self.gVariables['Corr']     = 1
                #add raw froce data from device

                rawxyz = gInstHand.getRaw(gDigit - 1)

                #self.gHardware['gHand'].update()
                #raw = self.gHardware['gHand'].last_data
                #bb = gDigit*3 
                #aa = bb-3
                #rawxyz = raw[aa:bb]
                self.gVariables['RawX'] = rawxyz[0]
                self.gVariables['RawY'] = rawxyz[1]
                self.gVariables['RawZ'] = rawxyz[2]
                #add movement time, and change shape colours
                self.gVariables['MT'] = self.gTimer[2]
                gFinger.opacity     = 0.95
                gFixation.color = 'white'
                gFinger.fillColor   = 'green'

      

                #swtich states and reset timer1
                self.state          = self.gStates.WAIT_RELEASE
                self.gTimer.reset(1)

            # if the ens bars get to large
            if bar_height >= box_height:
                gBuzzSound.play()

                #save data for finger forces with scalar applied 
                pos             = gInstHand.getXYZ(gDigit - 1)
                self.gVariables['ForceX'] = pos[0]
                self.gVariables['ForceY'] = pos[1]
                self.gVariables['ForceZ'] = pos[2]
                rms = gInstHand.getXY_RMSForces(gDigit - 1)
                self.gVariables['EnsForce'] = rms[0]
                self.gVariables['Corr']     = 2
 
                rawxyz = gInstHand.getRaw(gDigit - 1)

                #self.gHardware['gHand'].update()
                #raw = self.gHardware['gHand'].last_data
                #bb = gDigit*3
                #aa = bb-3
                #rawxyz = raw[aa:bb]
                self.gVariables['RawX'] = rawxyz[0]
                self.gVariables['RawY'] = rawxyz[1]
                self.gVariables['RawZ'] = rawxyz[2]
                self.gVariables['MT'] = 0


                gFinger.opacity    = 0.95
                gFinger.fillColor   = 'red'
                gEnsbarL.fillColor  = 'red'
                gEnsbarR.fillColor  = 'red'
                gTarget.opacity     = 0
                self.state = self.gStates.TRIAL_FAILED
            # if the resp time is up
            if self.gTimer[1] > gRespTime:
                gBuzzSound.play()
                #save data for finger forces with scalar applied 
                pos             = gInstHand.getXYZ(gDigit - 1)
                self.gVariables['ForceX'] = pos[0]
                self.gVariables['ForceY'] = pos[1]
                self.gVariables['ForceZ'] = pos[2]
                rms = gInstHand.getXY_RMSForces(gDigit - 1)
                self.gVariables['EnsForce'] = rms[0]
                self.gVariables['Corr']     = 3
 
                rawxyz = gInstHand.getRaw(gDigit - 1)

                #self.gHardware['gHand'].update()
                #raw = self.gHardware['gHand'].last_data
                #bb = gDigit*3 
                #aa = bb-3
                #rawxyz = raw[aa:bb]
                self.gVariables['RawX'] = rawxyz[0]
                self.gVariables['RawY'] = rawxyz[1]
                self.gVariables['RawZ'] = rawxyz[2]

                self.gVariables['MT'] = 0

                gFinger.opacity     = 0.95
                gFinger.fillColor   = 'red'
                gTarget.opacity     = 0
                self.state          = self.gStates.TRIAL_FAILED
            #checks if we have trigged a failed trial
            if self.state == self.gStates.TRIAL_FAILED:
                #if so, what is the reason, and display the appropriate text, and hide the appropriate shapes (and resetting timer)
                if gEnsbarL.fillColor == 'red':
                    gFinger.opacity = 0
                    gWarnings.text = gWarnlist[0]
                    gWarnings.color = 'white'
                    self.gTimer.reset(1)

                else:
                    gFinger.opacity = 0
                    gWarnings.text = gWarnlist[1]
                    gWarnings.color = 'white'
                    gFinger.opacity = 0
                    gTarget.opacity = 0
                    self.gTimer.reset(1)

        # WAIT_RELEASE
        elif self.state == self.gStates.WAIT_RELEASE:
            #calculate euclidian distance from finger to fixation cross continually
            euc_dist = np.linalg.norm(np.subtract(gFinger.pos,gFixation.pos))
            gTarget.radius += 0.02
            gTarget.opacity -= 0.05
            #check to see if the finger has returned to the cross, and locks finger position 
            if (euc_dist <= 0.05):  
                pos = gInstHand.getXY(gDigit - 1)
                gTarget.opacity = 0
                gTarget.radius = 0.08
                
                self.state                          = self.gStates.TRIAL_COMPLETE
                self.gVariables['measEndTime']      = self.gTimer[0]
                self.gTimer.reset(1)
                gWarnings.text = gWarnlist[2] 
                gWarnings.color = 'white'

              
                


            # if the time for the phase is over, hide finger and move to next
            if (self.gTimer[1] > gReturnTime):
                gFinger.opacity = 0
                gFixation.color = 'black'
                self.state                          = self.gStates.TRIAL_COMPLETE
                self.gVariables['measEndTime']      = self.gTimer[0]
                self.gTimer.reset(1)
                gWarnings.text = gWarnlist[2] 
                gWarnings.color = 'white'

                
                


        # TRIAL_FAILED
        elif self.state == self.gStates.TRIAL_FAILED:
            #swtiches state, logs end of the trial time and resests internal timer
            if (self.gTimer[1] > gFailTime): 
                gEnsbarL.fillColor = 'LightPink'
                gEnsbarR.fillColor = 'LightPink'
                gWarnings.text = gWarnlist[2] 

                self.state = self.gStates.TRIAL_COMPLETE
                self.gVariables['measEndTime']      = self.gTimer[0]
                self.gTimer.reset(1)





        # TRIAL_COMPLETE
        elif self.state == self.gStates.TRIAL_COMPLETE:
            if (self.gTimer[1] > gFingRemain):
                self.gHardware['gHand_L'].zerof(500)
                self.gHardware['gHand_R'].zerof(500)
                gFinger.opacity = 0
                gFixation.color = 'black'

            #waits for between trial time to elapse, before ending trial
            if (self.gTimer[1] > gDeadTime):
                self.state          = self.gStates.END_TRIAL
                gWarnings.text = ''
                gHand_R.stopRecording()
                gHand_L.stopRecording()



    # adding trial data on trial end
    def onTrialEnd(self):
        # get data from hand device hardware thread and write to mov file
        m_r = gHand_R.getBufferAsArray()
        m_l = gHand_L.getBufferAsArray()

        rows_max = max([int(m_r.size/19), int(m_l.size/19)])
        rows_min = min([int(m_r.size/19), int(m_l.size/19)])
        rows = rows_max - rows_min
        filler = np.full([rows, 19], np.nan)

        idx = [int(m_r.size/19), int(m_l.size/19)].index(rows_min)
        if idx == 0:
            m_r = np.vstack((m_r, filler))
        else:
            m_l = np.vstack((m_l, filler))

        m = np.concatenate((m_l,m_r), axis = 1)
        self.gData.add_mov_record_array(m) # * check for arrays to do this.

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
        self.gData.add_data_record([gTrial.TN, gDat.run, gTrial.Hand, gTrial.Digit, gVar['Corr'],
                                    gVar['TargetX'], gVar['TargetY'],gTrial.EnsPercent, 
                                    gVar['RawX'], gVar['RawY'], gVar['RawZ'], 
                                    gVar['ForceX'], gVar['ForceY'], gVar['ForceZ'], 
                                    gVar['RT'], gVar['MT'], gVar['EnsForce'], 
                                    gVar['measStartTime'], gVar['measEndTime']])
        # self.gData.add_mov_record(gVar['MOV_DATA'])
        self.gVariables['MOV_DATA'] = []
        # pdb.set_trace()

    # adding data on run end
    def onRunEnd(self):
        print('Run complete')
        print('Score : '+ str(np.sum(self.gData.data['Corr']==1)) )
        print('Passive Finger Movement: '+ str(np.mean(self.gData.data['EnsForce'])) )
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
    gExp.set_trial_states('START_TRIAL', 'CUE_PHASE', 'WAIT_PREPRATORY', 'WAIT_RESPONSE','WAIT_RELEASE',
                          'TRIAL_FAILED', 'TRIAL_COMPLETE','END_TRIAL')
    # initialize hopkins hand device (right handed) and add it to the hardware manager
    opt_R     = gExp.gParams['right_hand']
    gHand_R   = HopkinsHandDevice(opt_R)
    gExp.add_hardware('gHand_R',gHand_R)
    opt_L     = gExp.gParams['left_hand']
    gHand_L   = HopkinsHandDevice(opt_L)
    gExp.add_hardware('gHand_L',gHand_L)

    # hand over control to the game loop
    print('I am in : ' + gHand_R.processName() + ' and ' + gHand_L.processName())
    gExp.control()
    gHand_R.terminate()
    gHand_L.terminate()
