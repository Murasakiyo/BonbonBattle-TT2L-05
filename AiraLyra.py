import pygame

class Aira(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.posx, self.posy = 50, 300
        self.rect = pygame.Rect(self.posx, self.posy, 40, 40)





class Lyra(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.posx, self.posy = 1050, 300
        self.rect = pygame.Rect(self.posx, self.posy, 40, 40)
