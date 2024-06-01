import pygame

class Settings:
    def __init__(self):
        # Initialize player stats
        self.player_health = 250
        self.player_attack = 20
        self.player_speed = 400

        # Initialize game progress
        self.levels_unlocked_list = [False, False, False, False, False]  # Five levels
        # self.level_unlock = False

        # Initialize sugarcube values
        self.sugarcube_value = 10
        self.main_sugarcube_value = 50

        # Initialize first win flags
        self.first_win1 = False
        self.first_win2 = False
        self.first_win3 = False
        self.first_win4 = False
        self.first_win5 = False


    def reset_sugarcube_value(self):
        if any([self.first_win1, self.first_win2, self.first_win3, self.first_win4, self.first_win5]):
            self.sugarcube_value = 10

    def set_first_win(self, level):
        if level == 1:
            self.first_win1 = True
        elif level == 2:
            self.first_win2 = True
        elif level == 3:
            self.first_win3 = True
        elif level == 4:
            self.first_win4 = True
        elif level == 5:
            self.first_win5 = True

    def upgrade_player(self, health=None, speed=None, attack=None):
        if health:
            self.player_health += health
        if speed:
            self.player_speed += speed
        if attack:
            self.player_attack += attack

    def unlock_level(self, level):
        if self.level_unlock:
            self.levels_unlocked_list[level - 1] = True