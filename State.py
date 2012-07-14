# This file is part of FoodPuter.

#     Foobar is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     Foobar is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with Foobar.  If not, see <http://www.gnu.org/licenses/>.

#The main state machine code

#The logic of the foodputer resides here
#The GUI part resides in GUI.py and they should be as loosly coupled as
#possible

import putil
import Foodputer
import Hal
import Products
import GUI

class State(object):

    #override to implement behaviour
    def handle_rfid(self, str):
        putil.trace("{}:handle_rfid({})".format(type(self).__name__, str))
    def handle_barcode(self, str):
        putil.trace("{}:handle_barcode({})".format(type(self).__name__, str))
    def handle_pin(self, str):
        putil.trace("{}:handle_pin({})".format(type(self).__name__, str))
    def handle_abort(self):
        putil.trace("{}:handle_abort({})".format(type(self).__name__, ""))
    def handle_undo(self):
        putil.trace("{}:handle_undo({})".format(type(self).__name__, ""))
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
        GUI.wait_for_rfid()
        self.fetcher = Hal.id_fetcher(self)
        putil.trace("get the rfid from hal")
        self.fetcher.start()

    def on_exit(self):
        #make sure fetcher is dead
        self.fetcher.abort()
        self.fetcher = None
        
    def handle_hal(self, data):
        if not data:
            Foodputer.set_state(start)
            GUI.no_rfid()
            return
        Foodputer.new_order( data[0], data[1]) 
        Foodputer.set_state(ordering)
        Pin_check.tries_left = 3;
        GUI.valid_rfid()


class Ordering(State):

    def _init__(self):
        State.__init__(self)

    def handle_pin(self, str):
        putil.trace("shop smart, shop k-mart")
        Pin_check.pin = str
        Foodputer.set_state(pin_check)

    def handle_barcode(self, str):
        putil.trace("ding")
        item = Products.get_from_barcode(str)
        if item == None:
            GUI.warn("Unknown product cannot buy here")
            return
        GUI.info("Added {} - \"{}\"".format(item.name, item.text))
        Foodputer.add_item(item)


    def handle_abort(self):
        Foodputer.set_state(start)
        GUI.abort()

    def on_entry(self):
        putil.trace("new shopper")
        GUI.clear_messages()
        
    def handle_undo(self):
        Foodputer.undo()


class Pin_check(State):
    tries_left = 0;
    pin = ""
    def _init__(self):
        State.__init__(self)
        self.validator = None

    def on_entry(self):
        GUI.start_pincheck()
        self.validator = Hal.Validator(self)
        putil.trace("Check pin and order and everything")
        self.validator.start()

    def on_exit(self):
        #make sure fetcher is dead
        self.validator.abort()
        self.validator = None

    def handle_hal(self, data):
        putil.trace("caching")
        if data == Hal.ACCEPT:
            Foodputer.set_state(start)
            GUI.accepted_order()
        elif data == Hal.DENY:
            if Pin_check.tries_left == 0:
                self.abort()
            else:
                Pin_check.tries_left -= 1;
                Foodputer.set_state(ordering)
                GUI.wrong_pin(Pin_check.tries_left)
        elif data == Hal.NOFUNDS:
            Foodputer.set_state(ordering)
        else:
            putil.trace("no such return is nice");
            
                        
    def handle_abort():
        Foodputer.set_state(start)
        GUI.abort()


###using the states for something


#init the states
start = Start()
rfid_check = Rfid_check()
ordering = Ordering()
pin_check = Pin_check()
