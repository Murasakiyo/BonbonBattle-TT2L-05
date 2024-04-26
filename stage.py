import pygame
from state import State, CameraGroup
from torres import Player
from stanley import Stanley
from louie import Louie
from krie import Krie
from ultimates import Ultimate
from enemy1 import FrogEnemy
from enemy3 import Enemy3
from ultimates import *



class Stage(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.camera = CameraGroup(self.game)
        self.ult = Ultimate(self.game)
        self.ultimates()
        self.characters()
        self.background = pygame.image.load("sprites/bg_earlylvl.bmp").convert()
        self.trees = pygame.image.load("sprites/asset_earlylvl.png").convert_alpha()
        # self.enemy1 = FrogEnemy(self.game, self.camera)
        self.c_time = 0
        self.newctime = pygame.time.get_ticks()
        self.ultimate = False
        self.countdown = 0
        self.immunity = False

    def characters(self):
        self.player = Player(self.game, self.camera, 200,150) 
        self.louie = Louie(self.game, self.camera) 
        self.stan = Stanley(self.game, self.camera) 
        self.krie = Krie(self.game, self.camera)
        self.enemy3 = Enemy3(self.game, self.camera) 

    def ultimates(self):
        self.torres_ult = Torres_Ult(self.game, self.ult)
        self.stan_ult = Stan_Ult(self.game, self.ult)
        self.louie_ult = Louie_Ult(self.game, self.ult)
        self.krie_ult = Krie_Ult(self.game, self.ult)

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
            # self.louie.update(deltatime, player_action, self.player.rect.x, self.player.rect.y)
            # self.krie.update(deltatime, player_action, self.player.rect.x, self.player.rect.y)
            # self.enemy3.update(deltatime, player_action)
        # self.enemy1.update(deltatime, self.player) # pass player's position to enemy1

        if player_action["ultimate"]:
            new_state = Ultimate(self.game)
            new_state.enter_state()


    def render(self, display):
        display.blit(pygame.transform.scale(self.background, (1100,600)), (0,0))
        self.camera.custom_draw(display)
        display.blit(pygame.transform.scale(self.trees, (1200,600)), (-60,0))
    

        # if self.immunity == False:
        # self.stan.render(display)
        # self.player.render(display)
        # self.enemy3.render(display)


        #test code for enemy1
        # self.enemy1.render(display)
