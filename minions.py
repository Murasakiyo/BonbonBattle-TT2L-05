import pygame
import math
import torres
import state
from enemy3 import Enemy3

class Minions(pygame.sprite.Sprite):
    def __init__(self, game):
        # super().__init__(group)
        self.game = game
        self.camera = state.CameraGroup(self.game)
        self.player = torres.Player(self.game, self.camera)
        self.enemy3 = Enemy3(self.game)
        self.mini_rect = pygame.Rect(self.enemy3.rect_draw.x - 100, self.enemy3.rect_draw.y + 10, 30, 30)
        self.speed = 3

    def update(self, deltatime, player_action, player_x, player_y):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        self.player.rect.x += 400 * deltatime * direction_x 
        self.player.rect.y += 450 * deltatime * direction_y 

        self.mini_rect.clamp_ip(self.game.screen_rect)
        self.player.rect.clamp_ip(self.game.screen_rect)

        self.move_towards_player(player_x, player_y)



    def render(self, display):
        pygame.draw.rect(display, (255, 0, 255), self.mini_rect)
        pygame.display.flip()

    def move_towards_player(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player_x - self.mini_rect.x, player_y - self.mini_rect.y
        dist = math.hypot(dx, dy)

        dx, dy = dx / (dist + 1), dy / (dist + 1)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.mini_rect.x += dx * self.speed
        self.mini_rect.y += dy * self.speed