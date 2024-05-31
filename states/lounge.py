import pygame
from parent_classes.state import *
from parent_classes.dialogue import *
from states.circus import *
from states.level_choose import *
from torres import *
from stanley import *
from camera import *

class Lounge(State, Dialogue):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        # self.player = Player(self.game, 300, 150)
        self.player = Player(self.game, 300, 150)
        self.stan = Stanley(self.game)
        self.camera = LoungeCamera(self.game)
        self.circus = Circus(self.game)
        self.level = Level_Options(self.game)
        self.interact = pygame.sprite.Group()
        self.interact.add(self.player)
        self.camera.add(self.player, self.stan)
        self.button_e = self.game.E_button
        self.level_button = self.game.E_button
        self.button_rect = self.button_e.get_rect()
        self.lvlbtn_rect = self.level_button.get_rect()
        # self.offset = pygame.math.Vector2((0,0))

    def update(self, deltatime, player_action):
        player_action["up"], player_action["down"] = False, False
        player_action["ultimate"], player_action["attack"], player_action["defend"],= False, False, False
        self.stan.update_lounge(deltatime, self.player, player_action)
        self.stan.rect.x, self.stan.rect.y = 1300,140
        self.player.update(deltatime,player_action)

        
        self.button_update(player_action, self.circus, self.button_rect, self.camera.circus_rect, 130, 300, 30, 40)
        self.button_update(player_action, self.level, self.lvlbtn_rect, self.camera.level_rect, 1010, 1020, 100, 40)

    def render(self, display):
        self.camera.custom_draw(display, self.player)        
        self.button_render(display, 130, 300, self.button_e, self.button_rect)
        self.button_render(display, 1010, 1020, self.level_button, self.lvlbtn_rect)

        display.blit(self.game.sugarcube_image, (10, 10))
        self.game.draw_text(display, f"{int(self.game.current_currency)}", (30,30,30), 40, 5, 35)


    def button_render(self, display, x, y, button, button_rect):
        if self.camera.offset.x >= x and self.camera.offset.x <= y:
            display.blit(button, button_rect)
        # if target.rect.colliderect(self.level_rect):
        #     pass
    
    def button_update(self, player_action, state, rect, offrect, x, y, rectx, recty):
        if self.camera.offset.x >= x and self.camera.offset.x <= y:
            rect.x, rect.y = offrect.x + rectx, offrect.y - recty
            if player_action["E"]:
                player_action["transition"] = True
                
            if player_action["transition"]:
                player_action["right"], player_action["left"] = False, False

            if self.game.alpha == 255:
                new_state = state
                new_state.enter_state()
                player_action["transition"] = False

