import pygame
from parent_classes.state import *
from parent_classes.dialogue import *
from torres import *

class Lounge(State, Dialogue):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.player = Player(self.game,100,250)
        self.camera = CameraGroup(self.game)
        self.camera.add(self.player)
        self.background = {
            "ground": pygame.image.load("sprites/backgrounds/ground.bmp").convert(),
            "bg": pygame.transform.scale(pygame.image.load("sprites/lounge.bmp"), (2125,750)).convert(),
        }

    def update(self, deltatime, player_action):
        player_action["up"], player_action["down"] = False, False
        player_action["ultimate"], player_action["attack"], player_action["defend"],= False, False, False

        self.player.update(deltatime,player_action)

    def render(self, display):
        display.blit(self.background["bg"], (0,-320))
        display.blit(self.background["ground"], (0,420))
        self.camera.custom_draw(display)
