# Class to set up a text display associated with the main experiment
#
# Created:
# Nov 17: Naveed Ejaz
from psychopy import visual

class TextDisplay:
    handle = []

    # constructor
    def __init__(self, params):
        self.handle = visual.Window(params['textwin_size'], color=params['textwin_bgcolor'], pos=params['textwin_pos'], name="TextDisplay")

    # flip buffer to screen
    def flip(self):
		self.handle.flip()

	# close window
    def close(self):
		self.handle.close()
