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
       

        self.take_damage = False
        self.attack_time = 0
        self.let_attack = True
        self.deal_damage = False
        self.attack_cooldown = 0

    def update(self, deltatime, player_action):
        print(self.fly_swarm.flylist)
        if self.game.start == True:
            if self.game.ult == False:

                # Update player and enemies
                self.player.update(deltatime, player_action)
                self.fly_swarm.update(deltatime, player_action, self.player.rect.center[0], 
                                   self.player.rect.center[1], self.player.rect, self.player.rect.x) 
                
                self.update_ultimate(deltatime, player_action)
                self.health_update()
                self.moxie_update(player_action)

                for flies in self.fly_swarm.flylist.sprites():
                    self.flies_collisions(deltatime, player_action, self.fly_swarm.flylist, self.fly_swarm.flylist, flies, 
                                        flies.damage, flies.body_damage)
                    
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
        
        # Player stats
        self.health_render(display)
        self.moxie_render(display)

        self.groupenemy_health_render(display,self.fly_swarm.flylist.sprites())

        self.ultimate_display(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, "white", 500,150,200)
