# Class to set up a visual display associated with the main experiment
#
# Created:
# Nov 17: Naveed Ejaz
from psychopy import visual

class ExperimentDisplay:
    handle      = []
    autodraw    = []
    autoLog     = []

    # constructor
    def __init__(self, params):
        self.handle     = visual.Window(params['expwin_size'], color=params['expwin_bgcolor'], pos=params['expwin_pos'], fullscr=params['expwin_fullscreen'], name="ExperimentDisplay")
        self.autodraw   = params['expwin_autodraw']
        self.autoLog    = params['expwin_autolog']

    # draw a grating stimulus
    def grating(self, tex, mask, sf, name):
        vis = visual.GratingStim(self.handle, tex=tex, mask=mask, sf=sf, name=name)
        vis.setAutoDraw(self.autodraw)
        vis.autoLog = self.autoLog
        return vis

    # flip buffer to screen
    def flip(self):
		self.handle.flip()

	# close window
    def close(self):
        if self.handle != []:
            self.handle.close()
            self.handle = []

