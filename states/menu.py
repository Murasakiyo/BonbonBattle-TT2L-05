import pygame
from parent_classes.state import State
from states.level_1 import First_Stage
from states.level_2 import Sec_Stage
from states.level_4 import Quad_Stage


class MainMenu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        self.start_button = pygame.image.load("sprites/start_button.png").convert_alpha()
        self.start_button_hover = pygame.image.load("sprites/start_button_hover.png").convert_alpha()
        self.current_start = self.start_button
        self.rect_START = self.start_button.get_rect(width= 200, height=150)
        self.rect_START.x, self.rect_START.y = 600, 465
        self.set_button = pygame.image.load("sprites/set_button.png").convert_alpha()
        self.set_button_hover = pygame.image.load("sprites/set_button_hover.png").convert_alpha()
        self.rect_SET = self.set_button.get_rect(width=100, height=100)
        self.rect_SET.x, self.rect_SET.y = 900, 465
        self.current_set = self.set_button
        self.click = False
        self.next = False


    def update(self, deltatime, player_action):
        self.mouse = pygame.mouse.get_pos()
        if self.rect_START.collidepoint(self.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.next = True
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.next = False
                self.click = False
        

        if self.next:
            player_action["transition"] = True

        if self.game.alpha == 255:
            new_state = Sec_Stage(self.game)
            new_state.enter_state()
            player_action["transition"] =  False
            

    
    def render(self, display):
        display.blit(pygame.image.load("sprites/main_screen.bmp").convert(), (0,0))
        if self.rect_START.collidepoint(self.mouse):
            self.current_start = self.start_button_hover
        else:
            self.current_start = self.start_button
        if self.rect_SET.collidepoint(self.mouse):
            self.current_set = self.set_button_hover
        else:
            self.current_set = self.set_button
        display.blit(self.current_start, (self.rect_START.x, self.rect_START.y))
        display.blit(self.current_set, (self.rect_SET.x, self.rect_SET.y))