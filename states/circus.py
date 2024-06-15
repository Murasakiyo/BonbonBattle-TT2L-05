import pygame
from parent_classes.state import *
from torres import *
from krie import *
from states.upgrade import *
from krie_dialogue import *

class Circus(State):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.player = Player(self.game, 300, 320)
        self.talk = Krie_Dialogue(self.game)
        self.init_talk = False
        self.krie = Krie(self.game)
        self.chara_upgrade = Upgrade(self.game)
        self.krie.rect.x, self.krie.rect.y = 800, 250
        self.camera = CameraGroup(self.game)
        self.camera.add(self.player)
        self.door_rect = pygame.Rect(170,300,100,200)
        self.button_e = self.game.E_button
        self.button_shop = self.game.E_button
        self.button_rect = self.button_e.get_rect()
        self.shop_rect = self.button_shop.get_rect()
        self.button_rect.x, self.button_rect.y = self.door_rect.centerx - 20, self.door_rect.y - 60
        self.shop_rect.x, self.shop_rect.y = self.krie.rect.centerx - 35, self.krie.rect.y - 40
        self.black = False
        self.finish = False


    def update(self, deltatime, player_action):
        self.game.play_circus_music = True
        player_action["up"], player_action["down"] = False, False
        player_action["ultimate"], player_action["attack"], player_action["defend"],= False, False, False
        if not(self.init_talk):
            self.player.update(deltatime,player_action)

        self.krie.update_circus(deltatime, self.player, player_action)


        # Collide with exit
        if self.player.rect.colliderect(self.door_rect):
            if player_action["E"]:
                player_action["transition"] = True

            if player_action["transition"]:
                player_action["right"], player_action["left"] = False, False

            if self.game.alpha == 255:
                self.exit_state(-1)
                player_action["transition"] = False

        # Collide with Krie
        if self.player.rect.colliderect(self.krie.rect):
            if player_action["E"]:
                if not(self.game.settings.krie_intro):
                    self.init_talk = True
                else:
                    new_state = self.chara_upgrade
                    self.game.game_canvas.blit(self.game.black, (0, 0))
                    new_state.enter_state()
                
        if self.init_talk:
            self.talk.update(deltatime, player_action)
            self.finish = self.talk.end_convo()

        if self.finish:
            self.init_talk = False
            self.game.settings.krie_intro = True

    def render(self, display):
        display.blit(self.game.circus, (0, -100))
        self.krie.render(display)
        display.blit(self.game.shop, (0, -100))
        self.camera.custom_draw(display)
        if self.player.rect.colliderect(self.door_rect):
            display.blit(self.button_e, self.button_rect)
        
        if self.player.rect.colliderect(self.krie.rect):
            display.blit(self.button_shop, self.shop_rect)

        display.blit(self.game.sugarcube_image, (10, 10))
        self.game.draw_text(display, f"{int(self.game.current_currency)}", True, (30,30,30), 40, 10, 35)

        if self.init_talk:
            self.talk.render(display)



        
