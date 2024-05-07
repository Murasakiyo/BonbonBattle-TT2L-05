import pygame
from parent_classes.state import *
from torres import *
from enemy2 import *
from confection import *
from parent_classes.ultimate_action import *
from parent_classes.health import *
from parent_classes.collisions import *
from parent_classes.moxie import *
from parent_classes.enemyhealthbar import *


class Sec_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.fly_swarm = FlyEnemy(self.game)
        # self.enemy2 = Fly(self.game)
        # self.fly_group = pygame.sprite.Group()
        # self.fly_group.add(self.enemy2)
        self.ultimates()
        self.characters()
        self.load_health_bar()
        self.load_moxie_bar()
        # self.load_enemy_health(self.enemy2, self.enemy2.rect.centerx, self.enemy2.rect.centery)
        self.c_time = 0
        self.newctime = pygame.time.get_ticks()
        self.ultimate = False
        self.countdown = 0
        self.immunity = False

        self.take_damage = False
        self.attack_time = 0
        self.let_attack = True
        self.deal_damage = False
        self.attack_cooldown = 0

    def update(self, deltatime, player_action):

        if self.game.start == True:
            if self.game.ult == False:
                # Cooldown for player receiving damage
                if self.game.damaged == True:
                    self.immunity = True
                    self.c_time += deltatime
                    if self.c_time > 2:
                        self.game.damaged = False
                        self.immunity = False

                # Update player and enemies
                self.player.update(deltatime, player_action)
                self.fly_swarm.update(deltatime, player_action, self.player.rect.center[0], 
                                   self.player.rect.center[1], self.player.rect, self.player.rect.x) 
                
                self.update_ultimate(deltatime, player_action)
                self.health_update()
                self.moxie_update(player_action)
                for flies in self.fly_swarm.flylist.sprites():
                    self.enemy_collisions(deltatime, player_action, self.fly_swarm.flylist, self.fly_swarm.flylist, flies, 
                                        flies.damage, flies.body_damage, flies, flies, False)
                    self.enemy_health_update(flies, flies.rect.x, flies.rect.y, flies.HP, False)
                    

            if player_action["ultimate"]:
                self.game.ult = True            
            self.add_ultimate(deltatime, player_action)
        else:
            self.game.start_timer()
        # print(self.attack_time)

    def render(self, display):
        display.blit(pygame.transform.scale(self.game.forest2, (1100,600)), (0,0))
        self.camera.custom_draw(display)
        self.fly_swarm.render(display)
        display.blit(pygame.transform.scale(self.game.trees, (1200,600)), (-60,0))
        
        self.health_render(display)
        self.moxie_render(display)
        for flies in self.fly_swarm.flylist.sprites():
            self.enemy_health_render(display, flies.rect.x, flies.rect.y)

        self.ultimate_display(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, "white", 500,150,200)
