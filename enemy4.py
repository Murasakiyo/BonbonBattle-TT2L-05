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
        self.positional = random.randrange(1, 6)
        self.extend_count = 0
        self.extend_count2 = 0
        self.super_count = 0
        self.super_timer = 0
        self.change_pos_timer = 0
        self.ult_timer = 0
        self.test_bool = False
        self.test_bool2 = False
        self.extend_vert = False
        self.extend_horiz = False
        self.super_attack = False
        self.super_check = False
        self.string_check1 = True
        self.string_check2 = True
        self.ultimate = False
        self.ult_check = False
        self.move_bool = True
        self.speed = 20
        self.move_speed = 5
        self.HP = 300
        self.moxie = 0
        self.super_points = 0
        self.aira_super = pygame.image.load("sprites/ult_aira.png")
        self.super_rect = self.aira_super.get_rect()


    def update(self, deltatime, player_action, player_x, player_y):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        if not self.super_attack:
            self.string_extension(deltatime, player_x, player_y)
        self.placement(deltatime)

        if self.HP <= 150:
            if self.super_points >= 5 and self.ult_check == False:
                self.super_timer += deltatime
                self.super_check = True
                if self.super_timer > 5:
                    self.super_attack = True
                    self.super_points = 0
                    self.super_timer = 0
                    
        if self.super_attack:
            self.string_extension2(deltatime)

        if self.move_bool:
            self.move_towards_player(self.pos_x, self.pos_y)        
    

        if self.moxie >= 100:
            self.ultimate = True

        if self.ultimate:
            self.ult_timer += deltatime
            self.ult_check = True
            if self.ult_timer > 5:
                self.move_bool = False
                self.ultimate_movement(player_x, player_y)
            if self.ult_timer > 15:
                self.moxie = 0
                self.move_bool = True
                self.ult_check = False
                self.ultimate = False
                self.ult_timer = 0







        # print(self.positional)
        # print(self.string_check1)
        # print(self.super_points)
        # print(self.ult_timer)
        # print(self.HP)
        # print(self.super_points)
        print(self.extend_count)


    def render(self, display):
        if not self.super_check and not self.ult_check:
            pygame.draw.rect(display, "violet", self.rect_string1)
            pygame.draw.rect(display, "violet", self.rect_string2)
        pygame.draw.rect(display, "violet", self.rect)

        if self.super_attack:
            pygame.Surface.blit(display, self.aira_super, (0, 0))




    def string_extension(self, deltatime, player_x, player_y):
        if self.extend_vert == True:
            if self.test_bool == False:
                if self.rect_string1.y <= 0:
                    self.rect_string1.y += 1 * self.speed
                if self.rect_string1.y >= 0:
                    self.test_bool = True
                    self.string_check1 = True

            if self.test_bool == True:
                self.rect_string1.y -= 1 * self.speed
                if self.rect_string1.y <= -600:
                    self.test_bool = False
                    self.extend_vert = False
                    self.string_check2 = False
            
        if self.extend_vert == False and self.super_check == False and self.ult_check == False:
            self.extend_count += deltatime
            self.rect_string1.x = player_x - 25
            if self.extend_count > 4:
                self.extend_vert = True
                self.extend_count = 0

#####

        if self.extend_horiz == True:
            if self.test_bool2 == False:
                if self.rect_string2.x <= 0:
                    self.rect_string2.x += 1 * self.speed
                if self.rect_string2.x >= 0:
                    self.test_bool2 = True
                    self.string_check2 = True

            if self.test_bool2 == True:
                self.rect_string2.x -= 1 * self.speed
                if self.rect_string2.x <= -1100:
                    self.test_bool2 = False
                    self.extend_horiz = False
                    self.string_check1 = False
            
        if self.extend_horiz == False and self.super_check == False and self.ult_check == False:
            self.extend_count2 += deltatime
            self.rect_string2.y = player_y - 25
            if self.extend_count2 > 2:
                self.extend_horiz = True
                self.extend_count2 = 0

    def string_extension2(self, deltatime):
        self.super_count += deltatime
        if self.super_count > 8 and self.ult_check == False:
            self.super_count = 0
            self.super_check = False
            self.super_attack = False
                # self.string_check1 = True
                # self.string_check2 = True
    

    def move_towards_player(self, pos_x, pos_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = pos_x - self.rect.x, pos_y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / (dist + 0.01), dy / (dist + 0.01)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.move_speed
        self.rect.y += dy * self.move_speed

        # print(self.rect.x)

    def ultimate_movement(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player_x - self.rect.x, player_y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / (dist + 1), dy / (dist + 1)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.move_speed
        self.rect.y += dy * self.move_speed


    def placement(self, deltatime):
        # self.change_pos_timer += deltatime
        # if self.change_pos_timer > 3:
        self.positional = 1
            # self.change_pos_timer = 0

        if self.ultimate:
            self.positional = 5

        if self.super_check:
            self.positional = 4

        if self.positional == 1: # 10, 50
            self.pos_x, self.pos_y = 1050, 300 # top left

        if self.positional == 2:
            self.pos_x, self.pos_y = 10, 550 # bottom left

        if self.positional == 3:
            self.pos_x, self.pos_y = 1050, 10 # top right

        if self.positional == 4:
            self.pos_x, self.pos_y = 1050, 550 # bottom right

        if self.positional == 5:
            self.pos_x, self.pos_y = self.game.screen_rect.centerx, self.game.screen_rect.centery