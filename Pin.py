import sys
from Slice import Slice, Slice_state


class Pin(Slice):
    
    def __init__(self):
        Slice.__init__(self, Slice_state.LOCKED)
        self.angle += self.da
    def get_text(self):
        return "Enter pincode"

    @staticmethod
    def is_pin(str):
        return str[0] == 'p'

    def handle_pin(self, str):
        """Handle the pin input
        
        based on pin state"""

        if self.state ==  Slice_state.DONE:
            print "have a nice day .. reset erverything for next order"
        elif self.state ==  Slice_state.READY:
            #start the order process
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
