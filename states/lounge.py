import pygame
from parent_classes.state import *
from parent_classes.dialogue import *
from states.circus import *
from states.level_choose import *
from torres import *
from stanley import *
from camera import *
from music import Sounds

class Lounge(State, Dialogue):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        # self.player = Player(self.game, 300, 150)
        self.player = Player(self.game, 300, 150)
        self.stan = Stanley(self.game)
        self.conversation = Stan_Dialogue(self.game)
        self.camera = LoungeCamera(self.game)
        self.circus = Circus(self.game)
        self.level = Level_Options(self.game)
        self.interact = pygame.sprite.Group()



        self.interact.add(self.player)
        self.camera.add(self.player, self.stan)
        self.button_e = self.game.E_button
        self.level_button = self.game.E_button
        self.stan_button = self.game.E_button
        self.button_rect = self.button_e.get_rect()
        self.stan_rect = self.button_e.get_rect()
        self.lvlbtn_rect = self.level_button.get_rect()
        self.init_talk = False
        self.finish_talk = False

        # self.offset = pygame.math.Vector2((0,0))
        self.sounds = Sounds(self.game)
        self.sounds.lounge_bgmusic.play(-1)

    def update(self, deltatime, player_action):
        self.player.speed = 400
        # Restrict the players keys 
        player_action["up"], player_action["down"] = False, False
        player_action["ultimate"], player_action["attack"], player_action["defend"],= False, False, False
        self.stan.update_lounge(deltatime, self.player, player_action)
        self.stan.rect.x, self.stan.rect.y = 1300,140
        if not self.init_talk:
            self.player.update(deltatime,player_action)

        # Indicator Buttons hovering
        self.button_update(player_action, self.circus, self.button_rect, self.camera.circus_rect, 130, 300, 30, 40)
        self.button_update(player_action, self.level, self.lvlbtn_rect, self.camera.level_rect, 1010, 1020, 100, 40)
        if self.camera.offset.x >= 700 and self.camera.offset.x <= 950:
            self.stan_rect.x, self.stan_rect.y = self.camera.talk_rect.x + 110, self.camera.talk_rect.y  - 30
            if player_action["E"]:
                self.init_talk = True
        
        if self.init_talk:
            for actions in player_action:
                if not(player_action["next"]) and not(player_action["go"]):
                    player_action[actions] = False
            if self.conversation.counter == 0:
                self.conversation.update_firstconvo(deltatime, player_action)
                self.finish_talk = self.conversation.end_convo(self.conversation.convo)
                if self.finish_talk:
                    self.init_talk = False
                    self.finish_talk = False
            if self.conversation.counter > 0:
                self.finish_talk = self.conversation.update_options(deltatime, player_action)
                if self.finish_talk:
                    self.init_talk = False
                    self.finish_talk = False
                    self.conversation.reset_options()

        


    def render(self, display):
        self.camera.custom_draw(display, self.player)        
        self.button_render(display, 130, 300, self.button_e, self.button_rect)
        self.button_render(display, 1010, 1020, self.level_button, self.lvlbtn_rect)
        self.button_render(display, 700, 950, self.stan_button, self.stan_rect)

        display.blit(self.game.sugarcube_image, (10, 10))
        self.game.draw_text(display, f"{int(self.game.current_currency)}", True, (30,30,30), 40, 5, 35)

        if self.init_talk:
            self.conversation.render(display)


    def button_render(self, display, x, y, button, button_rect):
        if self.camera.offset.x >= x and self.camera.offset.x <= y:
            display.blit(button, button_rect)

    
    def button_update(self, player_action, state, rect, offrect, x, y, rectx, recty):
        if self.camera.offset.x >= x and self.camera.offset.x <= y:
            rect.x, rect.y = offrect.x + rectx, offrect.y - recty
            if player_action["E"]:
                player_action["transition"] = True
                self.sounds.lounge_bgmusic.stop()

            if player_action["transition"]:
                player_action["right"], player_action["left"] = False, False

            if self.game.alpha == 255:
                new_state = state
                new_state.enter_state()
                player_action["transition"] = False

class Stan_Dialogue():
    def __init__(self, game):
       super().__init__()
       self.game = game
       intro = self.game.open_txt("first_stan.txt")
       self.convo = Dialogue(self.game, "black", 24, intro)
       self.options = Answer(self.game, "I want to reset some part of my stats.", "Tell me about the court's abilities.", "Nevermind")
       self.current_image = self.game.asset["stanley"]["happy"]
       self.counter = 0
       self.choice = 0


    def update_firstconvo(self, deltatime, player_action):
            self.convo.dialogue_update(player_action)
            self.convo.finish()

    def update_options(self, deltatime, player_action):
        finish = False
        if not self.choice == 1 and not self.choice == 2 and not self.choice == 3:
            self.options.update(deltatime, player_action)
            self.choice = self.options.pick_choice(player_action)
        if self.choice == 1:
            finish = True
            return finish
        if self.choice == 2:
            finish = True
            return finish
        if self.choice == 3:
            finish = True
            return finish

    def reset_options(self):
        self.options.reset_choice()
        self.choice = 0

    def end_convo(self, talk):
        finish = False
        if talk.finish_convo:
            finish =True
        if finish:
            self.counter += 1
            return finish

    def render(self, display):
        if not(self.convo.finish_convo):
            if self.convo.activetext == 1:
                self.current_image = self.game.asset["stanley"]["happy"]
            if self.convo.activetext == 2:
                self.current_image = self.game.asset["torres"]["talk"]
            if self.convo.activetext == 4:
                self.current_image = self.game.asset["stanley"]["talk"]
            if self.convo.activetext == 10:
                self.current_image = self.game.asset["torres"]["miffed"]
            if self.convo.activetext == 14:
                self.current_image = self.game.asset["stanley"]["silly"]
            if self.convo.activetext == 16:
                self.current_image = self.game.asset["stanley"]["happy"]
            display.blit(self.current_image, (0,0))
            self.convo.draw_text(display)

        if self.counter > 0:
            self.options.render(display)

