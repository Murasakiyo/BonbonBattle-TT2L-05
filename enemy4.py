import pygame
import time
import math
import random

class Enemy4(pygame.sprite.Sprite):
    def __init__(self, game, player_x, player_y):
        self.game = game
        self.rect_string1 = pygame.Rect(player_x - 25, self.game.screen_rect.midtop[1] - 600, 50, 600 )
        self.rect_string2 = pygame.Rect(self.game.screen_rect.midleft[0] - 1100, player_y - 25, 1100, 50 )
        self.pos_x, self.pos_y = 1050, 300
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 40, 40)
        # self.rect2 = pygame.Rect()
        self.positional = 6
        self.extend_count = 0
        self.extend_count2 = 0
        self.attack_bool = False
        self.attack_bool2 = False
        self.extend_vert = False
        self.extend_horiz = False
 
        self.super_attack = False
        self.super_count = 0
        self.super_timer = 0
        self.start_super_atk = False
        self.stop_moving = False

        self.atk_speed = 20
        self.move_speed = 5
        self.HP = 300
        self.moxie = 0
        self.aira_super = pygame.image.load("sprites/ult_aira.png")
        self.super_rect = self.aira_super.get_rect()


    def update(self, deltatime, player_action, player_x, player_y):
       
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        if not self.super_attack:
            self.normal_attack(deltatime, player_x, player_y)
            self.super_timer = 0


        self.placement(deltatime)
        if not self.start_super_atk:
            self.move_towards_position(self.pos_x, self.pos_y)






        if self.super_count > 4:
            self.super_attack = True
                    
        if self.super_attack:
            self.super_movement(player_x, player_y, deltatime)


        # print(self.super_timer)
        print(self.stop_moving)
        # print(self.super_attack)
        # print(self.super_count)


    def render(self, display):
        if not self.super_attack:
            pygame.draw.rect(display, "violet", self.rect_string1)
            pygame.draw.rect(display, "violet", self.rect_string2)
        pygame.draw.rect(display, "violet", self.rect)


        # pygame.Surface.blit(display, self.aira_super, (0, 0))




    def normal_attack(self, deltatime, player_x, player_y):
        if self.extend_vert == True:
            if self.attack_bool == False:
                if self.rect_string1.y <= 0:
                    self.rect_string1.y += 1 * self.atk_speed
                if self.rect_string1.y >= 0:
                    self.attack_bool = True

            if self.attack_bool == True:
                self.rect_string1.y -= 1 * self.atk_speed
                if self.rect_string1.y <= -600:
                    self.attack_bool = False
                    self.extend_vert = False

                    self.super_count += 1
            
        if self.extend_vert == False:
            self.extend_count += deltatime
            self.rect_string1.x = player_x - 25
            if self.extend_count > 4:
                self.extend_vert = True
                self.extend_count = 0

#####

        if self.extend_horiz == True:
            if self.attack_bool2 == False:
                if self.rect_string2.x <= 0:
                    self.rect_string2.x += 1 * self.atk_speed
                if self.rect_string2.x >= 0:
                    self.attack_bool2 = True

            if self.attack_bool2 == True:
                self.rect_string2.x -= 1 * self.atk_speed
                if self.rect_string2.x <= -1100:
                    self.attack_bool2 = False
                    self.extend_horiz = False

                    self.super_count += 1
            
        if self.extend_horiz == False:
            self.extend_count2 += deltatime
            self.rect_string2.y = player_y - 25
            if self.extend_count2 > 2:
                self.extend_horiz = True
                self.extend_count2 = 0

    def ultimate_attack(self, deltatime):
        pass
    

    def move_towards_position(self, pos_x, pos_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = pos_x - self.rect.x, pos_y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / (dist + 0.01), dy / (dist + 0.01)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.move_speed
        self.rect.y += dy * self.move_speed

        # print(self.rect.x)

    def super_movement(self, player_x, player_y, deltatime):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player_x - self.rect.x, player_y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / (dist + 1), dy / (dist + 1)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.move_speed
        self.rect.y += dy * self.move_speed


        if self.rect.x < 551: # To determine the rect position is already at center
            self.stop_moving = True
        
        if self.stop_moving:
            self.super_timer += deltatime
            if self.super_timer > 0.5:
                self.start_super_atk = True
            if self.super_timer > 10:
                self.super_count = 0
                self.start_super_atk = False
                self.super_attack = False
                self.stop_moving = False


    def placement(self, deltatime):

        if not self.super_attack:
            self.positional = 6

        if self.super_attack and not self.super_count == 0:
            self.positional = 1
            # if self.start_super_atk == True:
            #     self.move_speed = 5

        if self.positional == 6:
            self.pos_x, self.pos_y = 1050, 300 # default position

        if self.positional == 5: # 10, 50
            self.pos_x, self.pos_y = 1050, 300 # top left

        if self.positional == 4:
            self.pos_x, self.pos_y = 10, 550 # bottom left

        if self.positional == 3:
            self.pos_x, self.pos_y = 1050, 10 # top right

        if self.positional == 2:
            self.pos_x, self.pos_y = 1050, 550 # bottom right

        if self.positional == 1: # center
            self.pos_x, self.pos_y = self.game.screen_rect.centerx, self.game.screen_rect.centery