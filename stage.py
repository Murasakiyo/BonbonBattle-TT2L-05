import pygame
from state import State, CameraGroup
from torres import Player
from stanley import Stanley
from enemy3 import Enemy3

class Stage(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.camera = CameraGroup(self.game)
        self.player = Player(self.game, self.camera) 
        self.stan = Stanley(self.game, self.camera) 
        self.enemy3 = Enemy3(self.game)
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
            if self.c_time > 3:
                self.game.damaged = False
                self.immunity = False
        self.player.update(deltatime, player_action)
        if self.immunity == False:
            self.stan.update(deltatime, player_action, self.player.rect.x, self.player.rect.y)

    def render(self, display):
        display.fill((100,100,100))
        self.camera.custom_draw(display)
        
        if self.immunity == False:
            self.stan.render(display)
        self.player.render(display)
        self.enemy3.render(display)



            

        
        
