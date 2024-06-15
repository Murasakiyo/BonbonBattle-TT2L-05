import pygame

class Settings:
    def __init__(self, game):
        self.game = game

        # Initialize player stats
        self.current_healthpoints = 250
        self.current_attackpoints = 3
        self.current_speed = 400

        # Initialize upgrade level
        self.current_atk_level = 0
        self.current_HP_level = 0
        self.current_spd_level = 0


        # Initialize sugarcube values
        self.sugarcube_value = 15
        self.first_sugarcube_value = 50

        # Initialize first win flags
        self.first_win1 = False
        self.first_win2 = False
        self.first_win3 = False
        self.first_win4 = False
        self.first_win5 = False

        # Initialize npc's dialogues
        self.krie_intro = False
        self.stan_dialogue_counter = 0


    def gamereset_value(self):
        self.game.current_currency = 1000
        self.game.current_level = 0
        self.game.skip_cutscenes = True
        self.game.settings.current_healthpoints = 250
        self.game.settings.current_attackpoints = 3
        self.game.settings.current_speed = 400
        self.game.tutorial = True
        self.game.settings.krie_intro = False
        self.game.settings.stan_dialogue_counter = 0
        self.game.settings.current_atk_level = 0
        self.game.settings.current_HP_level = 0
        self.game.settings.current_spd_level = 0
        self.game.settings.first_win5 = False
        


