import pygame
from parent_classes.state import *
from parent_classes.dialogue import *
from states.level_choose import Level_Options
from states.lounge import Lounge


class Story(State, Dialogue):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.scene = {
            "0": pygame.image.load("sprites/lounge.bmp").convert(),
            "1": pygame.image.load("sprites/first_cutscene/1.png").convert(),
            "2": pygame.image.load("sprites/first_cutscene/2.png").convert(),
            "3": pygame.image.load("sprites/first_cutscene/3.png").convert(),
            "4": pygame.image.load("sprites/first_cutscene/4.png").convert(),
            "5": pygame.image.load("sprites/first_cutscene/5.png").convert()
        }
        self.current_scene = self.scene["0"]
        self.intro = self.dialogue("intro.txt")
        self.variable("black", 24, self.intro)


    def update(self, deltatime, player_action):
        self.dialogue_update(player_action)
        if self.finish_convo:
            player_action["transition"] = True

        if self.game.alpha >= 240:
            self.game.draw_text(self.game.screen, "Loading...", True, "white", 400, 250, 80)
        if self.game.alpha == 255:
            new_state = Lounge(self.game)
            new_state.enter_state()
            player_action["transition"] =  False
            self.game.skip_cutscenes = True
        # self.transition_to_next_state(player_action)


    def transition_to_next_state(self, player_action):
        if self.activetext >= len(self.text) - 1:
            if player_action["next"]:
                self.game.state_stack.pop()
                player_action["next"] = False
                self.game.state_stack.append(Lounge(self.game))
                # self.game.state_stack.append(Level_Options(self.game))
                

    def render(self, display):
        if self.activetext == 2:
            self.current_scene= self.scene["1"]
        elif self.activetext == 4:
            self.current_scene= self.scene["2"]
        elif self.activetext == 6:
            self.current_scene= self.scene["3"]
        elif self.activetext == 8:
            self.current_scene= self.scene["4"]
        elif self.activetext == 12:
            self.current_scene= self.scene["5"]
        display.blit(self.current_scene, (0,0))
        self.draw_text(display)