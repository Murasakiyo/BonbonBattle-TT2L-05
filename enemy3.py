import pygame
import time
import math
import spritesheet

class Enemy3(pygame.sprite.Sprite):
    def __init__(self, game, group):
        # super().__init__(group)
        self.game = game
        self.rect_draw = pygame.Rect(180, 180, 40, 40)
        self.color = "white"


    def update(self, deltatime, player_action):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        self.rect_draw.x += 400 * deltatime * direction_x 
        self.rect_draw.y += 450 * deltatime * direction_y 

    def render(self, display):
        pygame.draw.rect(display, self.color, self.rect_draw)

    def move():
        pass
