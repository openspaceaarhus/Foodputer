#! /usr/bin/env python

import pygame, sys, math


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

font = pygame.font.Font("./font/Bender.otf", 32)



class Slice_state:
    LOCKED = 0
    READY = 1
    DONE = 2
    WAITING = 3

def tup_avg(pair):
    return (pair[0] + pair[1]) * .5


class Slice:
    inner_r = 16

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

        center = (self.center[0] + self.inner_r * math.cos(self.angle + self.da * .5),
                  self.center[1] + self.inner_r * math.sin(self.angle + self.da * .5))

        p1 = (center[0] + self.r * math.cos(self.angle),
              center[1] + self.r * math.sin(self.angle))
        p2 = (center[0] + self.r * math.cos(self.angle + self.da),
              center[1] + self.r * math.sin(self.angle + self.da))

        pygame.draw.aaline(surface, color, center, p1, 6)
        pygame.draw.aaline(surface, color, center, p2, 6)
        
        #create amn Rect covering ze points
        # left = self.center[0] - self.r
        # top =  self.center[1] - self.r
        # rect = pygame.Rect(left, top, self.r * 2,self.r * 2)
        # pygame.draw.arc(surface, color, rect , self.angle, self.angle + self.da, 16)
        
        #arc sucks
        last = p1
        steps = 17
        ss = self.da/steps
        for i in range(steps + 1):
            da = i * ss
            cur = (center[0] + self.r * math.cos(self.angle + da),
                   center[1] + self.r * math.sin(self.angle + da))
            pygame.draw.aaline(surface, color, last, cur, 6)
            last = cur

        #the label
        label = font.render(self.get_text() ,1, (0,255,0))
        surface.blit(label, map(tup_avg, zip(p1,p2)))


    def update(self, clock):
        self.angle +=  .0001;
        Slice.inner_r = 12 + 3 * math.sin(clock*.001)
        
class Barcode(Slice):
    
    def __init__(self):
        Slice.__init__(self, Slice_state.READY)
        self.angle += 2 * self.da

    def get_text(self):
        if (Slice_state.READY == self.state):
            return "Enter barcode"
        elif (Slice_state.LOCKED == self.state):
            return "can't change product now"
        else:
            return self.product

    @staticmethod
    def is_barcode(str):
        return str[0] == 'b'

    def handle_barcode(self, str):
        """Handle the barcode input
        based on barcode state"""
        
        if barcode.state ==  Slice_state.DONE or barcode.state ==  Slice_state.READY:
            #set or change the product
            self.product = "club mate"
            #change to the new state
            barcode.state =  Slice_state.DONE
        else:        #beep
            sys.stdout.write("\a")
        

class Pin(Slice):
    
    def __init__(self):
        Slice.__init__(self, Slice_state.LOCKED)
        self.angle += self.da
    def get_text(self):
        return "Enter pincode"

    @staticmethod
    def is_pin(str):
        return str[0] == 'p'

    def handle_pin(self, str):
        """Handle the pin input
        
        based on pin state"""

        if self.state ==  Slice_state.DONE:
            print "have a nice day .. reset erverything for next order"
        elif self.state ==  Slice_state.READY:
            #start the order process
            #something async would be nice
            

            #change to the new state ?
            self.state =  Slice_state.WAITING
        elif self.state == Slice_state.LOCKED:
             #beep
            sys.stdout.write("\a")
        else:
            print "unknown state error"
        




class Rfid(Slice):
    
    def __init__(self):
        Slice.__init__(self, Slice_state.READY)

    def get_text(self):
        return "Enter RFID"

    @staticmethod
    def is_rfid(str):
        return str[0] == 'r'

    def handle_rfid(self, str):
        """Handle the rfid input

        based on rfid state"""

        if self.state ==  Slice_state.DONE:
            print "have a nice day .. reset erverything for next order"
        elif self.state ==  Slice_state.READY:
            #start the "get name and token" process
            #something async would be nice
            
            #change to the new state ?
            self.state =  Slice_state.WAITING
        elif self.state == Slice_state.LOCKED:
             #beep
            sys.stdout.write("\a")
        else:
            print "unknown state error"
        

    

barcode = Barcode()
pin = Pin()
rfid = Rfid()
                         


strbuf = ""

def valid_id_char(s):
    return s.isalnum() or "-" in s


def handle_input(str):
    """Is is RFID, BARCODE og PIN

    and what action to take"""

    if Rfid.is_rfid(str):
        rfid.handle_rfid(str)
    elif Barcode.is_barcode(str):
        barcode.handle_barcode(str)
    elif Pin.is_pin(str):
        pin.handle_pin(str)
    else:
        print "Unknown input ", str

    
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
    barcode.update(walltime)
    rfid.update(walltime)
    if rfid.state == Slice_state.DONE  and  barcode.state == Slice_state.DONE:
        pin.state = Slice_state.READY
    pin.update(walltime)


    #update the screen
    screen.fill(BG)
    barcode.draw(screen)
    pin.draw(screen)
    rfid.draw(screen)



    pygame.display.flip()

