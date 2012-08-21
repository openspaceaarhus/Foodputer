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
import sys
import hashlib
import putil
import time
import urllib2
import random
import json
import Foodputer

ACCEPT = 0
DENY = 1
NOFUNDS = 2

#    URL = 'https://hal.osaa.dk/food'
URL = 'http://localhost:8080'

LOCAL = 0


class Validator(Thread):
    def __init__(self, pincheck):
        Thread.__init__(self)
        self.pincheck = pincheck
        self.alive = 1

    def abort(self):
        putil.trace("kill validator")
        self.alive = 0

    def run(self):
        pin = self.pincheck.pin
        
        #for debugging and mocking
        if (LOCAL):
            data = ACCEPT
            if pin == "p4":
                data = DENY
            elif pin == "p3":
                data =  NOFUNDS
            time.sleep(1)
            if self.alive:
                self.pincheck.handle_hal(data)
            return
        
        data = Foodputer.get_order()

        #remove token from data, but use it in sha1-digest
        msg = "{}{}{}".format(data['name'], data['total'],data['token'])
        digest = hashlib.sha512(msg).hexdigest()
        del data['token']
        data['signature'] = digest
        

        payload = json.dumps(data).encode('utf-8')
        ret = None
        try:
            print payload
            resp = urllib2.urlopen(URL, payload)
            print "resp info", resp.info()
            txt = resp.read()
            print "JSON is: ", txt
            ret = json.loads(txt)
            
        except (urllib2.URLError, urllib2.HTTPError), e:
            putil.trace("could not contact hal!!")
            self.alive = False;
            self.pincheck.handle_fail(e)
        except:
            putil.trace("Other error {}".format(sys.exc_info()[0]))


        if self.alive:
            self.pincheck.handle_hal(ret)

        

class id_fetcher(Thread):
    
    def __init__(self, rfid):
        Thread.__init__(self)
        self.rfid = rfid
        self.alive = 1

    def abort(self):
        putil.trace("Killing the fetcher")
        self.alive = 0

    def run(self):
        nr = self.rfid.nr
        #for debugging and mocking
        if (LOCAL):
            data = {'user': "bent hansen", 'token':"TokenToken"} if nr != "r2" else None
            time.sleep(1)
            self.rfid.handle_hal(data)
            return

        data = None
        try:
            resp = urllib2.urlopen("{}/{}".format(URL, nr))
            print resp.info()
            data = json.loads(resp.read())
            
        except (urllib2.URLError, urllib2.HTTPError), e:
            putil.trace("could not contact hal!!")
            self.alive = False;
            self.rfid.handle_fail(e)
        except:
            putil.trace("Other error {}".format(sys.exc_info()[0]))


        if self.alive:
            self.rfid.handle_hal(data)


