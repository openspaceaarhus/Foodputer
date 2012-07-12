from threading import Thread
import time

class Timeout(Thread):

    def __init__(self, secs, obj):
        Thread.__init__(self)
        self.secs = secs
        self.obj = obj
        self.alive = True
        
    def cancel(self):
        self.alive = False

    def run(self):
        time.sleep(self.secs)
        if self.alive:
            print "callback to: ", self.obj
            self.obj.callback()
