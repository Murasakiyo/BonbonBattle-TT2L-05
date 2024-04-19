import pygame
from state import State, CameraGroup
from torres import Player
from stanley import Stanley
from louie import Louie

class Stage(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.camera = CameraGroup(self.game)
        self.background = pygame.image.load("sprites/bg_earlylvl.bmp").convert()
        self.trees = pygame.image.load("sprites/asset_earlylvl.png").convert_alpha()
        self.player = Player(self.game, self.camera) 
        self.stan = Stanley(self.game, self.camera) 
        self.c_time = 0
        self.newctime = pygame.time.get_ticks()
        self.countdown = 0
        self.immunity = False
        


    def update(self, deltatime, player_action):
        # player_action["up"] = False
        # player_action["down"] = False
        if self.game.damaged == True:
            self.immunity = True
            self.c_time += deltatime
            if self.c_time > 1:
                self.game.damaged = False
                self.immunity = False
        self.player.update(deltatime, player_action)
        if self.immunity == False:
            self.stan.update(deltatime, player_action, self.player.rect.x, self.player.rect.y)

    def render(self, display):
        display.blit(pygame.transform.scale(self.background, (1100,600)), (0,0))
        self.camera.custom_draw(display)
        display.blit(pygame.transform.scale(self.trees, (1200,600)), (-60,0))
        
        # if self.immunity == False:
        self.stan.render(display)
        # self.player.render(display)



            

        
        
