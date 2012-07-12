import pygame, math
import Foodputer
import putil


red = (255, 0, 0)
green = (0, 255,0)
blue = (0, 0, 255)
yellow = (255,255,0)



class Screen(object):
    small_font = ''
    large_font = ''    
    
    messages = []
    
    state = None

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

    def draw(self, surface):
#        print "draw me like one of your french girls"
        self.large_txt(surface, "Scan RFID to start")
    


class WaitScreen(Screen):

    def __init__(self, msg):
        Screen.__init__(self)
        self.msg = msg

    def draw(self, surface):
#        print "draw me like one of your french girls"
        self.large_txt(surface, self.msg)


class OrderScreen(Screen):

    def __init__(self):
        Screen.__init__(self)
        
    def draw(self, surface):
#        print "draw me like one of your french girls"
        self.draw_messages(surface)
        self.draw_cart(surface)

    def draw_messages(self, surface):
        heading = self.large_font.render("messages:", 1, green)
        yoffset = 250
        xoffset = 200
        surface.blit(heading, (xoffset, yoffset))
        yoffset += self.large_font.get_linesize()
        msg_cnt = len(Screen.messages)
        cnt = min(msg_cnt, 5)
        for i in range(cnt):
            msg = Screen.messages[msg_cnt - i - 1]
            self.small_txt(surface, msg[1], (xoffset, yoffset), message_level.get_color(msg[0]))
            yoffset += self.small_line



    def draw_cart(self, surface):
        heading = self.large_font.render("Cart:", 1, green)
        yoffset = 50
        xoffset = 200
        self.large_txt(surface, "Cart:", (xoffset, yoffset))
        yoffset += self.large_font.get_linesize()
        cart = Foodputer.get_cart()
        if not cart:
            return
        total = 0
        xoffset2 = 400
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


        line = self.large_font.render("TOTAL %0.2f" % total, 1, green)
        surface.blit(line, (xoffset, yoffset))

         

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
