import pygame
from parent_classes.state import *
from parent_classes.dialogue import *
from torres import *
from camera import *

class Lounge(State, Dialogue):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.player = Player(self.game, 0, 150)
        
        self.camera = LoungeCamera(self.game)
        self.camera.add(self.player)
        # self.offset = pygame.math.Vector2((0,0))

    def update(self, deltatime, player_action):
        player_action["up"], player_action["down"] = False, False
        player_action["ultimate"], player_action["attack"], player_action["defend"],= False, False, False
        
        self.player.update(deltatime,player_action)

    def render(self, display):
        self.camera.custom_draw(display, self.player)
