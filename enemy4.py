import pygame
import math
import random
from AiraLyra import *

class Enemy4(pygame.sprite.Sprite):
    def __init__(self, game, player_x, player_y):
        self.game = game
        self.vert_string = pygame.Rect(player_x - 25, self.game.screen_rect.midtop[1] - 600, 50, 600 )
        self.horiz_string = pygame.Rect(self.game.screen_rect.midleft[0] - 1100, player_y - 25, 1100, 50 )

        self.aira = Aira(self.game)
        self.lyra = Lyra(self.game)

        # self.aira_posx, self.aira_posy = 50, 300
        # self.lyra_posx, self.lyra_posy = 1050, 300
        # self.airaspin_posx, self.airaspin_posy = self.game.screen_rect.centerx, self.game.screen_rect.centery
        # self.lyraspin_posx, self.lyraspin_posy = self.game.screen_rect.centerx, self.game.screen_rect.centery
        # self.aira_rect = pygame.Rect(self.aira_posx, self.aira_posy, 40, 40)
        # self.lyra_rect = pygame.Rect(self.lyra_posx, self.lyra_posy, 40, 40)
        self.aira_spin = pygame.Rect(self.airaspin_posx, self.airaspin_posy, 40, 40)
        self.lyra_spin = pygame.Rect(self.lyraspin_posx, self.lyraspin_posy, 40, 40)

        self.positional = 6              # Positional is a variable telling aira and lyra where to move during an instance of their attack
        self.spin_positional = 0
        self.extend_count = 0            # Extend_counts are for timing how long before the string extends to attack the player while retracted 
        self.extend_count2 = 0
        self.attack_bool = False         # Attack_bools help state when the strings are currently extending or retracting to avoid overlap in the attack code
        self.attack_bool2 = False        

        self.extend_vert = False         # extend bools here are for telling whether the strings are supposed to extend/retract or track player position
        self.extend_horiz = False        # They're used to tell the strings to stop following the player_pos as this happens when its retracted outside of the game screen
 
        self.super_attack = False        # This is when the super attack is starting to initiate (Aira/Lyra getting ready in positions)
        self.super_count = 0             # A pointer system to count up towards the super attack initiation
        self.super_timer = 0             # A timer for the duration of the super attack
        self.start_super_atk = False     # This is to tell when Aira/Lyra should start spinning 
        self.stop_moving = False         # This is for telling the Aira/Lyra rects to stop moving and blitting in the game as the spinning attack uses a different rect
        self.change_spin_pos_timer = 0

        self.ult_attack = False          # This is when the ultimate is starting to initiate (Aira/Lyra getting ready in positions)
        self.ult_timer = 0               # The timer for the duration of the ultimate attack
        self.start_ult_atk = False       # To begin the ultimate attack
        self.stop_super_atk = False      # To temporarily halt the super attack in lieu of the ultimate attack
        self.stop_normal_atk = False     # To temporarily halt the normal attack in lieu of the ultimate attack
        
        self.atk_speed = 20              # speed for strings
        self.move_speed = 8              # speed for aira/lyra movements
        self.spin_speed_lyra = 8         # Lyra's spin is the one moving around the screen
        self.spin_speed_aira = 5         # Aira's spin is the one following the player
        self.HP = 300
        self.moxie = 0
        self.ultimate_image = pygame.image.load("sprites/ult_aira.png")
        self.ult_rect = self.ultimate_image.get_rect()


    def update(self, deltatime, player_action, player_x, player_y):
       
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]


        if not self.super_attack and not self.stop_normal_atk:
            self.normal_attack(deltatime, player_x, player_y)
            self.super_timer = 0

        # Resetting string positions during a special atk phase
        if self.stop_normal_atk or self.super_attack:
            self.vert_string.y = -601
            self.horiz_string.x = -1101

        self.placement(deltatime)

        # Super attack codes
        if not self.start_super_atk:
            self.move_towards_position(self.lyra_posx, self.lyra_posy, self.aira_posx, self.aira_posy)

        if self.super_count > 4:
            self.super_attack = True
                    
        if self.super_attack and not self.stop_super_atk:
            self.super_movement(player_x, player_y, deltatime)


        # Ultimate Attack Codes
        if not self.ult_attack and not self.super_attack:
            self.moxie += deltatime * 5

        if self.moxie >= 250:
            self.super_count = 0
            self.stop_super_atk = True

        if self.moxie >= 280:
            self.stop_normal_atk = True

        if self.moxie >= 300:
            self.ult_attack = True
            self.moxie = 0

        if self.ult_attack:
            self.ultimate_attack(deltatime)

        # print(self.super_timer)
        # print(self.start_super_atk)
        # print(self.super_attack)
        # print(self.super_count)
        # print(self.moxie)
        # print(pygame.mouse.get_pos())
        print(self.spin_positional)


    def render(self, display):
        if not self.super_attack:
            pygame.draw.rect(display, "violet", self.vert_string)
            pygame.draw.rect(display, "violet", self.horiz_string)


        if self.stop_moving and not self.ult_attack:
            pygame.draw.rect(display, "black", self.aira_spin)
            pygame.draw.rect(display, "black", self.lyra_spin)


        if not self.stop_moving:
            pygame.draw.rect(display, "pink", self.aira.rect)
            pygame.draw.rect(display, "violet", self.lyra.rect)

        if self.start_ult_atk:
            pygame.Surface.blit(display, self.ultimate_image, (0, 0))




    def normal_attack(self, deltatime, player_x, player_y):
        if self.extend_vert == True:
            if self.attack_bool == False:
                if self.vert_string.y <= 0:
                    self.vert_string.y += 1 * self.atk_speed
                if self.vert_string.y >= 0:
                    self.attack_bool = True

            if self.attack_bool == True:
                self.vert_string.y -= 1 * self.atk_speed
                if self.vert_string.y <= -600:
                    self.attack_bool = False
                    self.extend_vert = False

                    self.super_count += 1
            
        if self.extend_vert == False:
            self.extend_count += deltatime
            self.vert_string.x = player_x - 25
            if self.extend_count > 4:
                self.extend_vert = True
                self.extend_count = 0

