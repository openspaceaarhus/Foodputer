#! /usr/bin/env python

import pygame, sys, math


#SETTINGS
#TODO FULLSCREEN = 0
W = 800
H = 600

BG = (0,0,0)



#vars
screen = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()
running = 1


class Slice_state:
    LOCKED = 0
    READY = 1
    DONE = 2

class Slice:
    def __init__(self, state):
        self.state = state
        self.angle = 0
        self.da = 2.0 * math.pi / 3.0
        self.center = (W/2, H/2)
        self.r = min(W,H) / 3.0

    def draw(self, surface):
#        print "draw me like one of your french girls"
        color = (0,255,0)
        if (Slice_state.READY == self.state):
            color = (255,255,0)
        elif (Slice_state.LOCKED == self.state):
            color = (255,0,0)
        
        center = (self.center[0] + 12.0 * math.cos(self.angle + self.da * .5),
                  self.center[1] + 12.0 * math.sin(self.angle + self.da * .5))

        p1 = (center[0] + self.r * math.cos(self.angle),
              center[1] + self.r * math.sin(self.angle))
        p2 = (center[0] + self.r * math.cos(self.angle + self.da),
              center[1] + self.r * math.sin(self.angle + self.da))

        pygame.draw.line(surface, color, center, p1, 6)
        pygame.draw.line(surface, color, center, p2, 6)
        
        #create amn Rect covering ze points
        # left = self.center[0] - self.r
        # top =  self.center[1] - self.r
        # rect = pygame.Rect(left, top, self.r * 2,self.r * 2)
        # pygame.draw.arc(surface, color, rect , self.angle, self.angle + self.da, 16)
        
        #arc sucks
        last = p1
        steps = 7
        ss = self.da/steps
        for i in range(steps + 1):
            da = i * ss
            cur = (center[0] + self.r * math.cos(self.angle + da),
                   center[1] + self.r * math.sin(self.angle + da))
            pygame.draw.line(surface, color, last, cur, 6)
            last = cur


        
class Barcode(Slice):
    
    def __init__(self):
        Slice.__init__(self, Slice_state.READY)
        self.angle += 2 * self.da

class Pin(Slice):
    
    def __init__(self):
        Slice.__init__(self, Slice_state.LOCKED)
        self.angle += self.da

class Rfid(Slice):
    
    def __init__(self):
        Slice.__init__(self, Slice_state.DONE)



barcode = Barcode()
pin = Pin()
rfid = Rfid()
                         


strbuf = ""

def valid_id_char(s):
    return s.isalnum() or "-" in s


def is_rfid(str):
    return str[0] == 'r'

def handle_rfid(str):
    """Handle the rfid input

    based on rfid state"""


def is_barcode(str):
    return str[0] == 'b'

def handle_barcode(str):
    """Handle the barcode input

    based on barcode state"""
    
    if barcode.state ==  Slice_state.DONE or barcode.state ==  Slice_state.LOCKED:
        #do nothing
        print "cant do nothing usefull maybe beep to annoy the user?"
    else :
        barcode.state = Slice_state.DONE;
    

def is_pin(str):
    return str[0] == 'p'

def handle_pin(str):
    """Handle the pin input

    based on pin state"""



def handle_input(str):
    """Is is RFID, BARCODE og PIN

    and what action to take"""

    if is_rfid(str):
        handle_rfid(str)
    elif is_barcode(str):
        handle_barcode(str)
    elif is_pin(str):
        handle_pin(str)
    else:
        print "Unknown input ", str

    
def quit():
    print "bye bye"
    sys.exit(0)

while running:


    screen.fill(BG)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()

        if not hasattr(event, 'key') :
            continue

        if not event.type == pygame.KEYDOWN:
            continue

        if event.key == pygame.K_RETURN:
            handle_input(strbuf)
            strbuf = ""
        elif event.key == pygame.K_ESCAPE:
            quit()
        

        key = event.unicode
        print key

        if valid_id_char(key):
            print "valid"
            strbuf += key

    #update the screen
    screen.fill(BG)
    barcode.draw(screen)
    pin.draw(screen)
    rfid.draw(screen)

    pygame.display.flip()

