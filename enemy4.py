import pygame
import math
from AiraLyra import *

class Enemy4(pygame.sprite.Sprite):
    def __init__(self, game, player_x, player_y):
        self.game = game
        self.horiz_string = Horiz_hand(self.game, player_y)
        self.vert_string = Vert_hand(self.game, player_x)
       

        self.aira = Aira(self.game)
        self.lyra = Lyra(self.game)
        self.twin_ult = Twin_ult(self.game)

        self.airaspin_posx, self.airaspin_posy = self.game.screen_rect.centerx, self.game.screen_rect.centery
        self.lyraspin_posx, self.lyraspin_posy = self.game.screen_rect.centerx, self.game.screen_rect.centery


        self.positional = 6              # Positional is a variable telling aira and lyra where to move during an instance of their attack
        self.spin_positional = 0
        self.extend_count = 0            # Extend_counts are for timing how long before the string extends to attack the player while retracted 
        self.extend_count2 = 0
        self.attack_bool = False         # Attack_bools help state when the strings are currently extending or retracting to avoid overlap in the attack code
        self.attack_bool2 = False        

        self.extend_vert = False         # extend bools here are for telling whether the strings are supposed to extend/retract or track player position
        self.extend_horiz = False        # They're used to tell the strings to stop following the player_pos as this happens when its retracted outside of the game screen
 
        # New variables for animation
        self.idle = False
        self.idle_countdown = 0
        self.norm_attack = False
        self.spin = False


        self.super_attack = False        # This is when the super attack is starting to initiate (Aira/Lyra getting ready in positions)
        self.super_count = 0             # A pointer system to count up towards the super attack initiation
        self.super_timer = 0             # A timer for the duration of the super attack
        self.start_super_atk = False     # This is to tell when Aira/Lyra should start spinning 
        self.stop_moving = False         # This is for telling the Aira/Lyra rects to stop moving and blitting in the game as the spinning attack uses a different rect
        self.change_spin_pos_timer = 0   # This timer is for lyra's spin where she goes to different positions in the game based on time intervals

        self.ult_attack = False          # This is when the ultimate is starting to initiate (Aira/Lyra getting ready in positions)
        self.ult_timer = 0               # The timer for the duration of the ultimate attack
        self.start_ult_atk = False       # To begin the ultimate attack
        self.stop_super_atk = False      # To temporarily halt the super attack in lieu of the ultimate attack
        self.stop_normal_atk = False     # To temporarily halt the normal attack in lieu of the ultimate attack
        
        self.atk_speed = 20              # speed for strings
        self.move_speed = 0              # speed for aira/lyra movements
        self.spin_speed_lyra = 8         # Lyra's spin is the one moving around the screen
        self.spin_speed_aira = 5         # Aira's spin is the one following the player
        self.movement_timer = 0          # This is for changing their movement speeds for fixing the weird jitters that the movement code causes
        self.HP = 1000
        self.max_HP = self.HP
        self.moxie = 0
        self.max_moxie = 200

        self.string_damage = 20
        self.ult_damage = 80
        self.body_damage = 30

        self.go_middle = False
        self.heal = False


    def update(self, deltatime, player_action, player_x, player_y, death):
        self.aira.update(deltatime, self.idle, self.norm_attack, self.positional, self.start_super_atk, death)
        self.lyra.update(deltatime, self.idle, self.norm_attack, self.positional, self.start_super_atk, death)
        self.horiz_string.animate(deltatime)
        self.vert_string.animate(deltatime)

        if self.start_ult_atk:
            self.twin_ult.update(deltatime, self.start_ult_atk)
        self.twin_ult.anim_reset(self.start_ult_atk)

        # Death settings for variables
        if self.HP <= 0:
            self.HP = 0
            self.super_attack = False
            self.start_super_atk = False
            self.ult_attack = False
            self.start_ult_atk = False
            self.go_middle = True
            if self.go_middle:
                self.move_speed = 10

            if not self.aira.rect.centerx <= 540 and not self.aira.rect.centerx >= 560:
                self.move_speed = 0
                self.go_middle = False
            
        if self.moxie <= 0:
            self.moxie = 0


        # This code is for setting their speeds to 0 to fix the weird jitters with the sprite movement code
        if not(self.ult_attack) and not(self.HP <= 0):
            self.movement_timer += deltatime
            if self.movement_timer < 1.5:
                self.move_speed = 8
            if self.movement_timer > 0.95:
                self.move_speed = 0
            if self.go_middle:
                self.move_speed = 5
            
        if self.ult_attack:
            self.move_speed = 16

        
        if not self.super_attack and not self.stop_normal_atk:
            self.norm_attack = True

        if self.norm_attack:
            self.normal_attack(deltatime, player_x, player_y)
            self.super_timer = 0

        # Resetting string positions during a special atk phase
        if self.stop_normal_atk or self.super_attack:
            self.norm_attack = False
            self.vert_string.rect.y = -601
            self.horiz_string.rect.x = -1101

        self.placement(deltatime)

        # Super attack codes
        if not self.start_super_atk:
            self.move_towards_position(self.lyra_posx, self.lyra_posy, self.aira_posx, self.aira_posy)


        # Before spin attack, can use for animation
        if self.super_count > 4:
            self.move_speed = 8
            self.spin_speed_aira = 8
            self.norm_attack = False
            self.super_attack = True
        
        # Initiate Super movement
        if self.super_attack and not self.stop_super_atk:
            self.super_movement(player_x, player_y, deltatime)
        else: 
            self.spin = False

        if self.heal:
            self.HP += 50
            self.heal = False
    
        # Ultimate Attack Codes
        if not(self.HP <= 0):
            if not self.ult_attack and not self.super_attack:
                self.moxie += deltatime * 5

            if self.moxie >= 150:
                self.super_count = 0
                self.stop_super_atk = True

            if self.moxie >= 198:
                self.stop_normal_atk = True

            if self.moxie >= 200:
                self.ult_attack = True
                self.moxie = 0

            if self.ult_attack:
                self.ultimate_attack(deltatime)


    def render(self, display):
        # if not(self.start_ult_atk):
        #     self.aira.render(display)
        #     self.lyra.render(display)

        if not self.super_attack:
            self.horiz_string.render(display)
            self.vert_string.render(display)

        if self.start_ult_atk:
            self.twin_ult.render(display)


    def normal_attack(self, deltatime, player_x, player_y):

        if not(self.HP <= 0):
            # Once the timer for player tracking ends, the strings will extend and retract following these codes
            if self.extend_vert == True: # This code is for the extension of the strings
                if self.attack_bool == False:
                    if self.vert_string.rect.y <= 0:
                        self.vert_string.rect.y += 1 * self.atk_speed
                    if self.vert_string.rect.y >= 0:
                        self.game.offset = self.game.screen_shake(1,10,30)
                        self.game.sounds.screen_shake.play()
                        self.attack_bool = True

                if self.attack_bool == True: # This code is for the retraction of the strings
                    self.vert_string.rect.y -= 1 * self.atk_speed
                    if self.vert_string.rect.y <= -600:
                        self.attack_bool = False
                        self.extend_vert = False

                        self.super_count += 1
                

            # This patch of code is for the strings to track the player pos once it fully retracts from the game screen
            if self.extend_vert == False:
                self.extend_count += deltatime
                self.vert_string.rect.x = player_x - 25
                if self.extend_count > 4:
                    self.extend_vert = True
                    self.extend_count = 0

    #####
            # Once the timer for player tracking ends, the strings will extend and retract following these codes
            if self.extend_horiz == True: # This code is for the extension of the strings
                if self.attack_bool2 == False:
                    if self.horiz_string.rect.x <= 0:
                        self.horiz_string.rect.x += 1 * self.atk_speed
                    if self.horiz_string.rect.x >= 0:
                        self.game.offset = self.game.screen_shake(1,10,30)
                        self.attack_bool2 = True

                if self.attack_bool2 == True: # This code is for the retraction of the strings 
                    self.horiz_string.rect.x -= 1 * self.atk_speed
                    if self.horiz_string.rect.x <= -1100:
                        self.attack_bool2 = False
                        self.extend_horiz = False

                        self.super_count += 1
            
            # This patch of code is for the strings to track the player pos once it fully retracts from the game screen
            if self.extend_horiz == False:
                self.extend_count2 += deltatime
                self.horiz_string.rect.y = player_y - 25
                if self.extend_count2 > 2:
                    self.extend_horiz = True
                    self.extend_count2 = 0



# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def ultimate_attack(self, deltatime):

        if not(self.HP <= 0):
            if self.lyra.rect.centerx < 651:
                self.stop_moving = True

            if self.stop_moving:
                self.ult_timer += deltatime
                self.movement_timer = 0
                if self.ult_timer > 0.1:
                    self.start_ult_atk = True
                if self.ult_timer > 3:
                    self.start_ult_atk = False
                    self.stop_moving = False
                    self.stop_normal_atk = False
                    self.stop_super_atk = False
                    self.ult_timer = 0
                    self.ult_attack = False


    

    def move_towards_position(self, lyrapos_x, lyrapos_y, airapos_x, airapos_y):
        #  (Lyra's position)
        dx_lyra, dy_lyra = lyrapos_x - self.lyra.rect.centerx, lyrapos_y - self.lyra.rect.centery
        dist_lyra = math.hypot(dx_lyra, dy_lyra)
        dx_lyra, dy_lyra = dx_lyra / (dist_lyra + 0.01), dy_lyra / (dist_lyra + 0.01)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.lyra.rect.x += dx_lyra * self.move_speed
        self.lyra.rect.y += dy_lyra * self.move_speed



        #  (Aira's Position)
        dx_aira, dy_aira = airapos_x - self.aira.rect.centerx, airapos_y - self.aira.rect.centery
        dist_aira = math.hypot(dx_aira, dy_aira)
        dx_aira, dy_aira = dx_aira / (dist_aira + 0.01), dy_aira / (dist_aira + 0.01)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.aira.rect.x += dx_aira * self.move_speed
        self.aira.rect.y += dy_aira * self.move_speed

        if not self.moxie > 190 and not(self.HP <= 0):
            if self.positional == 1:
                self.go_middle = True
                if self.aira.rect.centerx >= 450:
                    self.go_middle = False
                    self.move_speed = 0
                    self.aira.rect.centerx = 450
                if self.lyra.rect.centerx <= 650:
                    self.go_middle = False
                    self.move_speed = 0
                    self.lyra.rect.centerx = 650
                    self.spin = True

        if self.HP <= 0:
            if self.positional == 1:
                self.go_middle = True
                if self.aira.rect.centerx == 550:
                    self.go_middle = False
                    self.move_speed = 0
                    self.aira.rect.centerx = 550

        if self.positional == 6:
            if self.aira.rect.x < 30:
                self.aira.rect.x = 30
            if self.lyra.rect.x > 930:
                self.lyra.rect.x = 930

        
        



    def super_movement(self, player_x, player_y, deltatime):

        if not(self.HP <= 0):
            # Find direction vector (dx, dy) between enemy and player.
            if self.start_super_atk:
                pos_x = player_x
                pos_y = player_y 
                dx, dy = pos_x - self.aira.rect.centerx, pos_y - self.aira.rect.centery
                dx2, dy2 = self.lyraspin_posx - self.lyra.rect.centerx, self.lyraspin_posy - self.lyra.rect.centery
                # self.spin = True

            if not self.start_super_atk:
                pos_x = self.game.screen_rect.centerx
                pos_y = self.game.screen_rect.centery
                dx, dy = pos_x - self.aira.rect.centerx, pos_y - self.aira.rect.centery
                dx2, dy2 = pos_x - self.lyra.rect.centerx, pos_y - self.lyra.rect.centery

            dist = math.hypot(dx, dy)
            dist2 = math.hypot(dx2, dy2)
            dx, dy = dx / (dist + 1), dy / (dist + 1)  # Normalize.
            dx2, dy2 = dx2 / (dist2 + 1), dy2 / (dist2 + 1) 
            # Move along this normalized vector towards the player at current speed.
            self.aira.rect.x += dx * self.spin_speed_aira
            self.aira.rect.y += dy * self.spin_speed_aira

            self.lyra.rect.x += dx2 * self.spin_speed_lyra
            self.lyra.rect.y += dy2 * self.spin_speed_lyra


            if self.lyra.rect.centerx < 651: # To determine the rect position is already at center
                
                self.stop_moving = True
                self.spin_speed_aira = 5
                self.super_count = 1

            
            if self.stop_moving:
                self.super_timer += deltatime
                self.movement_timer = 0
                
                if self.super_timer > 0.55:
                    self.start_super_atk = True
                if self.super_timer > 10:
                    self.super_count = 0
                    self.start_super_atk = False
                if self.super_timer > 12:
                    self.heal = True
                    self.super_attack = False
                    self.stop_moving = False


    def placement(self, deltatime):

        if not self.super_attack and not self.ult_attack:
            self.positional = 6
            self.change_spin_pos_timer = 0

        if self.HP <= 0:
            self.positional = 1

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


        # Call the positional variable
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

        # if self.positional == 0: # center
        #     self.lyra_posx, self.lyra_posy = self.game.screen_rect.centerx, self.game.screen_rect.centery
        #     self.aira_posx, self.aira_posy = self.game.screen_rect.centerx, self.game.screen_rect.centery


    def enemy_reset(self):
        self.aira.image = self.aira.idle_sprites[0]
        self.lyra.image = self.lyra.idle_sprites[0]

        self.HP = 1000
        self.moxie = 0

        self.aira.rect.x, self.aira.rect.y = 30, 200
        self.lyra.rect.x, self.lyra.rect.y = 930, 200

        self.positional = 6              
        self.spin_positional = 0
        self.extend_count = 0           
        self.extend_count2 = 0
        self.attack_bool = False         
        self.attack_bool2 = False        

        self.extend_vert = False   
        self.extend_horiz = False     
        self.horiz_string.rect.x, self.horiz_string.rect.y = self.game.screen_rect.midleft[0] - 1100 - 25, 200 - 25
        self.vert_string.rect.x, self.vert_string.rect.y = (450 - 25), self.game.screen_rect.midtop[1] - 600

        self.idle = False
        self.idle_countdown = 0
        self.norm_attack = False
        self.spin = False

        self.super_attack = False        
        self.super_count = 0             
        self.super_timer = 0             
        self.start_super_atk = False    
        self.stop_moving = False         
        self.change_spin_pos_timer = 0   

        self.ult_attack = False          
        self.ult_timer = 0              
        self.start_ult_atk = False      
        self.stop_super_atk = False      
        self.stop_normal_atk = False

        self.move_speed = 0              
        self.spin_speed_lyra = 8         
        self.spin_speed_aira = 5

        self.go_middle = False  
