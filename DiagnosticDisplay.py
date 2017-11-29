# Class to set up a diagnostic display associated with the main experiment
#
# Created:
# Nov 17: Naveed Ejaz
from psychopy import visual

class DiagnosticDisplay:
    handle      = []
    autodraw    = []
    txt         = []

    # constructor
    def __init__(self, params):
        self.handle     = []
        self.autodraw   = params['diagnosticwin_autodraw']
        self.numlines   = 5
        self.pos        = [[0,0.6], [0,0.3], [0,0], [0,-0.3], [0,-0.6]]
        self.txt        = list()

    # turn diagnostic window on/off
    def diagnostic(self, mode, params):
        if mode == 'on':
            if self.handle == []:
                self.handle = visual.Window(params['diagnosticwin_size'], color=params['diagnosticwin_bgcolor'], pos=params['diagnosticwin_pos'], name="DiagnosticDisplay")
                self.init_lines()
        elif mode == 'off':
            self.close()

    # write text to diagnostic
    def init_lines(self,**kwargs):
        for i in range(self.numlines):
            t = visual.TextStim(self.handle, text='', height=0.2, alignHoriz='center', alignVert='top', color='black', pos=self.pos[i])
            t.setAutoDraw(self.autodraw)
            self.txt.append(t)

    # sets the current line to the diagnostic text
    def __setitem__(self, key, item):
        self.txt[key].setText(item)

    # sets the current line to the diagnostic text
    def __getitem__(self, key):
        return self.txt[key]

    # flip buffer to screen
    def flip(self):
        if self.handle != []:
            self.handle.flip()

	# close window
    def close(self):
        if self.handle != []:
            self.handle.close()
            self.handle = []
