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

import putil
import Foodputer
import Hal
import Products
import GUI
import SoundEffects

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
        GUI.set_state(GUI.wait_rfid)
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
            GUI.set_state(GUI.MessageScreen("Unknown RFID, try again", 1, GUI.start))
            return
        Foodputer.new_order( data[0], data[1]) 
        Foodputer.set_state(ordering)
        GUI.set_state(GUI.ordering)
        Pin_check.tries_left = 3;
                
        
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
            SoundEffects.deny()
            return
        GUI.info("Added {} - \"{}\"".format(item.name, item.text))
        Foodputer.add_item(item)


    def handle_abort(self):
        Foodputer.set_state(start)
        GUI.set_state(GUI.MessageScreen("Back to start", 1, GUI.start))
        

    def on_entry(self):
        putil.trace("new shopper")
        SoundEffects.start_snd.play()
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
        GUI.set_state(GUI.wait_pin)
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
            SoundEffects.coin_snd.play()
            GUI.set_state(GUI.MessageScreen("Payment success", 3, GUI.start))
        elif data == Hal.DENY:
            if Pin_check.tries_left == 0:
                Foodputer.set_state(start)
                GUI.set_state(GUI.MessageScreen("NO MORE TRIES WRONG PIN", 3, GUI.start))
            else:
                Pin_check.tries_left -= 1;
                Foodputer.set_state(ordering)
                txt = "WRONG PIN: {} tries left".format(Pin_check.tries_left)
                GUI.set_state(GUI.MessageScreen(txt, 3, GUI.start))
        elif data == Hal.NOFUNDS:
            Foodputer.set_state(ordering)
            txt = "Not enough monies"
            GUI.set_state(GUI.MessageScreen(txt, 3, GUI.ordering))
        else:
            putil.trace("no such return is nice");
            
                        



###using the states for something

        


#init the states
start = Start()
rfid_check = Rfid_check()
ordering = Ordering()
pin_check = Pin_check()
