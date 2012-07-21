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

#the products
productfile = "products.csv"

import putil
import json    

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

    def __repr__(self):
        return  self.name


def get_from_barcode(barcode):
    if barcode in Product.atlas:
        return Product.atlas[barcode]
    return None



Product.read_productlist()
