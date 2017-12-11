# Main Keyboard Class
#
# Created:
# Dec 9: Naveed Ejaz

class Keyboard:
    # function handler for specifying subject id
    def subj(self, input_list):
        return ['subj', input_list[0]]

    # function handler for specifying run number and target file
    def run(self, input_list):
        # input 1 is the run number
        # input 2 is the target file name
        return ['run', int(input_list[0]), input_list[1]]

    # function handler for quiting program 
    def quit(self, input_list):
        return ['quit']

    # function handler for unrecognized keyboard input
    def error(self):
        print 'unexpected command'
        return ['error']

    # constructor
    def __init__(self, params):
        """Constructor purposely left empty"""

    # poll keyboard and get user input
    def poll(self, subject_id):
        commandStr = raw_input(subject_id + ">> ")
        splitstr   = commandStr.split(' ')

        out = ['return']
        if splitstr[0] != '':
            try:
                out = eval('self.' + splitstr[0] + '(splitstr[1:])')
            except:
                out = self.error()

        return out    

