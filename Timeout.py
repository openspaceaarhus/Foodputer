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
