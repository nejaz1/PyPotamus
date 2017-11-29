# Class to set up a visual display associated with the main experiment
#
# Created:
# Nov 17: Naveed Ejaz
from psychopy import visual
from operator import add

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
    def grating(self, **kwargs):
        vis = visual.GratingStim(self.handle, **kwargs)
        vis.setAutoDraw(self.autodraw)
        vis.autoLog = self.autoLog
        return vis

    # draw a circle
    def circle(self, **kwargs):
        vis = visual.Circle(self.handle, **kwargs)
        vis.setAutoDraw(self.autodraw)
        vis.autoLog = self.autoLog
        return vis

    # draw a line
    def line(self, **kwargs):
        vis = visual.Line(self.handle, **kwargs)
        vis.setAutoDraw(self.autodraw)
        vis.autoLog = self.autoLog
        return vis        

    # draw a rectangle
    def rect(self, **kwargs):
        vis = visual.Rect(self.handle, **kwargs)
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

