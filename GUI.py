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

import pygame, math
import Foodputer
import putil
from Timeout import Timeout
from Anim import Anim

red = (255, 0, 0)
green = (0, 255,0)
blue = (0, 0, 255)
yellow = (255,255,0)



class Screen(object):
    small_font = ''
    large_font = ''    
    messages = []
    state = None
    char_cnt = 0

    def __init__(self):
        pygame.init()
        self.large_font = pygame.font.Font("./font/Bender.otf", 32)
        self.small_font = pygame.font.Font("./font/Bender.otf", 16)
        self.small_line = self.small_font.get_linesize()
        self.time = 0

    def draw(self, surface):
#        print "draw me like one of your french girls"
        self.large_txt(surface, "Open Space Aarhus Foodputer")

    def update(self, dt):
        self.time += dt

    def on_entry(self):
        putil.trace("GUI enter: {}".format(type(self).__name__))
    def on_exit(self):
        putil.trace("GUI exit: {}".format(type(self).__name__))

    def large_txt(self, surface, str, pos = (100, 200), color = green):
        txt = self.large_font.render(str, 1, color)
        surface.blit(txt, pos)

    def small_txt(self, surface, str, pos = (100, 200), color = green):
        txt = self.small_font.render(str, 1, color)
        surface.blit(txt, pos)




class StartScreen(Screen):

    def __init__(self):
        Screen.__init__(self)
        self.coin = Anim("coin_gold.png", (8,1), .1, (300, 500))

    def draw(self, surface):
#        print "draw me like one of your french girls"
        self.large_txt(surface, "Scan RFID to start")
        self.coin.draw(surface)

    def update(self, dt):
        Screen.update(self, dt)
        self.coin.update(dt)

class WaitScreen(Screen):

    def __init__(self, msg):
        Screen.__init__(self)
        self.msg = msg

    def draw(self, surface):
#        print "draw me like one of your french girls"
        self.large_txt(surface, self.msg)


class MessageScreen(Screen):

    def __init__(self, msg, timeout, next_screen, fine_print = False):
        Screen.__init__(self)
        self.msg = msg
        timer = Timeout(timeout, self)
        self.next_screen = next_screen
        self.fine_print = fine_print
        #stop input
        Foodputer.Foodputer.accept_input = False 
        timer.start()

    def draw(self, surface):
#        print "draw me like one of your french girls"
        if self.fine_print:
            self.small_txt(surface, self.msg, (100, 100), red)            
        else:
            self.large_txt(surface, self.msg, (100, 100), red)

    def callback(self):
        #allow input
        Foodputer.Foodputer.accept_input = True 

        print "I'm going through changes"
        set_state(self.next_screen)


class OrderScreen(Screen):

    def __init__(self):
        Screen.__init__(self)
        
    def draw(self, surface):
#        print "draw me like one of your french girls"
        order = Foodputer.Foodputer.order #hmmm
        self.large_txt(surface, "Hi {}".format(order.name), (10, 10))
        self.draw_messages(surface)
        self.draw_cart(surface)
        self.draw_strbuf(surface)

    def draw_messages(self, surface):
        yoffset = 10
        xoffset = 400
        self.large_txt(surface, "messages:", (xoffset, yoffset))
        yoffset += self.large_font.get_linesize()
        msg_cnt = len(Screen.messages)
        cnt = min(msg_cnt, 5)
        for i in range(cnt):
            msg = Screen.messages[msg_cnt - i - 1]
            self.small_txt(surface, msg[1], (xoffset, yoffset), message_level.get_color(msg[0]))
            yoffset += self.small_line



    def draw_cart(self, surface):
        yoffset = 200
        xoffset = 250
        self.large_txt(surface, "Cart:", (xoffset, yoffset))
        yoffset += self.large_font.get_linesize()
        cart = Foodputer.get_cart()
        if not cart:
            return
        total = 0
        xoffset2 = 450
        for k in cart.keys():
            tup = cart[k]
            item = tup[0]
            cnt = tup[1]
            total += cnt * item.price
            txt = "{} stk {} a".format(cnt, item.name)           
            self.small_txt(surface, txt, (xoffset, yoffset))
            txt = "{}{}".format(" " if item.price < 10 else "", "%0.2f" % item.price)
            self.small_txt(surface, txt , (xoffset2, yoffset))
            yoffset += self.small_line


        line = self.large_font.render("TOTAL        %0.2f" % total, 1, green)
        surface.blit(line, (xoffset, 500))

         
    def draw_strbuf(self, surface):
        txt = ''.join([ "*"] * Screen.char_cnt)
        txt = "Enter pin to complete order:{}".format(txt)
        self.large_txt(surface, txt, (10, 550))


################################################################################
#        STATEVARS                                                             #
################################################################################

start = StartScreen()
ordering = OrderScreen()
wait_rfid = WaitScreen("Awaiting HAL check of RFID")
wait_pin = WaitScreen("Awaiting HAL check of PIN")

def set_state(s):
    putil.trace("GUI set state: {}".format(type(s).__name__))
    if Screen.state != None:
        Screen.state.on_exit() 
    s.on_entry()
    Screen.state = s;

def set_charcount(cnt):
    Screen.char_cnt = cnt;


################################################################################
#        MESSAGES                                                              #
################################################################################
        
class message_level(object):
    INFO = 0
    WARN = 1
    ALERT = 2

    @staticmethod
    def get_color(level):
        """mixing gui and model

        because it is in the same place :S
        """
        if (level == message_level.INFO):
            return green
        elif (level == message_level.WARN):
            return yellow
        elif (level == message_level.ALERT):
            return red

################################################################################
#        Events to handle from foodputers statechanges                         #
################################################################################

#TODO better naming and more doc

def wait_for_rfid():
    """Show the user that the rfid is being checked
    
    """
    set_state(wait_rfid)


def no_rfid():
    """The Rfid were not valid

    """
    set_state(MessageScreen("Unknown RFID, try again", 1, start))

def hal_error(e):
    """Something went wrong whilst talking to HAL

    """
    txt = "HAL: {}".format(e)
    set_state(MessageScreen(txt, 6, start, True))

def valid_rfid():
    """The id process i succesfully completed
    
    Can start ordering
    """
    set_state(ordering)

def abort():
    """abort abort abort

    No more shopping
    """
    set_state(MessageScreen("Back to start", 1, start))


def start_pincheck():
    set_state(wait_pin)

def accepted_order():
    set_state(MessageScreen("Payment success", 3, start))

def wrong_pin(tries_left):

    txt = "WRONG PIN: {} tries left".format(tries_left)
    set_state(MessageScreen(txt, 3, start))

                
def not_enough_money():
    """Cue the canned laughter

    Keep shopping, user most remove items or abort
    """
    txt = "Not enough monies"
    set_state(MessageScreen(txt, 3, ordering))

def info(str):
        #use a screen
    print "INFO: ", str
    Screen.messages.append ( (message_level.INFO, str) )

def warn(str):
        #use a screen
    print "WARN: ", str
    Screen.messages.append ( (message_level.WARN, str) )

def alert(str):
        #use a screen
    Screen.messages.append ( (message_level.ALERT, str) )


def clear_messages():
    Screen.messages = []
