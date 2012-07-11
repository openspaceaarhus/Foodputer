#the stuff that talks to HAL
from threading import Thread
import putil
import time
import urllib2



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
        data = "validation data"
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
        data = "ID from HAL"
        # try:
        #     resp = urllib2.urlopen("{}/{}".format(self.URL, self.rfid.nr))
        #     data = resp.read()
        # except urllib2.URLError, e:
        #     print e.reason
        time.sleep(1)

        if self.alive:
            self.rfid.handle_hal(data)


