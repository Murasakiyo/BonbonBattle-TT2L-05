import pygame
from parent_classes.state import State
from states.first_cutscene import Story
from states.game_set import Game_Settings
from states.lounge import Lounge
from settings import Settings


class MainMenu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        self.sounds = self.game.sounds
        self.settings = Settings(self.game)
        self.start_button = pygame.image.load("sprites/start_button.png").convert_alpha()
        self.start_button_hover = pygame.image.load("sprites/start_button_hover.png").convert_alpha()
        self.current_start = self.start_button
        self.rect_START = self.start_button.get_rect(width= 250, height=100)
        self.rect_START.x, self.rect_START.y = 600, 465
        self.set_button = pygame.image.load("sprites/set_button.png").convert_alpha()
        self.set_button_hover = pygame.image.load("sprites/set_button_hover.png").convert_alpha()
        self.rect_SET = self.set_button.get_rect(width=100, height=100)
        self.rect_SET.x, self.rect_SET.y = 900, 465
        self.current_set = self.set_button
        self.click = False
        self.next = False


    def update(self, deltatime, player_action):
        if self.rect_START.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.sounds.start_game.play()
                self.next = True
                self.click = True
                player_action["start"] = True
                
            if not pygame.mouse.get_pressed()[0]:
                self.click = False

        if self.rect_SET.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.click = True
                new_state = Game_Settings(self.game)
                new_state.enter_state()
            if not pygame.mouse.get_pressed()[0]:
                self.click = False
        
        if self.next:
            player_action["transition"] = True

        if self.game.alpha >= 240:
            self.game.draw_text(self.game.screen, "Loading...", True, "white", 400, 250, 80)
        if self.game.alpha == 255:
            if self.game.skip_cutscenes:
                new_state = Lounge(self.game)
            else:
                new_state = Story(self.game)
            new_state.enter_state()
            player_action["transition"] =  False
            self.next = False
            

    def render(self, display):
        display.blit(pygame.image.load("sprites/main_screen.bmp").convert(), (0,0))
        self.hover_button(display, self.rect_START, self.current_start, self.start_button, self.start_button_hover)
        self.hover_button(display, self.rect_SET, self.current_set, self.set_button, self.set_button_hover)
       
