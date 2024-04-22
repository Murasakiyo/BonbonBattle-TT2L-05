import pygame
import time
import math
import spritesheet

class Enemy3(pygame.sprite.Sprite):
    def __init__(self, game, group):
        super().__init__(group)
        self.game = game
        self.rect = pygame.Rect(180, 180, 40, 40)
        self.color = "white"


    def update():
        pass

    def render():
        pass

    def move():
        pass
