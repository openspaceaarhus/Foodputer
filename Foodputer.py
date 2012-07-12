import State
import putil
import Products

class Order(object):
    
    def __init__(self, name, token):
        self.name = name
        self.token = token
        self.buy_list = []
        self.cart = {} #map id -> (product, #items)

    def add_item(self, item):
        print "add_item:", item
        #add to a stack of orders
        self.buy_list.append(item)
        #update inventory
        cnt = 1
        if item.id in self.cart:
            cur = self.cart[item.id]
            cnt += cur[1] 
            
        self.cart[item.id] = (item, cnt) 

    def remove_item(self, item):
        if not item.id in self.cart:
            putil.trace("NO such item in cart")
            return
        
        cur = self.cart[item.id]
        cnt = cur[1] - 1
        if cnt == 0:
            del self.cart[item.id]
        else:
            self.cart[item.id] = (item, cnt) #update cnt
            
    def undo_order(self):
        if len(self.buy_list) < 1:
            putil.trace("cant undo no more")
            return
        item = self.buy_list.pop()
        self.remove_item(item)
        GUI.info("Removed {} from cart".format(item.name))
        

        
    
class Foodputer(object):
    state = None
    order = None



def new_order(name, token):
    Foodputer.order = Order(name, token)


def get_cart():
    if not Foodputer.order:
        return None
    return Foodputer.order.cart
    

def add_item(item):
    if not Foodputer.order:
        putil.trace("trying to put things in non-cart")
        return
    Foodputer.order.add_item(item)

def undo():
    if not Foodputer.order:
        putil.trace("trying to undo a non-cart")
        return
    Foodputer.order.undo_order()
    
    


def is_barcode(str):
    return str[0] == 'b'

def is_rfid(str):
    return str[0] == 'r'

def is_pin(str):
    return str[0] == 'p'


def handle_input(str):
    """Is is RFID, BARCODE og PIN
    
    and what action to take"""
    
    if len(str) < 1:
        return
    if str == "a":
        Foodputer.state.handle_abort()
    elif str == "u":
        Foodputer.state.handle_undo()
    elif is_rfid(str):
        Foodputer.state.handle_rfid(str)
    elif is_barcode(str):
        Foodputer.state.handle_barcode(str)
    elif is_pin(str):
        Foodputer.state.handle_pin(str)
    else:
        print "Unknown input ", str
        
    putil.trace("main in state: {}".format(type(Foodputer.state).__name__))



        
def set_state(s):
    putil.trace("set state: {}".format(type(s).__name__))
    if Foodputer.state != None:
        Foodputer.state.on_exit() 
    Foodputer.state = s;
    s.on_entry()




#omfg circular imports fix w00t
import GUI
