import pygame
from parent_classes.dialogue import *

class Krie_Dialogue():
    def __init__(self, game):
       super().__init__()
       self.game = game
       question_1 = ["Hello, Torres! How're the battles?", " " ]
       self.convo = Dialogue(self.game, "black", 24, question_1)
       self.answer1 = Answer(self.game, "It was alright.", "Your highness, I require your assistance..!", "I am terrified.")
       self.asset = {
            "happy": pygame.image.load("sprites/dialogue/krie/happy.png").convert_alpha(),
            "miffed": pygame.image.load("sprites/dialogue/krie/miffed.png").convert_alpha(),
            "talk": pygame.image.load("sprites/dialogue/krie/talk.png").convert_alpha(),
            "think": pygame.image.load("sprites/dialogue/krie/think.png").convert_alpha(),
       }
       self.krie_answer = self.game.open_txt("first_krie.txt")
       self.test = Dialogue(self.game, "black", 24, self.krie_answer)
       self.pick1 = 0


    def update(self, deltatime, player_action):
        for actions in player_action:
            if not(player_action["next"]) and not(player_action["go"]):
                player_action[actions] = False
        self.convo.dialogue_update(player_action)
        self.convo.finish()
        # if self.convo.finish_convo:
        if not self.pick1 == 1 and not self.pick1 == 2 and not self.pick1 == 3 :
            self.answer1.update(deltatime, player_action)
            self.pick1 = self.answer1.pick_choice(player_action)
        if self.pick1 == 1 or self.pick1 == 2 or self.pick1 == 3:
            self.test.dialogue_update(player_action)
            self.test.transtion_end()


    def end_convo(self):
        finish = False
        if self.test.finish_convo:
            finish =True
            return finish


    def render(self, display):
        if not(self.convo.finish_convo):
            display.blit(self.asset["happy"], (0,0))
            self.convo.draw_text(display)

        if self.convo.finish_convo:
            if not self.pick1 == 1 and not self.pick1 == 2 and not self.pick1 == 3:
                self.answer1.render(display)

        if self.pick1 == 1 or self.pick1 == 2 or self.pick1 == 3:
            if not(self.test.finish_convo):
                display.blit(self.asset["happy"], (0,0))
                self.test.draw_text(display)


