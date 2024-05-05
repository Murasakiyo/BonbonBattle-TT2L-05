import pygame

class Health():
    def __init__(self, game):
        self.game = game
        self.health_rect = pygame.Rect(10, 10, 250, 40)
        self.healthpoints = 250
        self.health_bar = pygame.Rect(10, 10, self.healthpoints, 40)


    def update(self, deltatime, take_damage):

        # elif self.healthpoints <= 0:
        #     self.healthpoints += 250

        self.health_bar = pygame.Rect(10, 10, self.healthpoints, 40)



    def render(self, display):
        pygame.draw.rect(display, "black", self.health_rect)
        pygame.draw.rect(display, "green", self.health_bar)