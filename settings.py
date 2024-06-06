import pygame

class Settings:
    def __init__(self):
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


    def reset_sugarcube_value(self):
        if any([self.first_win1, self.first_win2, self.first_win3, self.first_win4, self.first_win5]):
            self.sugarcube_value = 10


