import pygame

class Vanilla(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        image = pygame.image.load('sprites/vanilla.png').convert_alpha()
        self.image = pygame.transform.scale(image, (64,80)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 700, 100
        self.image_mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

    def render(self, display):
        display.blit(self.image, self.rect)
        # pygame.draw.rect(display, (255,255,255), self.rect, 2)

class Float(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        image = pygame.image.load('sprites/float.png').convert_alpha()
        self.image = pygame.transform.scale(image, (64,80)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 800, 300
        self.image_mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

    def render(self, display):
        display.blit(self.image, self.rect)
        # pygame.draw.rect(display, (255,255,255), self.rect, 2)


class Strawb(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        image = pygame.image.load('sprites/strawberry.png').convert_alpha()
        self.image = pygame.transform.scale(image, (64,80)).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = 700, 400
        self.image_mask = pygame.mask.from_surface(self.image)

    def update(self):
        pass

    def render(self, display):
        display.blit(self.image, self.rect)
        # pygame.draw.rect(display, (255,255,255), self.rect, 2)