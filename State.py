from threading import Thread
import time
import urllib2



tracing = 1
def trace(str):
    if tracing:
        print str


class State(object):
    
    state = None

#    def __init__(self):
        
        
    @staticmethod
    def set_state(s):
        trace("set state: {}".format(type(s).__name__))
        #to allow event handling
        s.on_entry()
        prev = State.state
        State.state = s;
        if prev != None:
            prev.on_exit() 


    #override to implement behaviour
    def handle_rfid(self, str):
        trace(str)
    def handle_barcode(self, str):
        trace(str)
    def handle_pin(self, str):
        trace(str)
    def handle_abort(self):
        trace("Abort")
    def handle_undo(self):
        trace("Undo")
    def on_entry(self):
        trace("enter: {}".format(type(self).__name__))
    def on_exit(self):
        trace("exit: {}".format(type(self).__name__))


class Start(State):
    
    def _init__(self):
        State.__init__(self)

    def handle_rfid(self, str):
        trace("Velcome user")
        State.set_state(rfid_check)



class id_fetcher(Thread):
#    URL = 'https://hal.osaa.dk/food'
    URL = 'http://localhost:8080'

    
    def __init__(self, rfid):
        Thread.__init__(self)
        self.rfid = rfid
        self.alive = 1

    def abort(self):
        trace("Killing the fetcher")
        self.alive = 0

    def run(self):
        data = "ID from HAL"
        # try:
        #     resp = urllib2.urlopen("{}/{}".format(self.URL, self.rfid.nr))
        #     data = resp.read()
        # except urllib2.URLError, e:
        #     print e.reason
        time.sleep(1)

        if self.alive:
            self.rfid.handle_hal(data)


class Rfid_check(State):
    
    def _init__(self):
        State.__init__(self)

    def on_entry(self):
        self.fetcher = id_fetcher(self)
        trace("get the rfid from hal")
        self.fetcher.start()

    def on_exit(self):
        #make sure fetcher is dead
        self.fetcher.abort()
        self.fetcher = None
        
    def handle_hal(self, data):
        print data
        State.set_state(ordering)
        
class Ordering(State):

    def _init__(self):
        State.__init__(self)

    def handle_pin(self, str):
        trace("shop smart, shop k-mart")
        State.set_state(pin_check)

    def handle_barcode(self, str):
        trace("ding")

    def on_entry(self):
        #clear orders
        trace("new shopper")




class Validator(Thread):
#    URL = 'https://hal.osaa.dk/food'
    URL = 'http://localhost:8080'

    
    def __init__(self, pincheck):
        Thread.__init__(self)
        self.pincheck = pincheck
        self.alive = 1

    def abort(self):
        trace("kill validator")
        self.alive = 0

    def run(self):
        data = "validation data"
        time.sleep(1)
        if self.alive:
            self.pincheck.handle_hal(data)


class Pin_check(State):

    def _init__(self):
        State.__init__(self)
        self.validator = None

    def on_entry(self):
        self.validator = Validator(self)
        trace("Check pin and order and everything")
        self.validator.start()

    def on_exit(self):
        #make sure fetcher is dead
        self.validator.abort()
        self.validator = None

    def handle_hal(self, data):
        trace("caching")
        State.set_state(start)





###using the states fro something

        


#init the states
start = Start()
rfid_check = Rfid_check()
ordering = Ordering()
pin_check = Pin_check()

State.set_state(start)
