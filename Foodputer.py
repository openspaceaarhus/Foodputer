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
    
    def total(self):
        total = 0
        for p in self.cart.keys():
            tup = self.cart[p]
            item = tup[0]
            cnt = tup[1]
            total += cnt * item.price

        return total

        
    
class Foodputer(object):
    state = None
    order = None
    accept_input = True



def new_order(name, token):
    Foodputer.order = Order(name, token)


def get_cart():
    if not Foodputer.order:
        return None
    return Foodputer.order.cart

def get_order():
    """return the order as a dict
    
    """
    if not Foodputer.order:
        return None
    order = Foodputer.order
    data = {}
    data['name'] = order.name
    data['token'] = order.token
#    data['cart'] = order.cart

    data['total'] = order.total()

    return data

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
    
#TODO move input accept to gui?
    if len(str) < 1 or not Foodputer.accept_input:
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
