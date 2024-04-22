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
        self.speed = 5


    def update(self, deltatime, player_action):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        # self.rect_draw.x += 400 * deltatime * direction_x 
        # self.rect_draw.y += 450 * deltatime * direction_y 

        self.move_towards_player(player_action)

    def render(self, display):
        pygame.draw.rect(display, self.color, self.rect_draw)

    def move_towards_player(self, player):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player.rect.x - self.rect_draw.x, player.rect.y - self.rect_draw.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / dist, dy / dist  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect_draw.x += dx * self.speed
        self.rect_draw.y += dy * self.speed
