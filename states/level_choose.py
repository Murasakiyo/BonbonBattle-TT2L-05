import pygame
from parent_classes.state import *
from states.level_1 import First_Stage
from states.level_2 import Sec_Stage
from states.level_4 import Quad_Stage

class Level_Options(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        self.backgrounds()
        self.buttons()
        self.make_button()
        self.current_time = 0
        self.first_level = First_Stage(self.game)
        self.second_level = Sec_Stage(self.game)
        self.fourth_level= Quad_Stage(self.game)
        self.current_level1 = self.lvl1
        self.current_level2 = self.lvl2
        self.current_level3 = self.lvl3
        self.current_level4 = self.lvl4
        self.current_level5 = self.lvl5
        self.current_background = self.level1
        self.show_bg = self.current_background
        self.alpha = 0

        self.menu_options = {0 :"lvl1", 1 : "lvl2", 2 :"lvl3", 3 : "lvl4",  4 : "lvl5"}
        self.index = 0


    def update(self, deltatime, player_action):
        self.show_bg = self.current_background
        self.bg_transition(player_action)
        self.update_keys(player_action, deltatime)
        if self.menu_options[self.index] == "lvl1": 
            self.current_level1 = self.lvl1_hover
            self.current_background = self.level1
            new_state = self.first_level
        else:
            self.current_level1 = self.lvl1
        if self.menu_options[self.index] == "lvl2": 
            self.current_level2 = self.lvl2_hover
            self.current_background = self.level2
            new_state = self.second_level
        else:
            self.current_level2 = self.lvl2
        if self.menu_options[self.index] == "lvl3": 
            self.current_level3 = self.lvl3_hover
            self.current_background = self.level3
        else:
            self.current_level3 = self.lvl3
        if self.menu_options[self.index] == "lvl4": 
            self.current_level4 = self.lvl4_hover
            self.current_background = self.level4
            new_state = self.fourth_level
        else:
            self.current_level4 = self.lvl4
        if self.menu_options[self.index] == "lvl5": 
            self.current_level5 = self.lvl5_hover
            self.current_background = self.level5
        else:
            self.current_level5 = self.lvl5

        if player_action["go"]:
            player_action["transition"] = True

        if self.game.alpha == 255:
            new_state.enter_state()
            self.game.reset_keys()

            

    def render(self, display):
        # display.fill((0,0,0))
        display.blit(self.show_bg, (0,0))
        display.blit(self.current_level1, (self.button1.x, self.button1.y))
        display.blit(self.current_level2, (self.button1.x + 200, self.button1.y))
        display.blit(self.current_level3, (self.button1.x + 400, self.button1.y))
        display.blit(self.current_level4, (self.button1.x + 600, self.button1.y))
        display.blit(self.current_level5, (self.button1.x + 800, self.button1.y))


    def update_keys(self, player_action, deltatime):
        self.current_time += deltatime
        if self.current_time > 0.15:
            if player_action["right"]:
                self.index = (self.index + 1) % len(self.menu_options)
            elif player_action["left"]:
                self.index = (self.index - 1) % len(self.menu_options)
            self.current_time = 0

    def bg_transition(self, player_action):
        if player_action["right"] or player_action["left"]:
            self.alpha = 0
        if self.alpha != 255:
            self.alpha = min(self.alpha + 10, 255)
        self.show_bg.set_alpha(self.alpha)
        pygame.display.flip()



    def backgrounds(self):
        self.level1 = pygame.image.load("sprites/backgrounds/level1_start.png").convert()
        self.level2 = pygame.image.load("sprites/backgrounds/level2_start.png").convert()
        self.level3 = pygame.image.load("sprites/backgrounds/level3_start.png").convert()
        self.level4 = pygame.image.load("sprites/backgrounds/level4_start.png").convert()
        self.level5 = pygame.image.load("sprites/backgrounds/level5_start.png").convert()

        
    def buttons(self):
        self.lvl1 = pygame.image.load("sprites/buttons/lvl1.png").convert_alpha()
        self.lvl2 = pygame.image.load("sprites/buttons/lvl2.png").convert_alpha()
        self.lvl3 = pygame.image.load("sprites/buttons/lvl3.png").convert_alpha()
        self.lvl4 = pygame.image.load("sprites/buttons/lvl4.png").convert_alpha()
        self.lvl5 = pygame.image.load("sprites/buttons/lvl5.png").convert_alpha()

        self.lvl1_hover = pygame.image.load("sprites/buttons/lvl1_hover.png").convert_alpha()
        self.lvl2_hover = pygame.image.load("sprites/buttons/lvl2_hover.png").convert_alpha()
        self.lvl3_hover = pygame.image.load("sprites/buttons/lvl3_hover.png").convert_alpha()
        self.lvl4_hover = pygame.image.load("sprites/buttons/lvl4_hover.png").convert_alpha()
        self.lvl5_hover = pygame.image.load("sprites/buttons/lvl5_hover.png").convert_alpha()

    def make_button(self):
        self.button1 = self.lvl1.get_rect(width= 100, height=100)
        self.button2 = self.lvl2.get_rect(width= 300, height=300)
        self.button3 = self.lvl3.get_rect(width= 300, height=300)
        self.button4 = self.lvl4.get_rect(width= 300, height=300)
        self.button5 = self.lvl5.get_rect(width= 300, height=300)

        self.button1.x, self.button1.y = 75,225
