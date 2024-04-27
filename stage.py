import pygame
from state import *
from torres import *
from stanley import *
from louie import *
from krie import *
from ultimates import *
from enemy1 import *
from enemy3 import *
from ultimates import *
from confection import *

class Stage(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.camera = CameraGroup(self.game)
        self.ultimates()
        self.characters()
        self.confection_ult = pygame.sprite.Group()
        self.confection_ult.add(self.vanilla)
        self.confection_ult.add(self.float)
        self.confection_ult.add(self.strawb)
        self.background = pygame.image.load("sprites/bg_earlylvl.bmp").convert()
        self.black = pygame.image.load("sprites/black.png").convert_alpha()
        self.trees = pygame.image.load("sprites/asset_earlylvl.png").convert_alpha()
        # self.enemy1 = FrogEnemy(self.game, self.camera)
        self.c_time = 0
        self.newctime = pygame.time.get_ticks()
        self.ultimate = False
        self.countdown = 0
        self.immunity = False


    def update(self, deltatime, player_action):
        # player_action["up"] = False
        # player_action["down"] = False
        if self.game.ult == False:
            if self.game.damaged == True:
                self.immunity = True
                self.c_time += deltatime
                if self.c_time > 1:
                    self.game.damaged = False
                    self.immunity = False
            self.player.update(deltatime, player_action)
            if self.immunity == False:
                # self.stan.update(deltatime, player_action, self.player.rect.x, self.player.rect.y)
                self.louie.update(deltatime, player_action, self.player.rect.x, self.player.rect.y)
                # self.krie.update(deltatime, player_action, self.player.rect.x, self.player.rect.y)
                # self.enemy3.update(deltatime, player_action)
            # self.enemy1.update(deltatime, self.player) # pass player's position to enemy1

        if player_action["ultimate"]:
            self.game.ult = True

        if self.game.ult:
            self.stan_ult.update(deltatime, player_action)


    def render(self, display):
        display.blit(pygame.transform.scale(self.background, (1100,600)), (0,0))
        self.camera.custom_draw(display)
        display.blit(pygame.transform.scale(self.trees, (1200,600)), (-60,0))
        self.vanilla.render(display)
        self.float.render(display)
        self.strawb.render(display)
        
    
        if self.game.ult:
            display.blit(pygame.transform.scale(self.black, (1100,600)), (0,0))
            self.stan_ult.render(display)


        # if self.immunity == False:
        # self.stan.render(display)
        # self.player.render(display)
        # self.enemy3.render(display)


        #test code for enemy1
        # self.enemy1.render(display)

    def characters(self):
        self.player = Player(self.game, self.camera, 200,150) 
        self.louie = Louie(self.game, self.camera) 
        self.stan = Stanley(self.game, self.camera) 
        self.krie = Krie(self.game, self.camera)
        self.enemy3 = Enemy3(self.game, self.camera) 

    def ultimates(self):
        self.torres_ult = Torres_Ult(self.game)
        self.stan_ult = Stan_Ult(self.game)
        self.louie_ult = Louie_Ult(self.game)
        self.krie_ult = Krie_Ult(self.game)

        self.vanilla = Vanilla(self.game)
        self.float = Float(self.game)
        self.strawb = Strawb(self.game)




