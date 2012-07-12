#! /usr/bin/env python

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
