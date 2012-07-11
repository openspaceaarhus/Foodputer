from State import * 
import putil
from Products import Product 

class order(object):
    
    def __init__(self, name, token):
        self.name = name
        self.token = token
    
class Foodputer(object):
    state = None
    order = None

Product.read_productlist()

def set_state(s):
    putil.trace("set state: {}".format(type(s).__name__))
    if Foodputer.state != None:
        Foodputer.state.on_exit() 
        
    s.on_entry()
    Foodputer.state = s;

def new_order(name, token):
    Foodputer.order = order(name, token)

def info(str):
        #use a screen
    print "INFO: ", str

def warn(str):
        #use a screen
    print "WARN: ", str

def alert(str):
        #use a screen
    print "ALERT: ", str        
