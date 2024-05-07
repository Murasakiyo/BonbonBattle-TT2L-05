import pygame
from parent_classes.state import *
from torres import *
from enemy1 import *
from confection import *
from parent_classes.ultimate_action import *
from parent_classes.health import *
from parent_classes.collisions import *
from parent_classes.moxie import *
from parent_classes.enemyhealthbar import *


class First_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar):
    def __init__(self, game):
        super().__init__(game)

        # Sprite groups
        self.camera = CameraGroup(self.game)
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.attack_group = pygame.sprite.Group()
        self.body_group = pygame.sprite.Group()
        self.enemy1 = FrogEnemy(self.game, self.camera)
        self.tongue = Tongue(self.game)
        self.tongue2 = Tongue2(self.game)

        self.ultimates()
        self.characters()
        self.load_health_bar()
        self.load_moxie_bar()
        self.enemy_health_update(self.enemy1.rect.x, self.enemy1.rect.y, self.enemy1.HP)

        self.attack_group.add(self.tongue, self.tongue2)
        self.body_group.add(self.enemy1)
        self.moxie_points = 0
      


    def update(self, deltatime, player_action):
        # print(int(self.player.rect.x - self.enemy1.rect.x))

        if self.game.start == True:
            if self.game.ult == False:
                
                # Update player and enemies
                self.player.update(deltatime, player_action)
                self.enemy1.update(deltatime, player_action, self.player.rect.center[0], 
                                self.player.rect.center[1], self.player.horiz_line, self.player.rect.x) 
                self.tongue.update(deltatime, player_action, self.enemy1.rect.centerx - 190, self.enemy1.rect.centery - 5, self.enemy1.attack)
                self.tongue2.update(deltatime, player_action, self.enemy1.rect.centerx -10, self.enemy1.rect.centery - 5, self.enemy1.attack)
                self.update_ultimate(deltatime, player_action)
                self.enemy_collisions(deltatime, player_action, self.body_group, self.attack_group, self.enemy1, 
                                      self.enemy1.tongue_damage, self.enemy1.body_damage, self.tongue, self.tongue2)
                self.health_update()
                self.moxie_update(player_action)
                self.enemy_health_update(self.enemy1.rect.x, self.enemy1.rect.y, self.enemy1.HP)


            self.add_ultimate(deltatime, player_action)
        else:
            self.game.start_timer()


    def render(self, display):
        display.blit(pygame.transform.scale(self.game.forest, (1100,600)), (0,0))
        # self.player.render(display)
        self.camera.custom_draw(display)
        
        if self.enemy1.current_anim_list == self.enemy1.attack_left:
            self.tongue.render(display)
        elif self.enemy1.current_anim_list == self.enemy1.attack_right:
            self.tongue2.render(display)
        display.blit(pygame.transform.scale(self.game.trees, (1200,600)), (-60,0))
        
        self.health_render(display)
        self.moxie_render(display)
        self.enemy_health_render(display, self.enemy1.rect.x, self.enemy1.rect.y)


        self.ultimate_display(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, "white", 500,150,200)

        


    





