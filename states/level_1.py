import pygame
from parent_classes.state import *
from torres import *
from enemy1 import *
from confection import *
from parent_classes.ultimate_action import *
from health import *
from collisions import *


class First_Stage(State, Ults, Collisions):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.ultimates()
        self.characters()
        self.load_for_collision()
        self.enemy1 = FrogEnemy(self.game, self.camera)
        self.tongue = Tongue(self.game)
        self.tongue2 = Tongue2(self.game)
        self.tongue_group = pygame.sprite.Group()
        self.frog_group = pygame.sprite.Group()
        self.tongue_group.add(self.tongue, self.tongue2)
        self.frog_group.add(self.enemy1)
        # self.health = Health(self.game)
        self.healthpoints = 250
        self.moxie_points = 0
        self.take_damage = False
        # self.collision = Collisions(self.game)
        self.take_damage = False
        self.health_bar = pygame.Rect(10, 10, self.healthpoints, 40)
        self.moxie_bar = pygame.Rect(10, 150, 40, 250 - self.moxie_points)
        self.attack_time = 0
        self.let_attack = True
        self.deal_damage = False
        self.player_attack = True
        self.attack_cooldown = 0
        self.frog_HP = 150
        self.frog_health = pygame.Rect(self.enemy1.rect.x, self.enemy1.rect.y, self.frog_HP, 10)


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
                                self.player.rect.center[1], self.player.horiz_line, self.player.rect.x) 
                self.tongue.update(deltatime, player_action, self.enemy1.rect.centerx - 190, self.enemy1.rect.centery - 5, self.enemy1.attack)
                self.tongue2.update(deltatime, player_action, self.enemy1.rect.centerx -10, self.enemy1.rect.centery - 5, self.enemy1.attack)
                self.update_ultimate(deltatime, player_action)


                # For enemy1 and player damage response
                if self.take_damage == True:
                    self.attack_time += deltatime
                    self.let_attack = False
                    if self.attack_time > 1:
                        self.let_attack = True
                        self.take_damage = False
                        self.attack_time = 0
                if self.take_damage == False and not player_action["defend"]:
                    if self.enemy1.attack:
                            if pygame.sprite.spritecollide(self.player, self.tongue_group, False): #first check: rectangular collision
                                if pygame.sprite.spritecollide(self.player, self.tongue_group, False, pygame.sprite.collide_mask): #second check: mask collision
                                    if self.enemy1.current_anim_list == self.enemy1.attack_left:
                                        if any(self.tongue.rect.clipline(*line) for line in self.player.lines):
                                            self.healthpoints -= 20
                                            self.take_damage = True
                                    if self.enemy1.current_anim_list == self.enemy1.attack_right:
                                        if any(self.tongue2.rect.clipline(*line) for line in self.player.lines):
                                            self.healthpoints -= 20
                                            self.take_damage = True
                                            
                    if pygame.sprite.spritecollide(self.player, self.frog_group, False):
                        if any(self.enemy1.rect.clipline(*line) for line in self.player.lines):
                            if pygame.sprite.spritecollide(self.player, self.frog_group, False, pygame.sprite.collide_mask):
                                self.healthpoints -= 40
                                self.take_damage = True


                # for dealing damage to the enemies
                if self.deal_damage == True:
                    self.attack_cooldown += deltatime
                    self.player_attack = False
                    if self.attack_cooldown > 0.5:
                        self.player_attack = True
                        self.deal_damage = False
                        self.attack_cooldown = 0
                if self.player.attack == True and not self.deal_damage:
                    if pygame.sprite.spritecollide(self.player, self.frog_group, False): #first check: rectangular collision
                                if pygame.sprite.spritecollide(self.player, self.frog_group, False, pygame.sprite.collide_mask):
                                    if any(self.enemy1.rect.clipline(*line) for line in self.player.horiz_line):
                                        self.moxie_points += 25
                                        self.frog_HP -= 10
                                        self.deal_damage = True
                                    


                if self.healthpoints <= 0:
                    self.healthpoints += 250
                self.health_bar = pygame.Rect(10, 10, self.healthpoints, 40)
                self.moxie_bar = pygame.Rect(10, 150, 40, 250 - self.moxie_points)

            if player_action["ultimate"]:
                if self.moxie_points >= 250:
                    self.game.ult = True
                    if not(self.init_stan):
                        self.moxie_points = 0
                    else:
                        self.moxie_points = 250



            self.frog_health = pygame.Rect(self.enemy1.rect.x, self.enemy1.rect.y, self.frog_HP, 10)
            

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
        
        self.collision_render(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, "white", 500,150,200)

        pygame.draw.rect(display, "black", self.health_rect)
        pygame.draw.rect(display, "green", self.health_bar)

        pygame.draw.rect(display, "purple", self.moxie_rect)
        pygame.draw.rect(display, "black", self.moxie_bar)
        
        pygame.draw.rect(display, "black", (self.enemy1.rect.x, self.enemy1.rect.y, 150, 10))
        pygame.draw.rect(display, "green", self.frog_health)
        self.ultimate_display(display)


    





