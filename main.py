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

    def draw(self, surface):
#        print "draw me like one of your french girls"
        color = (0,255,0)
        if (Slice_state.READY == self.state):
            color = (255,255,0)
        elif (Slice_state.LOCED == self.state):
            color = (255,0,0)
        pygame.draw.line(surface, color, (0,0), (W,H))
        
        
class Barcode(Slice):
    
    def __init__(self):
        Slice.__init__(self, Slice_state.READY)

class Pin(Slice):
    
    def __init__(self):
        Slice.__init__(self, Slice_state.LOCKED)

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

    pygame.display.flip()

