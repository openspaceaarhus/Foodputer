#the products
productfile = "products.csv"

import putil
    

class Product:
    atlas = {}  #the worldmap of prices? :S
    
    def __init__(self, name, text, price, barcode):
        self.name = name.strip()
        self.text = text.strip()
        self.price = price
        self.id = barcode
        
    def __str__(self):
        price = "%0.2f" % self.price
        return "{} {},-".format(self.name, price)
    
    @staticmethod
    def read_productlist():
        """read a csv text file with barcodes and descriptions
        
        Store in ascociative array, mapping barcode -> product
        """
        for line in open(productfile):
            if line.startswith("#"):
                continue
            p = line.split(",")
            Product.atlas[p[0]] = Product(p[1], p[2], float(p[3]), p[0])
            
            putil.trace(Product.atlas[p[0]])


    @staticmethod
    def get_from_barcode(barcode):
        if barcode in Product.atlas:
            return Product.atlas[barcode]
        return None
