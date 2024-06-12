import pygame

class Sounds():
    def __init__(self, game):
        self.game = game
        self.start_game = pygame.mixer.Sound("sounds/start.wav")
        self.upgrade_clicked = pygame.mixer.Sound("sounds/upgrade.wav")
        self.no_upgrade = pygame.mixer.Sound("sounds/no_upgrade.wav")
        self.enemies_death = pygame.mixer.Sound("sounds/enemies_death.wav")
        self.collect_sugarcube = pygame.mixer.Sound("sounds/sugarcubes.wav")
        self.circus_bgmusic = pygame.mixer.Sound("sounds/lounge.wav")
        self.lvl1_bgmusic = pygame.mixer.Sound("sounds/level1.wav")
