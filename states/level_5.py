import pygame
from parent_classes.state import *
from torres import *
from enemy4 import *
from confection import *
from parent_classes.ultimate_action import *
from parent_classes.health import *
from parent_classes.collisions import *
from parent_classes.moxie import *
from parent_classes.enemyhealthbar import *
from parent_classes.particleeffect import *


class Penta_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar, ParticleFunctions):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.ultimate = False

        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.body_group = pygame.sprite.Group()
        self.attack_group = pygame.sprite.Group()

        self.ultimates()
        self.characters()
        self.load_health_bar()
        self.load_moxie_bar()
        self.enemy4 = Enemy4(self.game, self.player.rect.centerx, self.player.rect.centery)
        # self.enemy_health_update(self.enemy4.rect.x, self.enemy4.rect.y, self.enemy4.HP)


        self.deal_damage = True
        self.attack_cooldown = 0
        self.countdown = 0
        self.gacha = 0
        self.accept_ult = False


    def update(self, deltatime, player_action):
        # print(int(self.enemy2.flies.rect.x-self.player.rect.x))

        if self.game.start == True:
            if self.game.ult == False:

                # Update player and enemies
                self.player.update(deltatime, player_action)


                self.health_update()
                self.moxie_update(player_action)
                # self.enemy_health_update(self.enemy4.rect.x, self.enemy4.rect.y, self.enemy4.HP)

                self.enemy4.update(deltatime, player_action, self.player.rect.centerx, self.player.rect.centery)
                self.update_ultimate(deltatime, player_action)


                self.get_hit(deltatime, player_action)  
                
                        

            self.add_ultimate(deltatime, player_action, self.body_group)
        else:
            self.game.start_timer()


    def render(self, display):
        display.blit(pygame.transform.scale(self.game.forest, (1100,600)), (0,0))
        self.camera.custom_draw(display)

        display.blit(pygame.transform.scale(self.game.trees, (1200,600)), (-60,0))
        # self.player.render(display)
        self.enemy4.render(display)

        self.health_render(display)
        self.moxie_render(display)
        # self.boss_health_render(display)
        
        if self.game.ult:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
        self.ultimate_display(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, True, "white", 500,150,200)

    def get_hit(self, deltatime, player_action):
        if self.player.take_damage == False:
            if any(self.enemy4.aira_spin.clipline(*line) for line in self.player.lines):
                self.player.healthpoints -= 20
                self.player.take_damage = True

        if self.player.take_damage == False:
            if any(self.enemy4.rect_string1.clipline(*line) for line in self.player.lines):
                self.player.healthpoints -= 10
                # self.enemy4.moxie += 20
                self.player.take_damage = True

        if self.player.take_damage == False:
            if any(self.enemy4.rect_string2.clipline(*line) for line in self.player.lines):
                self.player.healthpoints -= 10
                # self.enemy4.moxie += 20
                self.player.take_damage = True

        if self.player.take_damage:
            self.countdown += deltatime
            if self.countdown > 2:
                self.player.take_damage = False
                self.countdown = 0

        if self.deal_damage:
            if player_action["attack"]:
                self.enemy4.HP -= 150
                self.deal_damage = False
        if not self.deal_damage:
            self.attack_cooldown += deltatime
            if self.attack_cooldown > 2:
                self.deal_damage = True
                self.attack_cooldown = 0
