import pygame
from parent_classes.dialogue import *

class Krie_Dialogue():
    def __init__(self, game):
       super().__init__()
       self.game = game
       question_1 = ["Why if it isn't the Ganache Knight!","How're the battles?", " " ]
       self.convo = Dialogue(self.game, "black", 24, question_1)
       self.answer1 = Answer(self.game, "It was alright.", "Your highness, I require your assistance..!", "I haven't battled yet.", " ", True, False)
       self.asset = {
            "happy": pygame.image.load("sprites/dialogue/krie/happy.png").convert_alpha(),
            "miffed": pygame.image.load("sprites/dialogue/krie/miffed.png").convert_alpha(),
            "talk": pygame.image.load("sprites/dialogue/krie/talk.png").convert_alpha(),
            "think": pygame.image.load("sprites/dialogue/krie/think.png").convert_alpha(),
       }
       self.krie_answer = self.game.open_txt("first_krie.txt")
       self.krie_reply = Dialogue(self.game, "black", 24, self.krie_answer)
       self.pick1 = 0
       self.current_krie = self.asset["talk"]


    def update(self, deltatime, player_action):
        for actions in player_action:
            if not(player_action["next"]) and not(player_action["go"]):
                player_action[actions] = False
        self.convo.dialogue_update(player_action)
        self.convo.finish()
        if not self.pick1 == 1 and not self.pick1 == 2 and not self.pick1 == 3 :
            self.answer1.update(deltatime, player_action)
            self.pick1 = self.answer1.pick_choice(player_action)
        if self.pick1 == 1 or self.pick1 == 2 or self.pick1 == 3:
            self.krie_reply.dialogue_update(player_action)
            self.krie_reply.transtion_end()


    def end_convo(self):
        finish = False
        if self.krie_reply.finish_convo:
            finish =True
            return finish


    def render(self, display):
        if not(self.convo.finish_convo):
            display.blit(self.asset["happy"], (0,0))
            self.convo.draw_text(display)

        if self.convo.finish_convo:
            if not self.pick1 == 1 and not self.pick1 == 2 and not self.pick1 == 3:
                display.blit(self.game.asset["torres"]["talk"], (0,0))
                self.answer1.render(display)

        if self.pick1 == 1 or self.pick1 == 2 or self.pick1 == 3:
            if not(self.krie_reply.finish_convo):
                if self.krie_reply.activetext == 2:
                    self.current_krie = self.asset["talk"]
                if self.krie_reply.activetext == 4:
                    self.current_krie = self.asset["think"]
                display.blit(self.current_krie, (0,0))
                self.krie_reply.draw_text(display)




