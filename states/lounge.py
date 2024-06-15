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
        self.interact_timer = 0
        self.game.play_bg_music(self.game.sounds.circus_bgmusic)


    def update(self, deltatime, player_action):
        self.game.play_circus_music = True
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

            if self.game.settings.stan_dialogue_counter == 0:
                self.conversation.update_firstconvo(deltatime, player_action)
                self.finish_talk = self.conversation.end_convo(self.conversation.convo)
                if self.finish_talk:
                    self.init_talk = False
                    self.finish_talk = False

            if self.game.settings.stan_dialogue_counter > 0:
                self.finish_talk = self.conversation.update_options(deltatime, player_action, self.player)
                if self.finish_talk:
                    self.init_talk = False
                    self.conversation.reset_options(self.conversation.options)
                    self.conversation.reset_stats_reset()
                    self.conversation.reset_info()
                    self.finish_talk = False


        if not self.finish_talk:
            if self.conversation.stan_attack_anim:
                self.interact_timer += deltatime
                self.stan.attack = True
                if self.interact_timer > 0.8:
                    self.stan.attack = False
                    self.interact_timer = 0
                    self.conversation.stan_attack_anim = False

            
    def render(self, display):
        self.camera.custom_draw(display, self.player)        
        self.button_render(display, 130, 300, self.button_e, self.button_rect)
        self.button_render(display, 1010, 1020, self.level_button, self.lvlbtn_rect)
        if not self.init_talk:
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
       self.box = pygame.image.load("sprites/dialogue_box.png").convert_alpha()
       self.box_rect = self.box.get_rect(width = 700, height =200 )
       self.box_rect.x, self.box_rect.y = 210, 380


       intro = self.game.open_txt("first_stan.txt")
       self.convo = Dialogue(self.game, "black", 24, intro)
       self.options = Answer(self.game, "I want to reset some part of my stats.", "Tell me about the court's abilities.", "Nevermind", " ", True, False)
       self.current_image = self.game.asset["stanley"]["happy"]
       self.counter = 1
       self.choice, self.sec_choice, self.thi_choice = 0, 0, 0
       ask = ["Which stat would you like to reset?", " "]
       warn_reset = ["Through this reset, your stats will go back to", "its default value.", "But! it will be compensated with a little", "bit of sugarcube.", 
              "Are you sure you want to go through","with this?", " "]
       cheeky = ["Alright~ But don't say I didn't warn you so~", " "]
       self.choose_reset = Dialogue(self.game, "black", 24, ask)
       self.ask_for_reset = Dialogue(self.game, "black", 24, warn_reset)
       self.reset_confirm = Dialogue(self.game, "black", 24, cheeky)
       self.reset_choice = Answer(self.game, "Attack", "Health", "Speed", " ", True, False)
       self.confirm = Answer(self.game, "Yes", "Nevermind", " ", " ", False, False)
       self.reset_counter = 0
       self.attack, self.health, self.speed, self.finish = False, False, False, False
       self.stan_attack_anim = False

       self.support_doll_info = self.game.open_txt("support_doll.txt")
       ask_info = ["Which doll would you like to know more about?", " "]
       self.info_choice = 0
       self.ask_support = Dialogue(self.game, "black", 24, ask_info)
       self.choose_info = Answer(self.game, "The Court Jester", "The Queen", "The Pierrot Prince", "Nevermind", False, True)
       self.stan_info, self.krie_info, self.louie_info = False, False, False
       self.info_stan, self.info_krie, self.info_louie = 0,0,0
       self.info_counter, self.info_timer = 0 , 0

    def update_firstconvo(self, deltatime, player_action):
            self.convo.dialogue_update(player_action)
            self.convo.finish()

    def update_options(self, deltatime, player_action, player):
        finish = False
        if not self.choice == 1 and not self.choice == 2 and not self.choice == 3:
            self.options.update(deltatime, player_action)
            self.choice = self.options.pick_choice(player_action)
        if self.choice == 1:
            finish = self.stat_reset(deltatime, player_action, player)
            return finish
        if self.choice == 2:
            finish = self.ask_info(deltatime, player_action)
            return finish
        if self.choice == 3:
            finish = True
            return finish
        
    def stat_reset(self, deltatime, player_action, player):
        if not(self.choose_reset.finish_convo):
            self.choose_reset.dialogue_update(player_action)
            self.choose_reset.finish()
        else:
            self.reset_counter = 1

        if self.reset_counter == 1:
            if not self.sec_choice == 1 and not self.sec_choice == 2 and not self.sec_choice == 3:
                self.reset_choice.update(deltatime, player_action)
                self.sec_choice = self.reset_choice.pick_choice(player_action)
            if self.sec_choice == 1:
                self.attack = True
            if self.sec_choice == 2:
                self.health = True
            if self.sec_choice == 3:
                self.speed = True
            if self.sec_choice == 1 or self.sec_choice == 2 or self.sec_choice == 3:
                self.reset_counter = 2

        if self.reset_counter == 2:
            if not(self.ask_for_reset.finish_convo):
                self.ask_for_reset.dialogue_update(player_action)
                self.ask_for_reset.finish()
            else:
                self.reset_counter = 3

        if self.reset_counter == 3:
            if not self.thi_choice == 1 and not self.thi_choice == 2:
                self.confirm.update(deltatime, player_action)
                self.thi_choice = self.confirm.pick_choice(player_action)
            if self.thi_choice == 1:
                self.stan_attack_anim = True
                if self.attack:
                    current_set = self.game.settings.current_atk_level
                    self.game.settings.current_attackpoints = 3
                    player.attribute_update()
                    self.attack = False
                    self.reset_counter = 4
                if self.health:
                    current_set = self.game.settings.current_HP_level
                    self.game.settings.current_healthpoints = 250
                    player.attribute_update()
                    self.health = False
                    self.reset_counter = 4
                if self.speed:
                    current_set = self.game.settings.current_spd_level
                    self.game.settings.current_speed = 400
                    player.attribute_update()
                    self.speed = False
                    self.reset_counter = 4
                self.game.save_data()
            if self.thi_choice == 2:
                self.finish = True
                return self.finish
            if self.reset_counter == 4:
                if not(self.reset_confirm.finish_convo):
                    self.reset_confirm.dialogue_update(player_action)
                    self.reset_confirm.finish()
                else:
                    self.game.current_currency += (current_set * 50)
                    self.finish = True
                    return self.finish

    def ask_info(self, deltatime, player_action):
        if not(self.ask_support.finish_convo):
            self.ask_support.dialogue_update(player_action)
            self.ask_support.finish()
        else:
            self.info_counter = 1

        if self.info_counter == 1:
            if not self.info_choice == 1 and not self.info_choice == 2 and not self.info_choice == 3 and not self.info_choice == 4:
                self.choose_info.update(deltatime, player_action)
                self.info_choice = self.choose_info.pick_choice(player_action)
            if self.info_choice == 1:
                self.stan_info = True
                self.current_image = self.game.asset["stanley"]["happy"]
            if self.info_choice == 2:
                self.current_image = pygame.image.load("sprites/dialogue/krie/happy.png").convert_alpha()
                self.krie_info = True
            if self.info_choice == 3:
                self.louie_info = True
            if self.info_choice == 4:
                self.finish = True
                return self.finish
            if self.info_choice == 1 or self.info_choice == 2 or self.info_choice == 3:
                self.info_counter = 2
        
        if self.info_counter == 2:
            if self.stan_info:
                self.info_timer += deltatime
                if self.info_timer > 0.2:
                    if player_action["next"]:
                        self.info_stan += 1
                        self.info_timer = 0
                if self.info_stan > 1:
                    self.finish = True
                    return self.finish
            if self.krie_info:
                self.info_timer += deltatime
                if self.info_timer > 0.2:
                    if player_action["next"]:
                        self.info_krie += 1
                        self.info_timer = 0
                if self.info_krie > 1:
                    self.finish = True
                    return self.finish
            if self.louie_info:
                self.info_timer += deltatime
                if self.info_timer > 0.2:
                    if player_action["next"]:
                        self.info_louie += 1
                        self.info_timer = 0
                if self.info_louie > 1:
                    self.finish = True
                    return self.finish
                    
                
    def reset_stats_reset(self):
        self.choose_reset.reset_dialogue()
        self.ask_for_reset.reset_dialogue()
        self.reset_confirm.reset_dialogue()
        self.reset_choice.reset_options()
        self.confirm.reset_options()
        self.reset_counter = 0 
        self.attack, self.health, self.speed, self.finish = False, False, False, False
    
    def reset_info(self):
       self.ask_support.reset_dialogue()
       self.choose_info.reset_options()
       self.stan_info, self.krie_info, self.louie_info = False, False, False
       self.info_stan, self.info_krie, self.info_louie = 0,0,0
       self.info_counter, self.info_timer = 0 , 0
       self.info_choice = 0


    def reset_options(self, options):
        options.reset_options()
        self.choice = 0
        self.sec_choice = 0
        self.thi_choice = 0

    def end_convo(self, talk):
        finish = False
        if talk.finish_convo:
            finish =True
        if finish:
            self.game.settings.stan_dialogue_counter += 1
            return finish

    def render(self, display):

        if self.game.settings.stan_dialogue_counter == 0:
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

        if self.game.settings.stan_dialogue_counter > 0:
            self.options.render(display)
            if self.choice == 1:
                if self.reset_counter == 4:
                    display.blit(self.game.black, (0,0))
                display.blit(self.current_image, (0,0))
                if self.reset_counter == 0:
                    self.current_image = self.game.asset["stanley"]["talk"]
                    self.choose_reset.draw_text(display)
                if self.reset_counter == 1:
                    self.current_image = self.game.asset["torres"]["talk"]
                    self.reset_choice.render(display)
                if self.reset_counter == 2:
                    self.current_image = self.game.asset["stanley"]["shock"]
                    self.ask_for_reset.draw_text(display)
                if self.reset_counter == 3:
                    self.confirm.render(display)
                if self.reset_counter == 4:
                    self.current_image = self.game.asset["stanley"]["crazy"]
                    self.reset_confirm.draw_text(display)
            
            if self.choice == 2:
                if self.info_counter == 0:
                    self.ask_support.draw_text(display)
                if self.info_counter == 1:
                    self.choose_info.render(display)
                if self.info_counter == 2:
                    display.blit(self.current_image, (0,0))
                    display.blit(self.box, (self.box_rect.x, self.box_rect.y))
                    if self.stan_info:
                        if self.info_stan == 0:
                            for x in range(4):
                                self.game.draw_text(display, self.support_doll_info[x], True, (0,0,14), 240, 410 + (x*30), 22)
                        if self.info_stan == 1:
                            for x in range(5,8):
                                self.game.draw_text(display, self.support_doll_info[x], True, (0,0,14), 240, 410 + ((x-5)*30), 22)
                    if self.krie_info:
                        if self.info_krie == 0:
                            for x in range(9, 13):
                                self.game.draw_text(display, self.support_doll_info[x], True, (0,0,14), 240, 410 + ((x-9)*30), 22)
                        if self.info_krie == 1:
                            for x in range(14,16):
                                self.game.draw_text(display, self.support_doll_info[x], True, (0,0,14), 240, 410 + ((x-14)*30), 22)
                    if self.louie_info:
                        if self.info_louie == 0:
                            for x in range(17, 21):
                                self.game.draw_text(display, self.support_doll_info[x], True, (0,0,14), 240, 410 + ((x-17)*30), 22)
                        if self.info_louie == 1:
                            for x in range(22,25):
                                self.game.draw_text(display, self.support_doll_info[x], True, (0,0,14), 240, 410 + ((x-22)*30), 22)
                
                


