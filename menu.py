import pygame
from state import State
from stage import Stage

class MainMenu(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.game = game
        self.rect_START = pygame.Rect(600,465,250,100)
        self.rect_SETTING = pygame.Rect(900,465,150,100)
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

        # if self.rect_SETTING.collidepoint(self.mouse):
        #     if pygame.mouse.get_pressed()[0] and not self.click:
        #         self.click = True
        #     if not pygame.mouse.get_pressed()[0]:
        #         self.click = False

        if self.next:
            player_action["transition"] = True

        if self.game.alpha == 255:
            new_state = Stage(self.game)
            new_state.enter_state()
            player_action["transition"] =  False
            

    
    def render(self, display):
        display.blit(pygame.image.load("sprites/main_screen.bmp").convert(), (0,0))
        pygame.draw.rect(display, (255,207,71), self.rect_START)
        pygame.draw.rect(display, (102,102,255), self.rect_SETTING)