import sys
from Slice import Slice, Slice_state
from threading import Thread
import urllib2


class id_fetcher(Thread):
#    URL = 'https://hal.osaa.dk/food'
    URL = 'http://localhost:8080'

    
    def __init__(self, rfid):
        Thread.__init__(self)
        self.rfid = rfid

    def run(self):
        data = ""
        try:
            resp = urllib2.urlopen("{}/{}".format(self.URL, self.rfid.nr))
            data = resp.read()
        except urllib2.URLError, e:
            print e.reason

        self.rfid.handle_hal(data)


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
            self.nr = str
            t = id_fetcher(self)
            t.start()
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
            
    def handle_hal(self, data):
        self.state = Slice_state.DONE
        print data
