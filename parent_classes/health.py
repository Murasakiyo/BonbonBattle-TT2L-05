import pygame

class Health():
    def __init__(self, game):
        self.game = game


    def load_health_bar(self):
        self.health_rect = pygame.Rect(10, 10, 250, 40)
        self.health_bar = pygame.Rect(10, 10, self.player.healthpoints, 40)

    def health_update(self):
        if self.player.healthpoints <= 0:
            self.player.healthpoints = 0
        self.health_bar = pygame.Rect(10, 10, self.player.healthpoints, 40)

    def health_render(self, display):
        pygame.draw.rect(display, "black", self.health_rect)
        pygame.draw.rect(display, "green", self.health_bar)
        