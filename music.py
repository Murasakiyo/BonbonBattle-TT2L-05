import pygame

class Sounds():
    def __init__(self, game):
        self.game = game
        self.start_game = pygame.mixer.Sound("sounds/start.wav")
        self.upgrade_clicked = pygame.mixer.Sound("sounds/upgrade.wav")
        self.enemies_death = pygame.mixer.Sound("sounds/enemies_death.wav")
        self.collect_sugarcube = pygame.mixer.Sound("sounds/sugarcubes.wav")
        self.lounge_bgmusic = pygame.mixer.Sound("sounds/lounge2.wav")