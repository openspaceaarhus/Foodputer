#! /usr/bin/env python

import pygame, sys, math

from Slice import Slice, Slice_state
from Barcode import Barcode
from Rfid import Rfid
from Pin import Pin

from State import *


#SETTINGS
#TODO FULLSCREEN = 0
W = 800
H = 600

BG = (0,0,0)

pygame.init()

#vars
screen = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()
running = 1

strbuf = ""

def valid_id_char(s):
    return s.isalnum() or "-" in s


def handle_input(str):
    """Is is RFID, BARCODE og PIN

    and what action to take"""
    
    if len(str) < 1:
        return

    if Rfid.is_rfid(str):
        State.state.handle_rfid(str)
    elif Barcode.is_barcode(str):
        State.state.handle_barcode(str)
    elif Pin.is_pin(str):
        State.state.handle_pin(str)
    else:
        print "Unknown input ", str

    trace("main in state: {}".format(type(State.state).__name__))
    
def quit():
    print "bye bye"
    sys.exit(0)


walltime = 0

while running:
    dt = clock.tick(90)
    walltime += dt
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
        
        #manually store the valid input as a unicode-char-buffer
        key = event.unicode
        if valid_id_char(key):
            #print "valid"
            strbuf += key


    #do the logic
    # barcode.update(walltime)
    # rfid.update(walltime)
    # if rfid.state == Slice_state.DONE  and  barcode.state == Slice_state.DONE:
    #     pin.state = Slice_state.READY
    # pin.update(walltime)


    #update the screen
    screen.fill(BG)
    # barcode.draw(screen)
    # pin.draw(screen)
    # rfid.draw(screen)



    pygame.display.flip()

