import pygame

class Aira(pygame.Sprite.sprite):
    def __init__(self, game):
        self.game = game
        self.posx, self.posy = 50, 300
        self.rect = pygame.Rect(self.posx, self.posy, 40, 40)
        self.spin_posx, self.spin_posy = self.game.screen_rect.centerx, self.game.screen_rect.centery
        self.spin_rect = pygame.Rect(self.spin_posx, self.spin_posy, 40, 40)




class Lyra(pygame.Sprite.sprite):
    def __init__(self, game):
        self.game = game
        self.posx, self.posy = 1050, 300
        self.rect = pygame.Rect(self.posx, self.posy, 40, 40)
        self.spin_posx, self.spin_posy = self.game.screen_rect.centerx, self.game.screen_rect.centery
        self.spin_rect = pygame.Rect(self.spin_posx, self.spin_posy, 40, 40)