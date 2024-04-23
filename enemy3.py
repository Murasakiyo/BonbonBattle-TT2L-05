import pygame
import time
import math
import spritesheet
import state
import torres

class Enemy3(pygame.sprite.Sprite):
    def __init__(self, game, group):
        # super().__init__(group)
        self.game = game
        self.camera = state.CameraGroup(self.game)
        self.player = torres.Player(self.game, self.camera)
        self.rect_draw = pygame.Rect(180, 180, 40, 40)
        self.enemyborder = pygame.Rect(100, 90, 900, 370)
        self.color = "white"
        self.speed = -1


    def update(self, deltatime, player_action):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        self.player.rect.x += 400 * deltatime * direction_x 
        self.player.rect.y += 450 * deltatime * direction_y 

        self.rect_draw.clamp_ip(self.enemyborder)

        self.move_towards_player()

    def render(self, display):
        pygame.draw.rect(display, self.color, self.rect_draw)
        # pygame.draw.rect(display, self.color, self.enemyborder) #draws the enemy border for refference
        pygame.display.flip()

    def move_towards_player(self):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = self.player.rect.x - self.rect_draw.x, self.player.rect.y - self.rect_draw.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / (dist + 1), dy / (dist + 1)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect_draw.x += dx * self.speed
        self.rect_draw.y += dy * self.speed


class Minions(pygame.sprite.Sprite):
    def __init__(self, game, group):
        # super().__init__(group)
        self.game = game

    def update(self, deltatime, player_action):
        pass

    def render(self, display):
        pass
