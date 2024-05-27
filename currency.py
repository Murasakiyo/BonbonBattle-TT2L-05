import pygame
import random

class Sugarcube(pygame.sprite.Sprite):
    def __init__(self, game, value):
        super().__init__()
        self.game = game
        image = pygame.image.load('sprites/sugarcube.png').convert_alpha()
        self.image = pygame.transform.scale(image, (40,40)).convert_alpha()
        self.rect = self.image.get_rect()
        min_x, max_x = 80, self.game.SCREENWIDTH - 80
        min_y, max_y = 80, self.game.SCREENHEIGHT - 80
        self.rect.x = random.randint(min_x, max_x)
        self.rect.y = random.randint(min_y, max_y)
        self.image_mask = pygame.mask.from_surface(self.image)
        self.sugarcube_value = value
        # self.currency = 0
        

    def update(self):
        pass

    def collect(self, player):
        self.game.current_currency += self.sugarcube_value
        print(f"Sugarcubes: {self.game.current_currency}")
        self.kill()   # remove sprite

    def render(self, display):
        display.blit(self.image, self.rect)


    