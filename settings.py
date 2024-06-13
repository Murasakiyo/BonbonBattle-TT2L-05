import pygame

class Settings:
    def __init__(self, game):
        self.game = game

        # Initialize player stats
        self.current_healthpoints = 250
        self.current_attackpoints = 3
        self.current_speed = 400

        # Initialize sugarcube values
        self.sugarcube_value = 10
        self.first_sugarcube_value = 50

        # Initialize first win flags
        self.first_win1 = False
        self.first_win2 = False
        self.first_win3 = False
        self.first_win4 = False
        self.first_win5 = False
        self.krie_intro = False

    
    def gamereset_value(self):
        self.game.current_currency = 0
        self.game.current_level = 0
        self.game.skip_cutscenes = False
        self.game.settings.current_healthpoints = 250
        self.game.settings.current_attackpoints = 3
        self.game.settings.current_speed = 400
        self.krie_intro = False
        


