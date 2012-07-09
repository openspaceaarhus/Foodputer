import pygame, math

class Slice_state:
    LOCKED = 0
    READY = 1
    DONE = 2
    WAITING = 3

def tup_avg(pair):
    return (pair[0] + pair[1]) * .5


class Slice:
    inner_r = 16
    font = ''
    def __init__(self, state = Slice_state.READY, W = 800, H = 600):
        self.font = pygame.font.Font("./font/Bender.otf", 32)
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
        label = self.font.render(self.get_text() ,1, (0,255,0))
        surface.blit(label, map(tup_avg, zip(p1,p2)))


    def update(self, clock):
        self.angle +=  .0001;
        Slice.inner_r = 12 + 3 * math.sin(clock*.001)
