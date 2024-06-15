import pygame
import time
pygame.mixer.init()

circus_bgmusic = pygame.mixer.Sound("sounds/lounge.wav")

channel_1 = circus_bgmusic.play(-1)
print("playing_sound")