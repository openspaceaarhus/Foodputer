import sys
from Slice import Slice, Slice_state



class Barcode(Slice):
    
    def __init__(self):
        Slice.__init__(self, Slice_state.READY)
        self.angle += 2 * self.da

    def get_text(self):
        if (Slice_state.READY == self.state):
            return "Enter barcode"
        elif (Slice_state.LOCKED == self.state):
            return "can't change product now"
        else:
            return self.product

    @staticmethod
    def is_barcode(str):
        return str[0] == 'b'

    def handle_barcode(self, str):
        """Handle the barcode input
        based on barcode state"""
        

        if self.state ==  Slice_state.DONE:
            print "have a nice day .. reset erverything for next order"
        elif self.state ==  Slice_state.READY:
            #set or change the product
            self.product = "club mate"
            #change to the new state
            self.state =  Slice_state.DONE
        elif self.state == Slice_state.LOCKED:
             #beep
            sys.stdout.write("\a")
        elif self.state == Slice_state.WAITING:
             #beep
            print "should never wait for db access"
        else:
            print "unknown state error"
        

