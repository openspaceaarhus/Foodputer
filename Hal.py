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


#the stuff that talks to HAL
#it is a crude mock up for now

from threading import Thread
import putil
import time
import urllib2
import random

ACCEPT = 0
DENY = 1
NOFUNDS = 2


class Validator(Thread):
#    URL = 'https://hal.osaa.dk/food'
    URL = 'http://localhost:8080'

    
    def __init__(self, pincheck):
        Thread.__init__(self)
        self.pincheck = pincheck
        self.alive = 1

    def abort(self):
        putil.trace("kill validator")
        self.alive = 0

    def run(self):
        pin = self.pincheck.pin
        data = ACCEPT
        if pin == "p4":
            data = DENY
        elif pin == "p3":
            data =  NOFUNDS
        time.sleep(1)
        if self.alive:
            self.pincheck.handle_hal(data)




class id_fetcher(Thread):
#    URL = 'https://hal.osaa.dk/food'
    URL = 'http://localhost:8080'

    
    def __init__(self, rfid):
        Thread.__init__(self)
        self.rfid = rfid
        self.alive = 1

    def abort(self):
        putil.trace("Killing the fetcher")
        self.alive = 0

    def run(self):
        data = ("Bent hansen", "token token")
        if random.random() > .8:
            data = None
        # try:
        #     resp = urllib2.urlopen("{}/{}".format(self.URL, self.rfid.nr))
        #     data = resp.read()
        # except urllib2.URLError, e:
        #     print e.reason
        time.sleep(1)

        if self.alive:
            self.rfid.handle_hal(data)


