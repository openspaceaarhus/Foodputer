import putil
from  Foodputer import *
import Hal
from Products import Product
import GUI

class State(object):

    #override to implement behaviour
    def handle_rfid(self, str):
        putil.trace("{}:handle_rfid({})".format(type(Foodputer.state).__name__, str))
    def handle_barcode(self, str):
        putil.trace("{}:handle_barcode({})".format(type(Foodputer.state).__name__, str))
    def handle_pin(self, str):
        putil.trace("{}:handle_pin({})".format(type(Foodputer.state).__name__, str))
    def handle_abort(self):
        putil.trace("{}:handle_abort({})".format(type(Foodputer.state).__name__, ""))
    def handle_undo(self):
        putil.trace("{}:handle_undo({})".format(type(Foodputer.state).__name__, ""))
    def on_entry(self):
        putil.trace("enter: {}".format(type(self).__name__))
    def on_exit(self):
        putil.trace("exit: {}".format(type(self).__name__))


class Start(State):
    
    def _init__(self):
        State.__init__(self)

    def handle_rfid(self, str):
        putil.trace("Velcome user")
        Foodputer.set_state(rfid_check)


class Rfid_check(State):
    
    def _init__(self):
        State.__init__(self)

    def on_entry(self):
        self.fetcher = Hal.id_fetcher(self)
        putil.trace("get the rfid from hal")
        self.fetcher.start()

    def on_exit(self):
        #make sure fetcher is dead
        self.fetcher.abort()
        self.fetcher = None
        
    def handle_hal(self, data):
        print data
        Foodputer.new_order("username", "TokenToken")
        Foodputer.set_state(ordering)
        
class Ordering(State):

    def _init__(self):
        State.__init__(self)

    def handle_pin(self, str):
        putil.trace("shop smart, shop k-mart")
        Foodputer.set_state(pin_check)

    def handle_barcode(self, str):
        putil.trace("ding")
        item = Product.get_from_barcode(str)
        if item == None:
            GUI.warn("Unknown product cannot buy here")
            return
        Foodputer.order.add_item(item)

    def on_entry(self):
        #clear orders
        putil.trace("new shopper")
        
    def handle_undo(self):
        Foodputer.order.undo_order()


class Pin_check(State):

    def _init__(self):
        State.__init__(self)
        self.validator = None

    def on_entry(self):
        self.validator = Hal.Validator(self)
        putil.trace("Check pin and order and everything")
        self.validator.start()

    def on_exit(self):
        #make sure fetcher is dead
        self.validator.abort()
        self.validator = None

    def handle_hal(self, data):
        putil.trace("caching")
        Foodputer.set_state(start)





###using the states fro something

        


#init the states
start = Start()
rfid_check = Rfid_check()
ordering = Ordering()
pin_check = Pin_check()
