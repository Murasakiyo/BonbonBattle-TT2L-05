import pygame
from state import State, CameraGroup
from torres import Player
from stanley import Stanley
from louie import Louie
from krie import Krie
from enemy1 import FrogEnemy
from enemy2 import FlyEnemy
from enemy3 import Enemy3
import random

class Stage(State):
    def __init__(self, game):
        State.__init__(self, game)
        self.camera = CameraGroup(self.game)
        self.background = pygame.image.load("sprites/bg_earlylvl.bmp").convert()
        self.trees = pygame.image.load("sprites/asset_earlylvl.png").convert_alpha()
        self.player = Player(self.game, self.camera) 
        self.louie = Louie(self.game, self.camera) 
        self.stan = Stanley(self.game, self.camera) 
        self.krie = Krie(self.game, self.camera)
        self.enemy1 = FrogEnemy(self.game)
        # self.enemy2 = FlyEnemy(self.game)
        # self.enemy3 = Enemy3(self.game, self.camera)
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
            # self.stan.update(deltatime, player_action, self.player.rect.x, self.player.rect.y)
            # self.louie.update(deltatime, player_action, self.player.rect.x, self.player.rect.y)
            # self.krie.update(deltatime, player_action, self.player.rect.x, self.player.rect.y)
            # self.enemy3.update(deltatime, player_action)
            pass
        self.enemy1.update(deltatime, player_action, self.player.rect.center[0], self.player.rect.center[1], self.player.enemy1_collision) # pass player's position to enemy1
        # self.enemy2.update(deltatime, player_action, self.player.rect.center[0], self.player.rect.center[1]) # pass player's position to enemy2

        # for i in range(3):
        #     random_x = random.randint(0, self.game.SCREENWIDTH)
        #     random_y = random.randint(0, self.game.SCREENHEIGHT)
        #     new_enemy = FlyEnemy(self.game)  # Create a new enemy instance
        #     new_enemy.rect.center = (random_x, random_y)  # Position
        #     self.enemy2.enemies.add(new_enemy)  # Add the enemy to the grp


    def render(self, display):
        display.blit(pygame.transform.scale(self.background, (1100,600)), (0,0))
        self.camera.custom_draw(display)
        display.blit(pygame.transform.scale(self.trees, (1200,600)), (-60,0))
    

        # if self.immunity == False:
        # self.stan.render(display)
        # self.player.render(display)



        #test code for enemy1
        # self.enemy1.render(display)
        self.player.render(display)
        self.enemy1.render(display)
        # self.enemy2.render(display)
        # self.enemy3.render(display)

