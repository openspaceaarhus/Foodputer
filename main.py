#! /usr/bin/env python

import pygame, sys, math
import State
import Foodputer
import GUI
import putil

#SETTINGS
#TODO FULLSCREEN = 0
W = 800
H = 600

BG = (0,0,0)

pygame.init()

#vars
surface = pygame.display.set_mode((W,H))
clock = pygame.time.Clock()


Foodputer.set_state(State.start)
GUI.set_state( GUI.start)


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
            Foodputer.handle_input(strbuf)
            strbuf = ""
            GUI.set_charcount(len(strbuf))
        elif event.key == pygame.K_ESCAPE:
            quit()
        
        #manually store the valid input as a unicode-char-buffer
        key = event.unicode
        if valid_id_char(key):
            #print "valid"
            strbuf += key
            GUI.set_charcount(len(strbuf))




    #update the screen
    surface.fill(BG)
    GUI.Screen.state.update(dt)

    #draw stuff
    GUI.Screen.state.draw(surface)

    pygame.display.flip()
