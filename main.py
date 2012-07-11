#! /usr/bin/env python

import pygame, sys, math

from State import *
from Foodputer import *
from GUI import  *
import putil

#SETTINGS
#TODO FULLSCREEN = 0
W = 800
H = 600

BG = (0,0,0)

pygame.init()

#vars
screen = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()


Foodputer.set_state(start)
Foodputer.screen = Screen()

def valid_id_char(s):
    return s.isalnum() or "-" in s
    
def quit():
    print "bye bye"
    sys.exit(0)

walltime = 0
strbuf = ""
running = 1
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




    #update the screen
    screen.fill(BG)
    Foodputer.screen.update(dt)

    #draw stuff
    Foodputer.screen.draw(screen)

    pygame.display.flip()



