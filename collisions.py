import pygame
import time
from enemy1 import *

class Collisions():
    def __init__(self, game):
        self.game = game
        
    def load_for_collision(self):
        # self.enemy1 = FrogEnemy(self.game)
        self.tongue = Tongue(self.game)
        self.tongue2 = Tongue2(self.game)
        self.health_bar = pygame.Rect(10, 10, 250, 40)
        self.health_rect = pygame.Rect(10, 10, 250, 40)
        self.moxie_rect = pygame.Rect(10, 150, 40, 250)

    def update_collisions(self, deltatime, player_lines, healthpoints):
        if any(self.tongue.rect.clipline(*line) for line in player_lines):
            self.take_damage = True

        if any(self.tongue2.rect.clipline(*line) for line in player_lines):
            self.take_damage = True

        if self.take_damage == True:
            healthpoints -= 5
            print("Hit")
        
        self.health_bar = pygame.Rect(10, 10, healthpoints, 40)

    def collision_render(self, display):
        pygame.draw.rect(display, "black", self.health_rect)
        pygame.draw.rect(display, "green", self.health_bar)