#####

        if self.extend_horiz == True:
            if self.attack_bool2 == False:
                if self.horiz_string.x <= 0:
                    self.horiz_string.x += 1 * self.atk_speed
                if self.horiz_string.x >= 0:
                    self.attack_bool2 = True

            if self.attack_bool2 == True:
                self.horiz_string.x -= 1 * self.atk_speed
                if self.horiz_string.x <= -1100:
                    self.attack_bool2 = False
                    self.extend_horiz = False

                    self.super_count += 1
            
        if self.extend_horiz == False:
            self.extend_count2 += deltatime
            self.horiz_string.y = player_y - 25
            if self.extend_count2 > 2:
                self.extend_horiz = True
                self.extend_count2 = 0





    def ultimate_attack(self, deltatime):

        if self.lyra.rect.x < 551:
            self.stop_moving = True

        if self.stop_moving:
            self.ult_timer += deltatime
            if self.ult_timer > 0.5:
                self.start_ult_atk = True
            if self.ult_timer > 5:
                self.start_ult_atk = False
                self.stop_moving = False
                self.stop_normal_atk = False
                self.stop_super_atk = False
                self.ult_timer = 0
                self.ult_attack = False


    

    def move_towards_position(self, lyrapos_x, lyrapos_y, airapos_x, airapos_y):
        #  (Lyra's position)
        dx_lyra, dy_lyra = lyrapos_x - self.lyra.rect.x, lyrapos_y - self.lyra.rect.y
        dist = math.hypot(dx_lyra, dy_lyra)
        dx_lyra, dy_lyra = dx_lyra / (dist + 0.01), dy_lyra / (dist + 0.01)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.lyra.rect.x += dx_lyra * self.move_speed
        self.lyra.rect.y += dy_lyra * self.move_speed

        #  (Aira's Position)
        dx_aira, dy_aira = airapos_x - self.aira.rect.x, airapos_y - self.aira.rect.y
        dist = math.hypot(dx_aira, dy_aira)
        dx_aira, dy_aira = dx_aira / (dist + 0.01), dy_aira / (dist + 0.01)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.aira.rect.x += dx_aira * self.move_speed
        self.aira.rect.y += dy_aira * self.move_speed



    def super_movement(self, player_x, player_y, deltatime):
        # Find direction vector (dx, dy) between enemy and player.
        if self.start_super_atk:
            pos_x = player_x
            pos_y = player_y 
            dx, dy = pos_x - self.aira_spin.x, pos_y - self.aira_spin.y
            dx2, dy2 = self.lyraspin_posx - self.lyra_spin.x, self.lyraspin_posy - self.lyra_spin.y

        if not self.start_super_atk:
            pos_x = self.game.screen_rect.centerx
            pos_y = self.game.screen_rect.centery
            dx, dy = pos_x - self.aira_spin.x, pos_y - self.aira_spin.y
            dx2, dy2 = pos_x - self.lyra_spin.x, pos_y - self.lyra_spin.y

        dist = math.hypot(dx, dy)
        dist2 = math.hypot(dx2, dy2)
        dx, dy = dx / (dist + 1), dy / (dist + 1)  # Normalize.
        dx2, dy2 = dx2 / (dist2 + 1), dy2 / (dist2 + 1) 
        # Move along this normalized vector towards the player at current speed.
        self.aira_spin.x += dx * self.spin_speed_aira
        self.aira_spin.y += dy * self.spin_speed_aira

        self.lyra_spin.x += dx2 * self.spin_speed_lyra
        self.lyra_spin.y += dy2 * self.spin_speed_lyra


        if self.lyra.rect.x < 551: # To determine the rect position is already at center
            self.stop_moving = True
        
        if self.stop_moving:
            self.super_timer += deltatime
            if self.super_timer > 0.5:
                self.start_super_atk = True
            if self.super_timer > 10:
                self.super_count = 0
                self.start_super_atk = False
            if self.super_timer > 12:
                self.super_attack = False
                self.stop_moving = False
            



    def placement(self, deltatime):

        if not self.super_attack and not self.ult_attack:
            self.positional = 6
            self.change_spin_pos_timer = 0

        if self.super_attack and not self.super_count == 0:
            self.positional = 1

            self.change_spin_pos_timer += deltatime
            if self.change_spin_pos_timer >= 1:
                self.spin_positional = 2
            if self.change_spin_pos_timer >= 2:
                self.spin_positional = 4
            if self.change_spin_pos_timer >= 3:
                self.spin_positional = 3
            if self.change_spin_pos_timer >= 4:
                self.spin_positional = 5
            if self.change_spin_pos_timer >= 5:
                self.spin_positional = 2
            if self.change_spin_pos_timer >= 6:
                self.spin_positional = 5
            if self.change_spin_pos_timer >= 7:
                self.spin_positional = 3
            if self.change_spin_pos_timer >= 8:
                self.spin_positional = 4
            if self.change_spin_pos_timer >= 9:
                self.spin_positional = 5
            if self.change_spin_pos_timer >= 10:
                self.positional =2

        if self.ult_attack:
            self.positional = 1


        if self.positional == 6:
            self.lyra_posx, self.lyra_posy = 1050, 300 # default position
            self.aira_posx, self.aira_posy = 50, 300

        if self.spin_positional == 5: # 10, 50
            self.lyraspin_posx, self.lyraspin_posy = 917, 300 # right


        if self.spin_positional == 4:
            self.lyraspin_posx, self.lyraspin_posy = 183, 300 #  left


        if self.spin_positional == 3:
            self.lyraspin_posx, self.lyraspin_posy = 555, 100 # top 


        if self.spin_positional == 2:
            self.lyraspin_posx, self.lyraspin_posy = 555, 500 # bottom 


        if self.positional == 1: # center
            self.lyra_posx, self.lyra_posy = self.game.screen_rect.centerx, self.game.screen_rect.centery
            self.aira_posx, self.aira_posy = self.game.screen_rect.centerx, self.game.screen_rect.centery



# Just gonna write notes here for collisions later:
# During normal attack phase, only vertical and horizontal strings will deal damage
# During super attack phase, ensure only the spinning attack rect can deal damage and nothing else
# Consequently, during ultimate attack phase, ensure only the ultimate rects can deal damage and turn off everything else