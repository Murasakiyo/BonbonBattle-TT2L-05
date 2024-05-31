import pygame
from parent_classes.state import *
from states.level_1 import First_Stage
from states.level_2 import Sec_Stage
from states.level_3 import Trio_Stage
from states.level_4 import Quad_Stage
from states.level_5 import Penta_Stage

class Level_Options(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        self.enter = pygame.image.load("sprites/buttons/enter.png").convert_alpha()
        self.backgrounds()
        self.current_time = 0
        self.first_level = First_Stage(self.game)
        self.second_level = Sec_Stage(self.game)
        self.third_level = Trio_Stage(self.game)
        self.fourth_level= Quad_Stage(self.game)
        self.fifth_level = Penta_Stage(self.game)
        self.current_level1 = self.game.lvl1
        self.current_level2 = self.game.lvl2
        self.current_level3 = self.game.lvl3
        self.current_level4 = self.game.lvl4
        self.current_level5 = self.game.lvl5
        self.current_background = self.level1
        self.show_bg = self.current_background
        self.alpha = 0

        self.menu_options = {0 :"lvl1", 1 : "lvl2", 2 :"lvl3", 3 : "lvl4",  4 : "lvl5"}
        self.index = 0

        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 40)
        sugarcube_image = pygame.image.load("sprites/sugarcube.png").convert_alpha()
        self.sugarcube_image = pygame.transform.scale(sugarcube_image, (25,25)).convert_alpha()


    def update(self, deltatime, player_action):

        self.show_bg = self.current_background
        self.bg_transition(player_action)
        self.update_keys(player_action, deltatime)
        if self.menu_options[self.index] == "lvl1": 
            self.current_level1 = self.game.lvl1_hover
            self.current_background = self.level1
            new_state = self.first_level
        else:
            self.current_level1 = self.game.lvl1
        if self.menu_options[self.index] == "lvl2": 
            self.current_level2 = self.game.lvl2_hover
            self.current_background = self.level2
            new_state = self.second_level
        else:
            self.current_level2 = self.game.lvl2
        if self.menu_options[self.index] == "lvl3": 
            self.current_level3 = self.game.lvl3_hover
            self.current_background = self.level3
            new_state = self.third_level
        else:
            self.current_level3 = self.game.lvl3
        if self.menu_options[self.index] == "lvl4": 
            self.current_level4 = self.game.lvl4_hover
            self.current_background = self.level4
            new_state = self.fourth_level
        else:
            self.current_level4 = self.game.lvl4
        if self.menu_options[self.index] == "lvl5": 
            self.current_level5 = self.game.lvl5_hover
            self.current_background = self.level5
            new_state = self.fifth_level
        else:
            self.current_level5 = self.game.lvl5

        if player_action["go"]:
            player_action["transition"] = True

        if not(self.game.init_reset):
            if self.game.alpha == 255:
                new_state.enter_state()
                self.start = False
                self.game.reset_keys()
        else:
            player_action["transition"] = False
            self.game.init_reset = False

        
            

    def render(self, display):
        # display.fill((0,0,0))
        display.blit(self.show_bg, (0,0))
        display.blit(self.current_level1, (self.game.button1.x, self.game.button1.y))
        display.blit(self.current_level2, (self.game.button1.x + 200, self.game.button1.y))
        display.blit(self.current_level3, (self.game.button1.x + 400, self.game.button1.y))
        display.blit(self.current_level4, (self.game.button1.x + 600, self.game.button1.y))
        display.blit(self.current_level5, (self.game.button1.x + 800, self.game.button1.y))
        if not(self.game.player_action["transition"]):
            display.blit(self.enter, (900, 500))
        currency_text = self.font.render(f"{int(self.game.current_currency)}", True, self.text_color)
        display.blit(self.sugarcube_image, (10, 10))
        display.blit(currency_text, (40, 10))


    def update_keys(self, player_action, deltatime):
        self.current_time += deltatime
        if self.current_time > 0.13:
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

    
