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
import putil

def cols(tup):
    return tup[0]

def rows(tup):
    return tup[1]


class Anim(object):
  
    def __init__(self, imgname, layout = (1,1), animrate = 1, pos = (200, 200)):
        pygame.init()
        try:
            img = pygame.image.load("./img/{}".format(imgname))
        except pygame.error:
            putil.trace("Could not open ./img/{}".format(imgname))

        self.img = img  #img.convert() #maybe convert alpha, but to make sure the color format matches screen etc
        w = img.get_width()
        h = img.get_height()
        fw = w / cols(layout)
        fh = h / rows(layout)
        frames = []
        for row in range(rows(layout)):
            for col in range(cols(layout)):
                r = pygame.Rect((col*fw, row*fh), (fw, fh))
                frames.append(self.img.subsurface(r))

        self.frames = frames
        self.cur_frame = 0
        self.walltime = 0
        self.animrate = animrate
        self.pos = pos

    def update(self, dt):
        self.walltime += dt * .001;
        if self.walltime > self.animrate:
            self.walltime -= self.animrate
            self.cur_frame += 1
            self.cur_frame %= len(self.frames)

    def draw(self, surface):
        surface.blit(self.frames[self.cur_frame], self.pos)


