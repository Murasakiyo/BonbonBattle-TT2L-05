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
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.ultimates()
        self.characters()
        self.background = pygame.image.load("sprites/bg_earlylvl.bmp").convert()
        self.black = pygame.image.load("sprites/black.png").convert_alpha()
        self.trees = pygame.image.load("sprites/asset_earlylvl.png").convert_alpha()
        self.c_time = 0
        self.newctime = pygame.time.get_ticks()
        self.ultimate = False
        self.countdown = 0
        self.immunity = False
        self.init_stan = False
        self.init_louie = False
        self.init_krie = False


    def update(self, deltatime, player_action):

        if self.game.ult == False:
            if self.game.damaged == True:
                self.immunity = True
                self.c_time += deltatime
                if self.c_time > 1:
                    self.game.damaged = False
                    self.immunity = False
            self.player.update(deltatime, player_action)
            if self.immunity == False:
                for support in self.support_dolls.sprites():
                    support.update(deltatime, player_action, self.player.rect.x, self.player.rect.y)

            if self.game.ult_finish == False:
                if pygame.sprite.spritecollide(self.player, self.confection_ult, False):
                    if pygame.sprite.spritecollide(self.player, self.confection_ult, False, pygame.sprite.collide_mask):
                        self.confection_ult.empty()

            if self.init_louie == False and self.init_krie == False:
                if pygame.sprite.spritecollide(self.player, self.vanilla_grp, False, pygame.sprite.collide_mask):
                    self.init_stan = True
                    self.camera.add(self.stan)
            if self.init_stan == False and self.init_krie == False:
                if pygame.sprite.spritecollide(self.player, self.float_grp, False, pygame.sprite.collide_mask):
                    self.init_louie = True
                    self.camera.add(self.louie)
            if self.init_louie == False and self.init_stan == False:
                if pygame.sprite.spritecollide(self.player, self.strawb_grp, False, pygame.sprite.collide_mask):
                    self.init_krie = True
                    self.camera.add(self.krie)

            if self.init_stan:
                self.support_dolls.add(self.stan)
            if self.init_louie:
                self.support_dolls.add(self.louie)
            if self.init_krie:
                self.support_dolls.add(self.krie)

        if player_action["ultimate"]:
            self.game.ult = True

        if self.game.ult:
            if self.init_stan:
                self.stan_ult.update(deltatime, player_action)
            elif self.init_louie:
                self.louie_ult.update(deltatime, player_action)
            elif self.init_krie:
                self.krie_ult.update(deltatime,player_action)
            else:
                self.torres_ult.update(deltatime,player_action)

        if self.game.ult_finish:
            self.init_stan = False
            self.init_louie = False
            self.init_krie = False

            for support in self.support_dolls.sprites():
                support.rect.x, support.rect.y = 0,200

            self.confection_ult.add(self.vanilla)
            self.confection_ult.add(self.float)
            self.confection_ult.add(self.strawb)

            self.stan.kill()
            self.louie.kill()
            self.krie.kill()
            self.game.ult_finish = False




    def render(self, display):
        display.blit(pygame.transform.scale(self.background, (1100,600)), (0,0))
        self.camera.custom_draw(display)
        display.blit(pygame.transform.scale(self.trees, (1200,600)), (-60,0))
        
        for confection in self.confection_ult.sprites():
            confection.render(display)

        # self.player.render(display)

        if self.game.ult:
            display.blit(pygame.transform.scale(self.black, (1100,600)), (0,0))
            if self.init_stan:
                self.stan_ult.render(display)
            elif self.init_louie:
                self.louie_ult.render(display)
            elif self.init_krie:
                self.krie_ult.render(display)
            else:
                self.torres_ult.render(display)


    def characters(self):
        self.player = Player(self.game, self.camera, 200,150) 
        self.louie = Louie(self.game) 
        self.stan = Stanley(self.game) 
        self.krie = Krie(self.game)

        # self.support_dolls.add(self.louie)
        # self.support_dolls.add(self.stan)
        # self.support_dolls.add(self.krie)

    

    def ultimates(self):
        self.vanilla_grp = pygame.sprite.Group()
        self.float_grp = pygame.sprite.Group()
        self.strawb_grp = pygame.sprite.Group()
        self.torres_ult = Torres_Ult(self.game)
        self.stan_ult = Stan_Ult(self.game)
        self.louie_ult = Louie_Ult(self.game)
        self.krie_ult = Krie_Ult(self.game)

        self.vanilla = Vanilla(self.game, self.vanilla_grp)
        self.float = Float(self.game, self.float_grp)
        self.strawb = Strawb(self.game, self.strawb_grp)

        self.confection_ult.add(self.vanilla)
        self.confection_ult.add(self.float)
        self.confection_ult.add(self.strawb)




