import pygame
import time
from enemy1 import *
from torres import *

################# When using this parent class, u need a package of this codes in the init function of the level to run ########################

                                                    # self.take_damage = False
                                                    # self.attack_time = 0
                                                    # self.let_attack = True
                                                    # self.deal_damage = False
                                                    # self.attack_cooldown = 0

################################################################################################################################################

class Collisions():
    def __init__(self, game):
        self.game = game
        
    def load_for_collision(self):
        pass

    def enemy_collisions(self, deltatime, player_action, body_group, attack_group, 
                         enemy, enemy_damage, body_damage, attack_sprite1, attack_sprite2, activate_code):
        # For enemy and player damage response
        if self.take_damage == True:
            self.attack_time += deltatime
            self.let_attack = False
            if self.attack_time > 1:
                self.let_attack = True
                self.take_damage = False
                self.attack_time = 0
        if self.take_damage == False and not player_action["defend"]:
            if activate_code == True:
                if enemy.attack:
                        if pygame.sprite.spritecollide(self.player, attack_group, False): #first check: rectangular collision
                            if pygame.sprite.spritecollide(self.player, attack_group, False, pygame.sprite.collide_mask): #second check: mask collision
                                if enemy.current_anim_list == enemy.attack_left:
                                    if any(attack_sprite1.rect.clipline(*line) for line in self.player.lines):
                                        self.player.healthpoints -= enemy_damage
                                        self.take_damage = True
                                        print("hit")
                                if enemy.current_anim_list == enemy.attack_right:
                                    if any(attack_sprite2.rect.clipline(*line) for line in self.player.lines):
                                        self.player.healthpoints -= enemy_damage
                                        self.take_damage = True
                                        print("hit")
            if activate_code == False:
                # For any enemy body and player body collision damage
                if pygame.sprite.spritecollide(self.player, body_group, False):
                    if any(enemy.rect.clipline(*line) for line in self.player.lines):
                        if pygame.sprite.spritecollide(self.player, body_group, False, pygame.sprite.collide_mask):
                            self.player.healthpoints -= body_damage
                            self.take_damage = True


        # for dealing damage to the enemies
        if self.deal_damage == True:
            self.attack_cooldown += deltatime
            if self.attack_cooldown > 1:
                self.deal_damage = False
                self.attack_cooldown = 0

        if self.player.attack == True and not self.deal_damage:
            if pygame.sprite.spritecollide(self.player, body_group, False): #first check: rectangular collision
                        if pygame.sprite.spritecollide(self.player, body_group, False, pygame.sprite.collide_mask):
                            if any(enemy.rect.clipline(*line) for line in self.player.horiz_line):
                                self.player.moxiepoints += 25
                                enemy.HP -= self.player.attackpoints
                                self.deal_damage = True
        


