import sys
from Slice import Slice, Slice_state

products = {}

class Product:
    
    def __init__(self, name, text, price):
        self.name = name.strip()
        self.text = text.strip()
        self.price = price
        
    def __str__(self):
        price = "%0.2f" % self.price
        return "{} {},-".format(self.name, price)
    

def read_productlist(filename):
    """read a csv text file with barcodes and descriptions

    Store in ascociative array, mapping barcode -> product
    """
    for line in open(filename):
        if line.startswith("#"):
            continue
        p = line.split(",")
        products[p[0]] = Product(p[1], p[2], float(p[3]))


def order_string(order):
    """a text rep of a list of products

    """
    buf = []
    total = 0.0
    for p in order:
        buf.append(p.__str__())
        total += p.price

    buf.append("TOTAL %0.2f,-" % total)

    return "\n".join(buf)

class Barcode(Slice):
    
    def __init__(self):
        Slice.__init__(self, Slice_state.READY)
        self.angle += 2 * self.da
        read_productlist("products.csv")
        self.order = []

    def get_text(self):
        if (Slice_state.READY == self.state):
            return "Enter barcode"
        elif (Slice_state.LOCKED == self.state):
            return order_string(self.order)
        # MESSAGE "can't change product now"
        else:
            return order_string(self.order)

    @staticmethod
    def is_barcode(str):
        return str[0] == 'b'

    def handle_barcode(self, str):
        """Handle the barcode input
        based on barcode state"""
        

        if self.state ==  Slice_state.DONE or self.state ==  Slice_state.READY:
            #set or change the product
            try:
                self.order.append(products[str])
            except KeyError, e:
                print "No such product is for sale"
                #MESAGE
                return
                
            self.state =  Slice_state.DONE
        elif self.state == Slice_state.LOCKED:
             #beep
            sys.stdout.write("\a")
        elif self.state == Slice_state.WAITING:
             #beep
            print "should never wait for db access"
        else:
            print "unknown state error"
        

