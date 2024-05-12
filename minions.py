import pygame
import math

class Minions(pygame.sprite.Sprite):
    def __init__(self, game, enemy3_rectx, enemy3_recty, speed):
        super().__init__()
        self.game = game
        self.rect = pygame.Rect(enemy3_rectx - 100, enemy3_recty, 30, 30) #left
        self.minion_speed = speed # 2
        self.damage = 10

    def update(self, deltatime, player_action, player_x, player_y):

        self.rect.clamp_ip(self.game.screen_rect)

        self.move_towards_player(player_x, player_y)

    def render(self, display):
        pygame.draw.rect(display, (255, 0, 255), self.rect)

    def move_towards_player(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player_x - self.rect.x, player_y - self.rect.y
        dist = math.hypot(dx, dy)

        dx, dy = dx / (dist + 1), dy / (dist + 1)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.minion_speed
        self.rect.y += dy * self.minion_speed



        