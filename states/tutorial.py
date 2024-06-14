import pygame
from parent_classes.state import *


class Tutorial(State):
    def __init__(self, game, player_x, player_y):
        super().__init__(game)
        self.game = game
        self.textbox = pygame.image.load("sprites/tutorial_box.png").convert_alpha()
        self.big_txtbox = pygame.image.load("sprites/big_box.png").convert_alpha()
        self.rect = self.textbox.get_rect(x = player_x + 70, y =player_y - 80)
        self.bigrect = self.big_txtbox.get_rect(x = player_x + 70, y =player_y - 80)
        self.color = (0,0,14)
        self.tutokeys = self.game.open_txt("tutorial_keys.txt")
        self.x, self.y = self.rect.topleft
        self.tuto_time, self.long_tuto_time =0, 0
        self.tuto5_counter =0
        # self.current_text = self.tutokeys


    def update(self, deltatime, player_action):

        # WASD Keys
        if self.game.tutorial_counter == 0:
            self.tuto_time += deltatime
            if self.tuto_time > 1:
                if player_action["left"] or player_action["right"] or player_action["up"] or player_action["down"]:
                    self.exit_state(-1)
                    self.game.tutorial_counter += 1
                    self.tuto_time = 0

        # Attack Key
        if self.game.tutorial_counter == 1:
            self.tuto_time += deltatime
            if self.tuto_time > 0.2:
                if player_action["attack"]:
                    self.exit_state(-1)
                    self.game.tutorial_counter += 1
                    self.tuto_time = 0

        # Defend Key
        if self.game.tutorial_counter == 2:
            self.tuto_time += deltatime
            if self.tuto_time > 0.2:
                if player_action["defend"]:
                    self.exit_state(-1)
                    self.game.tutorial_counter += 1
                    self.tuto_time = 0

        # Ultimate Key
        if self.game.tutorial_counter == 3:
            self.tuto_time += deltatime
            if player_action["ultimate"]:
                self.exit_state(-1)
                self.game.tutorial_counter += 1
                self.tuto_time = 0

        # Grab confection 
        if self.game.tutorial_counter == 4:
            self.tuto_time += deltatime
            if self.tuto_time > 1:
                if self.game.convo_keys["all_key"]:
                    self.exit_state(-1)
                    self.game.tutorial_counter += 1
                    self.tuto_time = 0

        # Support Dolls explanation
        if self.game.tutorial_counter == 5:
            self.tuto_time += deltatime
            if self.tuto_time > 1:
                self.long_tuto_time += deltatime
                if self.long_tuto_time > 1:
                    if self.game.convo_keys["all_key"]:
                        if not(self.tuto5_counter) == 3:
                            self.tuto5_counter += 1
                            self.long_tuto_time = 0
                    if self.tuto5_counter == 3:
                        self.exit_state(-1)
                        self.game.tutorial_counter += 1
                        self.long_tuto_time = 0
                        self.game.convo_keys["all_key"] = False
        
        if self.game.tutorial_counter == 6:
            self.tuto_time += deltatime
            if self.tuto_time > 1:
                if self.game.convo_keys["all_key"]:
                    self.exit_state(-1)
                    self.game.tutorial_counter += 1
                    self.game.tutorial = False
                    self.game.save_data()
                    self.tuto_time = 0

    def render(self, display):
        if self.game.tutorial_counter == 0 or self.game.tutorial_counter == 1 or self.game.tutorial_counter == 2 or self.game.tutorial_counter == 4 :
            display.blit(self.textbox, self.rect)
        if self.game.tutorial_counter == 3 or self.game.tutorial_counter == 6:
            display.blit(self.big_txtbox, self.bigrect)
        # WASD Keys
        if self.game.tutorial_counter == 0:
            for i in range(3):
                self.game.draw_text(display, self.tutokeys[i], True, self.color, self.x + 25, self.y + 20 + (i * 30), 17)
        # Attack Key
        if self.game.tutorial_counter == 1:
            for i in range(3,6):
                self.game.draw_text(display, self.tutokeys[i], True, self.color, self.x + 15, self.y + 20 + ((i-3) * 30), 17)
        # Defend Key
        if self.game.tutorial_counter == 2:
            for i in range(6,8):
                self.game.draw_text(display, self.tutokeys[i], True, self.color, self.x + 15, self.y + 20 + ((i-6) * 30), 17)
        # Ultimate Key
        if self.game.tutorial_counter == 3:
            display.blit(self.big_txtbox, self.bigrect)
            for i in range(9,12):
                self.game.draw_text(display, self.tutokeys[i], True, self.color, self.x + 15, self.y + 20 + ((i-9) * 30), 17)
        # Grab confection 
        if self.game.tutorial_counter == 4:
            for i in range(13,16):
                self.game.draw_text(display, self.tutokeys[i], True, self.color, self.x + 15, self.y + 20 + ((i-13) * 25), 17)
        # Support Dolls explanation
        if self.game.tutorial_counter == 5:
            self.bigrect.x, self.bigrect.y = 300, 200
            self.x, self.y = self.bigrect.topleft
            display.blit(self.big_txtbox, self.bigrect)
            if self.tuto5_counter == 0:
                display.blit(self.big_txtbox, self.bigrect)
                for i in range(17,21):
                    self.game.draw_text(display, self.tutokeys[i], True, self.color, self.x + 15, self.y + 20 + ((i-17) * 30), 17)
            if self.tuto5_counter == 1:
                display.blit(self.big_txtbox, self.bigrect)
                for i in range(22,26):
                    self.game.draw_text(display, self.tutokeys[i], True, self.color, self.x + 15, self.y + 20 + ((i-22) * 30), 17)
            if self.tuto5_counter == 2:
                display.blit(self.big_txtbox, self.bigrect)
                for i in range(27,32):
                    self.game.draw_text(display, self.tutokeys[i], True, self.color, self.x + 15, self.y + 20 + ((i-27) * 30), 17)
        if self.game.tutorial_counter == 6:
            for i in range(32,35):
                self.game.draw_text(display, self.tutokeys[i], True, self.color, self.x + 15, self.y + 20 + ((i-32) * 25), 17)