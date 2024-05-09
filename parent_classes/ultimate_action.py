import pygame
from torres import *
from stanley import *
from louie import *
from krie import *
from ultimates import *
from confection import *

class Ults():
    def __init__(self, game):
        self.game = game


    def update_ultimate(self, deltatime, player_action):
            # Sprite group update
            for support in self.support_dolls.sprites():
                support.update(deltatime, player_action, self.player.rect.x, self.player.rect.y)

            if self.game.ult_finish == False:
                # Check for collision rect and the mask collision
                if pygame.sprite.spritecollide(self.player, self.confection_ult, False):
                    if pygame.sprite.spritecollide(self.player, self.confection_ult, False, pygame.sprite.collide_mask):
                        self.confection_ult.empty() # Remove everything in the sprite group

            self.check_specifics()
            
    def add_ultimate(self, deltatime, player_action):
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
                self.ultimate_reset()


    def ultimate_display(self, display):

        for confection in self.confection_ult.sprites():
            confection.render(display)

        if self.game.ult:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.init_stan:
                self.stan_ult.render(display)
            elif self.init_louie:
                self.louie_ult.render(display)
            elif self.init_krie:
                self.krie_ult.render(display)
            else:
                self.torres_ult.render(display)


    def characters(self):
        self.player = Player(self.game, self.camera, 200,200) 
        self.louie = Louie(self.game) 
        self.stan = Stanley(self.game) 
        self.krie = Krie(self.game)

        # Initiation of a specific support doll
        self.init_stan = False
        self.init_louie = False
        self.init_krie = False


    
    # All sprites, ultimate sprite groups, and non-sprite ultimates are here
    def ultimates(self):

        self.vanilla_grp = pygame.sprite.Group()
        self.float_grp = pygame.sprite.Group()
        self.strawb_grp = pygame.sprite.Group()

        self.torres_ult = Torres_Ult(self.game)
        self.stan_ult = Stan_Ult(self.game)
        self.louie_ult = Louie_Ult(self.game)
        self.krie_ult = Krie_Ult(self.game)

        # Confection drops--------------------------------
        self.vanilla = Vanilla(self.game, self.vanilla_grp)
        self.float = Float(self.game, self.float_grp)
        self.strawb = Strawb(self.game, self.strawb_grp)

        self.confection_ult.add(self.vanilla)
        self.confection_ult.add(self.float)
        self.confection_ult.add(self.strawb)
        # -------------------------------------------------

    # Reset all sprite groups and sprite position
    def ultimate_reset(self):
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


    # Check the specific confection that is picked up
    def check_specifics(self):

        # Enable ultimate initiation and adding sprites into sprite groups
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

        # Add sprites into support doll sprite grp for UPDATES
        if self.init_stan:
            self.support_dolls.add(self.stan)
        if self.init_louie:
            self.support_dolls.add(self.louie)
        if self.init_krie:
            self.support_dolls.add(self.krie)