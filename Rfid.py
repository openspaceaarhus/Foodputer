import sys

from Slice import Slice, Slice_state



class Rfid(Slice):
    
    def __init__(self):
        Slice.__init__(self, Slice_state.READY)

    def get_text(self):
        return "Enter RFID"

    @staticmethod
    def is_rfid(str):
        return str[0] == 'r'

    def handle_rfid(self, str):
        """Handle the rfid input

        based on rfid state"""

        if self.state ==  Slice_state.DONE:
            print "Please cancel current order if you want to change whos paying"
        elif self.state ==  Slice_state.READY:
            #start the "get name and token" process
            #something async would be nice
            
            #change to the new state ?
            self.state =  Slice_state.WAITING
        elif self.state == Slice_state.LOCKED:
             #beep
            sys.stdout.write("\a")
        elif self.state == Slice_state.WAITING:
             #beep
            sys.stdout.write("\a")
        else:
            print "unknown state error"
