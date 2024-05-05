import pygame
from parent_classes.state import *
from torres import *
from enemy1 import *
from confection import *
from parent_classes.ultimate_action import *


class First_Stage(State, Ults):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.ultimates()
        self.characters()
        self.enemy1 = FrogEnemy(self.game, self.camera)
        self.tongue = Tongue(self.game)
        self.tongue2 = Tongue2(self.game)
        self.c_time = 0
        self.newctime = pygame.time.get_ticks()
        self.ultimate = False
        self.countdown = 0
        self.immunity = False

    def update(self, deltatime, player_action):
        # print(int(self.player.rect.x - self.enemy1.rect.x))

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
                self.enemy1.update(deltatime, player_action, self.player.rect.center[0], 
                                self.player.rect.center[1], self.player.enemy1_collision, self.player.rect.x) 
                self.tongue.update(deltatime, player_action, self.enemy1.rect.centerx - 190, self.enemy1.rect.centery - 5, self.enemy1.attack)
                self.tongue2.update(deltatime, player_action, self.enemy1.rect.centerx -10, self.enemy1.rect.centery - 5, self.enemy1.attack)
                self.update_ultimate(deltatime, player_action)

            if player_action["ultimate"]:
                if self.player.moxie_points >= 250:
                    self.game.ult = True
                    self.player.moxie_points = 0

            self.add_ultimate(deltatime, player_action)
        else:
            self.game.start_timer()


    def render(self, display):
        display.blit(pygame.transform.scale(self.game.forest, (1100,600)), (0,0))

        self.camera.custom_draw(display)
        
        if self.enemy1.current_anim_list == self.enemy1.attack_left:
            self.tongue.render(display)
        elif self.enemy1.current_anim_list == self.enemy1.attack_right:
            self.tongue2.render(display)
        display.blit(pygame.transform.scale(self.game.trees, (1200,600)), (-60,0))
        
        self.ultimate_display(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, "white", 500,150,200)

        

    





