import pygame
from parent_classes.state import *
from torres import *
from enemy3 import *
from confection import *
from parent_classes.ultimate_action import *
from parent_classes.health import *
from parent_classes.collisions import *
from parent_classes.moxie import *
from parent_classes.enemyhealthbar import *


class Quad_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.c_time = 0
        self.newctime = pygame.time.get_ticks()
        self.ultimate = False
        self.countdown = 0
        self.immunity = False

        self.enemy3_heal = 0

        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.enemy3 = Enemy3(self.game, self.camera)
        self.body_group = pygame.sprite.Group()
        self.attack_group = pygame.sprite.Group()

        self.ultimates()
        self.characters()
        self.load_health_bar()
        self.load_moxie_bar()
        self.enemy_health_update(self.enemy3.rect.x, self.enemy3.rect.y, self.enemy3.HP)

        self.attack_group.add(self.enemy3)
        self.body_group.add(self.enemy3)

    def update(self, deltatime, player_action):
        if self.game.start == True:
            if self.game.ult == False:

                # Update player and enemies
                self.player.update(deltatime, player_action)
                self.enemy3.update(deltatime, player_action, self.player.rect.center[0], self.player.rect.center[1], self.player.rect.x)

                self.health_update()
                self.moxie_update(player_action)
                self.enemy_health_update(self.enemy3.rect.x, self.enemy3.rect.y, self.enemy3.HP)
                
                self.update_ultimate(deltatime, player_action)

                self.flies_collisions(deltatime, player_action, self.body_group, self.attack_group, self.enemy3, self.enemy3.damage, self.enemy3.body_damage)
                self.minion_collisions(self.player.lines)

                if self.enemy3.leech == True:
                    self.old_health = self.player.healthpoints
                    self.player.healthpoints -= (self.player.healthpoints * 20/100)
                    self.enemy3_heal = (self.old_health * 20/100)
                    self.enemy3.HP += self.enemy3_heal

                if self.enemy3.HP > 300:
                    self.enemy3.HP = 300

                # print(self.enemy3_heal)

            self.add_ultimate(deltatime, player_action)
        else:
            self.game.start_timer()


    def render(self, display):
        display.blit(pygame.transform.scale(self.game.forest, (1100,600)), (0,0))
        self.confection_display(display)
        self.camera.custom_draw(display)
        self.enemy3.render(display)
        display.blit(pygame.transform.scale(self.game.trees, (1200,600)), (-60,0))
        
        self.health_render(display)
        self.moxie_render(display)
        self.boss_health_render(display)
        
        self.ultimate_display(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, "white", 500,150,200)
