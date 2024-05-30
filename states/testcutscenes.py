import pygame
from parent_classes.state import State
from states.level_choose import Level_Options

class CutscenesTest(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.click = False
        self.next = False
        self.saving_system = game.saving_system
        
    def update(self, deltatime, player_action):
        if not self.click:
            if pygame.mouse.get_pressed()[0]:
                self.click = True
                self.next = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False

        if self.next:
            self.game.skip_cutscenes = True
            self.saving_system.save_data_file()
            new_state = Level_Options(self.game)
            new_state.enter_state()
            self.next = False

    def render(self, display):
        display.fill((240,128,128))