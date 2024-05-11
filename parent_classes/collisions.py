import pygame
import time
from enemy1 import *
from torres import *


class Collisions():
    def __init__(self, game):
        self.game = game
        
    def load_for_collision(self):
        pass

    def enemy_collisions(self, deltatime, player_action, body_group, attack_group, 
                         enemy, enemy_damage, body_damage, attack_sprite1, attack_sprite2):
        
        self.cooldown_for_attacking(deltatime)

        # If player got attacked
        if self.player.take_damage == False and not player_action["defend"]:
            if enemy.attack:
                if pygame.sprite.spritecollide(self.player, attack_group, False): #first check: rectangular collision
                    if pygame.sprite.spritecollide(self.player, attack_group, False, pygame.sprite.collide_mask): #second check: mask collision
                        if enemy.current_anim_list == enemy.attack_left:
                            if any(attack_sprite1.rect.clipline(*line) for line in self.player.lines):
                                self.player.healthpoints -= enemy_damage
                                self.player.take_damage = True
                        if enemy.current_anim_list == enemy.attack_right:
                            if any(attack_sprite2.rect.clipline(*line) for line in self.player.lines):
                                self.player.healthpoints -= enemy_damage
                                self.player.take_damage = True
            # For any enemy body and player body collision damage
            if pygame.sprite.spritecollide(self.player, body_group, False):
                if any(enemy.rect.clipline(*line) for line in self.player.lines):
                    if pygame.sprite.spritecollide(self.player, body_group, False, pygame.sprite.collide_mask):
                        self.player.healthpoints -= body_damage
                        self.player.take_damage = True
            

        if self.player.attack == True and not self.player.deal_damage:
            if pygame.sprite.spritecollide(self.player, body_group, False): #first check: rectangular collision
                if pygame.sprite.spritecollide(self.player, body_group, False, pygame.sprite.collide_mask):
                    if any(enemy.rect.clipline(*line) for line in self.player.horiz_line):
                        self.player.moxiepoints += 25
                        enemy.HP -= self.player.attackpoints
                        self.player.deal_damage = True

    def flies_collisions(self, deltatime, player_action, body_group, attack_group, enemy, enemy_damage, body_damage):
        
        self.cooldown_for_attacking(deltatime)
         
        if self.player.take_damage == False and not player_action["defend"]:
            if enemy.attack:
                if pygame.sprite.spritecollide(self.player, attack_group, False): #first check: rectangular collision
                    if pygame.sprite.spritecollide(self.player, attack_group, False, pygame.sprite.collide_mask): #second check: mask collision
                        if any(enemy.rect.clipline(*line) for line in self.player.lines):
                            self.player.healthpoints -= enemy_damage
                            self.player.take_damage = True
                if pygame.sprite.spritecollide(self.player, body_group, False):
                    if any(enemy.rect.clipline(*line) for line in self.player.lines):
                        if pygame.sprite.spritecollide(self.player, body_group, False, pygame.sprite.collide_mask):
                            self.player.healthpoints -= body_damage
                            self.player.take_damage = True
                            
            if self.player.attack == True and not self.player.deal_damage:
                if pygame.sprite.spritecollide(self.player, body_group, False): #first check: rectangular collision
                    if pygame.sprite.spritecollide(self.player, body_group, False, pygame.sprite.collide_mask):
                        if any(enemy.rect.clipline(*line) for line in self.player.horiz_line):
                            self.player.moxiepoints += 25
                            enemy.HP -= self.player.attackpoints
                            self.player.deal_damage = True
    
    def minion_collisions(self, player_lines):
        for self.enemy3.minions in self.enemy3.minionlist.copy():
            if any(self.enemy3.minions.rect.clipline(*line) for line in player_lines):
                self.enemy3.minionlist.remove(self.enemy3.minions)
                self.enemy3.moxie_activate = True
                self.player.healthpoints -= self.enemy3.minions.damage
                self.player.moxiepoints += 10

     
    def cooldown_for_attacking(self, deltatime):
        # for dealing damage to the enemies (Player attacking)
        if self.player.deal_damage == True:
            self.player.attack_cooldown += deltatime
            if self.player.attack_cooldown > 0.3:
                self.player.deal_damage = False
                self.player.attack_cooldown = 0

    def cooldown_for_attacked(self, deltatime):
         # For enemy and player damage response
        if self.player.take_damage == True:
            self.player.attack_time += deltatime
            self.player.let_attack = False
            if self.player.attack_time > 1:
                self.player.let_attack = True
                self.player.take_damage = False
                self.player.attack_time = 0
