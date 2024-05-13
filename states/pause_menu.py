import pygame
from parent_classes.state import *

class Pause(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        self.pause_menu = pygame.image.load("sprites/pause_screen.png").convert_alpha()
        self.exit = pygame.image.load("sprites/buttons/exit.png").convert_alpha()
        self.resume = pygame.image.load("sprites/buttons/resume.png").convert_alpha()
        self.exit_hover = pygame.image.load("sprites/buttons/exit_hover.png").convert_alpha()
        self.resume_hover = pygame.image.load("sprites/buttons/resume_hover.png").convert_alpha()
        self.black = pygame.image.load("sprites/black.png").convert_alpha()
        self.black.set_alpha(30)
        self.pause_rect = self.pause_menu.get_rect(width= 600, height=440)
        self.exit_rect = self.exit.get_rect(width= 126, height=126)
        self.resume_rect = self.resume.get_rect(width= 126, height=126)
        self.pause_rect.x, self.pause_rect.y = 250,75
        self.exit_rect.x, self.exit_rect.y = self.pause_rect.x + 350, self.pause_rect.y + 250
        self.resume_rect.x, self.resume_rect.y = self.pause_rect.x + 130, self.pause_rect.y + 250
        self.current_exit = self.exit
        self.current_resume = self.resume
        self.click = False
        self.mouse = pygame.mouse.get_pos()
        self.exit_game, self.resume_game = False, False

    def update(self, deltatime, player_action):
        
        self.mouse = pygame.mouse.get_pos()

        if self.resume_rect.collidepoint(self.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.resume_game = True
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.resume_game = False
                self.click = False

        if self.resume_game:
            self.exit_state(-1)
            self.resume_game = False

        if self.exit_rect.collidepoint(self.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.exit_game = True
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.exit_game = False
                self.click = False

        if self.exit_game:
            self.exit_state(-2)
            self.exit_game = False
            player_action["transition"] = True
            self.game.defeat = False

        if self.game.alpha == 255:
            self.game.reset_game = True
            self.exit_state(-1)
            player_action["transition"] =  False
            

    def render(self, display):
        display.blit(self.black,(0,0))
        display.blit(self.pause_menu, (self.pause_rect.x, self.pause_rect.y))

        if self.exit_rect.collidepoint(self.mouse):
            self.current_exit = self.exit_hover
        else:
            self.current_exit = self.exit

        if self.resume_rect.collidepoint(self.mouse):
            self.current_resume = self.resume_hover
        else:
            self.current_resume = self.resume

        display.blit(self.current_exit, (self.exit_rect.x, self.exit_rect.y))
        display.blit(self.current_resume, (self.resume_rect.x, self.resume_rect.y ))
        
    