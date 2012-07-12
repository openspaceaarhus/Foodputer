import pygame


pygame.init()

deny_snd = pygame.mixer.Sound("./Sound/cantdo.wav")
start_snd = pygame.mixer.Sound("./Sound/playgame.wav")
coin_snd = pygame.mixer.Sound("./Sound/31377__freqman__27-coins.wav")

def deny():
    deny_snd.play()


