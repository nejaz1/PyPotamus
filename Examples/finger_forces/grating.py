from psychopy import visual, core

#setup stimulus
win=visual.Window([400,400])
gabor = visual.GratingStim(win, tex='sin', mask='gauss', sf=5, name='gabor')
gabor.setAutoDraw(True)  # automatically draw every frame
gabor.autoLog=False#or we'll get many messages about phase change

clock = core.Clock()
#let's draw a stimulus for 2s, drifting for middle 0.5s
while clock.getTime() < 10.0:  # clock times are in seconds
    if 0.5 <= clock.getTime() < 9.5:
        gabor.setPhase(0.1, '+')  # increment by 10th of cycle
    win.flip()

    