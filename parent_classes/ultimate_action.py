import pygame
from torres import *
from stanley import *
from louie import *
from krie import *
from ultimates import *
from confection import *
import random

class Ults():
    def __init__(self, game):
        self.game = game


    # Updating the ultimate when initiated
    def update_ultimate(self, deltatime, player_action):
            print(self.vanilla_grp)
            # Sprite group update
            for support in self.support_dolls.sprites():
                support.update(deltatime, self.player, player_action, self.player.rect.x, self.player.rect.y)

            if self.game.ult_finish == False:
                
                if not(self.accept_ult):
                    if self.gacha == 3:
                        self.vanilla.update()
                        self.confection_ult.add(self.vanilla)
                        self.vanilla_grp.add(self.vanilla)
                    elif self.gacha == 6:
                        self.strawb.update()
                        self.confection_ult.add(self.strawb)
                        self.strawb_grp.add(self.strawb)
                    elif self.gacha == 9:
                        self.float.update()
                        self.confection_ult.add(self.float)
                        self.float_grp.add(self.float)

            
                    # Check for collision rect and the mask collision
                    if pygame.sprite.spritecollide(self.player, self.confection_ult, False):
                        if pygame.sprite.spritecollide(self.player, self.confection_ult, False, pygame.sprite.collide_mask):
                            self.confection_ult.empty() # Remove everything in the sprite group

            self.check_specifics()

    # Check which support doll is initiated        
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

    # Display confection
    def confection_display(self,display):
        for confection in self.confection_ult.sprites():
            confection.render(display)

    # Display the ultimate animation
    def ultimate_display(self, display):
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

    # Initialize the objects
    def characters(self):
        self.player = Player(self.game, 200,200) 
        self.louie = Louie(self.game) 
        self.stan = Stanley(self.game) 
        self.krie = Krie(self.game)
        self.camera.add(self.player)
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
        self.vanilla = Vanilla(self.game)
        self.float = Float(self.game)
        self.strawb = Strawb(self.game)
        # -------------------------------------------------

    # Reset all sprite groups and sprite position
    def ultimate_reset(self):
        self.init_stan = False
        self.init_louie = False
        self.init_krie = False

        for support in self.support_dolls.sprites():
            support.rect.x, support.rect.y = 0,200

        min_x, max_x = 100, self.game.SCREENWIDTH - 100
        min_y, max_y = 100, self.game.SCREENHEIGHT - 100
        self.vanilla.rect.x, self.vanilla.rect.y = random.randint(min_x, max_x), random.randint(min_y, max_y)
        self.float.rect.x, self.float.rect.y = random.randint(min_x, max_x), random.randint(min_y, max_y)
        self.strawb.rect.x, self.strawb.rect.y = random.randint(min_x, max_x), random.randint(min_y, max_y)

        self.stan.kill()
        self.louie.kill()
        self.krie.kill()
        self.vanilla.kill()
        self.float.kill()
        self.strawb.kill()
        self.game.ult_finish = False
        self.gacha = 0
        self.accept_ult = False


    # Check the specific confection that is picked up
    def check_specifics(self):

        if not(self.accept_ult):
            # Enable ultimate initiation and adding sprites into sprite groups
            if self.init_louie == False and self.init_krie == False:
                if pygame.sprite.spritecollide(self.player, self.vanilla_grp, False, pygame.sprite.collide_mask):
                    self.init_stan = True
                    self.camera.add(self.stan)
                    self.support_dolls.add(self.stan)
                    self.accept_ult = True
            if self.init_stan == False and self.init_krie == False:
                if pygame.sprite.spritecollide(self.player, self.float_grp, False, pygame.sprite.collide_mask):
                    self.init_louie = True
                    self.camera.add(self.louie)
                    self.support_dolls.add(self.louie)
                    self.accept_ult = True
            if self.init_louie == False and self.init_stan == False:
                if pygame.sprite.spritecollide(self.player, self.strawb_grp, False, pygame.sprite.collide_mask):
                    self.init_krie = True
                    self.camera.add(self.krie)
                    self.support_dolls.add(self.krie)
                    self.accept_ult = True

                

