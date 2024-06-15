import pygame
from parent_classes.state import *
from settings import Settings


class Game_Settings(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.settings = Settings(self.game)
        self.assets = {
            "settings": pygame.image.load("sprites/settings_screen.png").convert_alpha(),
            "bg" : pygame.image.load("sprites/lounge.bmp").convert(),
            "reset_bttn" : self.game.button,
            "back_bttn" : self.game.button
        }
        self.set_rect = self.assets["settings"].get_rect(width= 600, height=440)
        self.set_rect.x, self.set_rect.y = 250,75
        self.reset_rect = self.assets["reset_bttn"].get_rect(x= 330, y= 400)
        self.back_rect = self.assets["back_bttn"].get_rect(x= 600, y= 400)
        self.current_reset = self.assets["reset_bttn"]
        self.current_back = self.assets["back_bttn"]
        self.alpha = 0
        self.assets["bg"].set_alpha(self.alpha)

        # Warning texts
        self.reset_warn = "RESET PROGRESS?"
        self.warning = "Warning: This action cannot be undone"
        self.warn_list = self.game.open_txt("reset_warning.txt")

        # Button variables
        self.last_warn = False
        self.reset = False
        self.back = False
        self.click = False
        self.init_transition = False

    def update(self, deltatime, player_action):
        # print(len(self.warn_list))
        self.bg_transition(player_action)

        if self.reset_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.reset = True
                self.click = True
                if self.last_warn:
                    self.game.reset_game = True
                    self.settings.gamereset_value()
                    self.exit_state(-1)
            if not pygame.mouse.get_pressed()[0]:
                self.reset = False
                self.click = False

        if self.back_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.back = True
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.back = False
                self.click = False

        if self.reset:
            self.last_warn = True

        if self.back:
            self.init_transition = True
        if self.alpha == 0:
            self.exit_state(-1)


    def render(self, display):
        display.blit(pygame.image.load("sprites/main_screen.bmp").convert(), (0,0))
        display.blit(self.assets["bg"], (-600,0))
        if self.alpha >= 230:
            display.blit(self.assets["settings"], (self.set_rect.x, self.set_rect.y))
            self.hover_button(display, self.reset_rect, self.current_reset, self.assets["reset_bttn"], self.game.button_hover)
            self.hover_button(display, self.back_rect, self.current_back, self.assets["back_bttn"], self.game.button_hover)
            self.game.draw_text(display, "YES", True, (0,0,14), 380, 405, 50)
            self.game.draw_text(display, "NO", True, (0,0,14), 665, 405, 50)
            self.game.draw_text(display, self.reset_warn, True, (0,0,14), 335, 100, 55)
            self.game.draw_text(display, self.warning, False, (225, 47,47), 310, 180, 25)
            for x in range(len(self.warn_list)):
                self.game.draw_text(display, self.warn_list[x], False, (0,0,14), 310, 210 + (x * 30), 25)
            if self.last_warn:
                self.game.draw_text(display, "Are you sure?", False, (225, 47,47), 350, 370, 20)
        
        
    def bg_transition(self, player_action):
        if not(self.init_transition):
            if self.alpha != 255:
                self.alpha = min(self.alpha + 10, 255)
        if self.init_transition:
            if self.alpha != 0:
                self.alpha = max(self.alpha - 10, 0)
        self.assets["bg"].set_alpha(self.alpha)
        pygame.display.flip()