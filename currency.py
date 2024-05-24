import pygame
import random

class Sugarcube(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        image = pygame.image.load('sprites/sugarcube.png').convert_alpha()
        self.image = pygame.transform.scale(image, (40,40)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = random.randint(0, 1100), random.randint(0, 600)
        self.image_mask = pygame.mask.from_surface(self.image)
        self.current_sugarcubes = 0

    def update(self):
        pass

    def collect(self, player):
        self.current_sugarcubes += 25
        print(f"Sugarcubes: {self.current_sugarcubes}")
        self.kill()   # remove sprite

    def render(self, display):
        display.blit(self.image, self.rect)

    