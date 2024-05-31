import pygame
from parent_classes.state import *
from parent_classes.dialogue import *
from torres import *
from krie import *

class Circus(State, Dialogue):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.player = Player(self.game, 300, 320)
        self.krie = Krie(self.game)
        self.camera = CameraGroup(self.game)
        self.camera.add(self.player)
        self.door_rect = pygame.Rect(170,300,100,200)
        self.button_e = self.game.E_button
        self.button_rect = self.button_e.get_rect()
        self.button_rect.x, self.button_rect.y = self.door_rect.centerx - 20, self.door_rect.y - 60



    def update(self, deltatime, player_action):
        player_action["up"], player_action["down"] = False, False
        player_action["ultimate"], player_action["attack"], player_action["defend"],= False, False, False
        self.player.update(deltatime,player_action)

        self.krie.update_circus(deltatime, self.player, player_action)
        self.krie.rect.x, self.krie.rect.y = 800, 250

        if self.player.rect.colliderect(self.door_rect):
            if player_action["E"]:
                player_action["transition"] = True

            if player_action["transition"]:
                player_action["right"], player_action["left"] = False, False

            if self.game.alpha == 255:
                self.exit_state(-1)
                player_action["transition"] = False

    def render(self, display):
        display.blit(self.game.circus, (0, -100))
        self.krie.render(display)
        display.blit(self.game.shop, (0, -100))
        self.camera.custom_draw(display)
        if self.player.rect.colliderect(self.door_rect):
            display.blit(self.button_e, self.button_rect)

        display.blit(self.game.sugarcube_image, (10, 10))
        self.game.draw_text(display, f"{int(self.game.current_currency)}", (30,30,30), 40, 10, 35)

        
