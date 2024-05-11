import pygame
import time
import math
import spritesheet
from minions import *

class Enemy3(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.rect_draw = pygame.Rect(180, 180, 40, 40)
        self.rect = pygame.Rect(180, 180, 40, 40)
        self.enemyborder1 = pygame.Rect(-895, 40, 900, 570) #left
        self.enemyborder2 = pygame.Rect(1095, 40, 900, 570) #right
        self.enemyborder3 = pygame.Rect(0, 560, 1100, 370) #bottom
        self.enemyborder4 = pygame.Rect(0, -330, 1100, 370) #top         
        self.color = "white"
        self.speed = 0
        self.attractspeed = 0
        self.minionspeed = 0
        self.current_time = 0
        self.minion_time = 0
        self.collide_time = 0
        self.start_time = time.time()
        self.avoid = False
        self.collide = False
        self.moxie_activate = False
        self.minions = Minions(self.game, self.rect.centerx, self.rect.centery, speed=0)
        self.minionlist = pygame.sprite.Group()
        self.HP = 500
        self.damage = 0
        self.body_damage = 50
        self.attack = False
        


    def update(self, deltatime, player_action, player_x, player_y):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        self.enemy3_movement(player_x, player_y)
        self.move_towards_border()
        # self.minions_movement(player_x, player_y)
        self.rect.clamp_ip(self.game.screen_rect)

        if pygame.Rect.colliderect(self.rect, self.enemyborder1) == True:
            self.avoid = True

        if pygame.Rect.colliderect(self.rect, self.enemyborder2) == True:
            self.avoid = True

        if pygame.Rect.colliderect(self.rect, self.enemyborder3) == True:
            self.avoid = True

        if pygame.Rect.colliderect(self.rect, self.enemyborder4) == True:
            self.avoid = True

        if self.avoid == True:
            self.current_time += deltatime
            if self.current_time > 0.5:
                self.avoid = False
                self.current_time = 0

        if self.avoid == True:
            self.attractspeed = 8
            self.speed = 0
        elif self.avoid == False:
            self.speed = -4 # -4
            self.attractspeed = 0


        if self.moxie_activate == True:
            self.moxie_activate = False


        self.minion_spawn(deltatime)   
        self.minionlist.update(deltatime, player_action, player_x, player_y)
        # self.update_minions(player_lines)

    


        # if self.collide == True:
        #     self.collide_time += deltatime
        #     if self.collide_time > 0.1:
        #         p_move_x += 200 * deltatime * direction_x 
        #         p_move_y += 225 * deltatime * direction_y

        #     if self.collide_time > 3:
        #         self.collide_time = 0
        #         self.collide = False 



        ################## Print zone #############################

        # print(self.current_time)
        # print(self.minionlist)
        # print(p_move_x)
        # print(self.collide)




    def render(self, display):
        pygame.draw.rect(display, self.color, self.rect)
        # pygame.draw.rect(display, self.color, self.enemyborder1)
        # pygame.draw.rect(display, self.color, self.enemyborder2)
        # pygame.draw.rect(display, self.color, self.enemyborder3)
        # pygame.draw.rect(display, self.color, self.enemyborder4) #draws the enemy border for refference

        for self.minions in self.minionlist.sprites():
            self.minions.render(display)

        pygame.display.flip()

###########################################
    def update_minions(self, player_lines):
        for self.minions in self.minionlist.copy():
            if any(self.minions.rect.clipline(*line) for line in player_lines):
                self.minionlist.remove(self.minions)
                self.moxie_activate = True

        # if any(self.minions.rect.clipline(*line) for line in player_lines):
        #     self.collide = True

        for self.minions2 in self.minionlist.copy():
            if any(self.minions2.rect.clipline(*line) for line in player_lines):
                self.minionlist.remove(self.minions2)
                self.moxie_activate = True

        for self.minions3 in self.minionlist.copy():
            if any(self.minions3.rect.clipline(*line) for line in player_lines):
                self.minionlist.remove(self.minions3)
                self.moxie_activate = True

        for self.minions4 in self.minionlist.copy():
            if any(self.minions4.rect.clipline(*line) for line in player_lines):
                self.minionlist.remove(self.minions4)
                self.moxie_activate = True


    def minion_spawn(self, deltatime):
        if len(self.minionlist) == 0:
                self.minion_time += deltatime
                if self.minion_time > 3:
                    for i in range(3):
                        if i == 1:
                            new_minion = Minions(self.game, self.rect.centerx - 100, self.rect.centery, 1+(i * 1))
                            self.minionlist.add(new_minion)
                        if i == 2:
                            new_minion = Minions(self.game, self.rect.centerx + 100, self.rect.centery, 1+(i * 1))
                            self.minionlist.add(new_minion) 
                    for i in range(3, 5):
                        if i == 3:
                            new_minion = Minions(self.game, self.rect.centerx, self.rect.centery + 100, 1+(i * 1))
                            self.minionlist.add(new_minion)     
                        if i == 4:
                            new_minion = Minions(self.game, self.rect.centerx, self.rect.centery - 100, 1+(i * 1))
                            self.minionlist.add(new_minion)                      
                    self.minion_time = 0


##############################################

    def enemy3_moxie_function(self):
        if self.moxie_activate == True:
            pass


    def enemy3_movement(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player_x - self.rect.x, player_y - self.rect.y
        dist = math.hypot(dx, dy)

        dx, dy = dx / (dist + 1), dy / (dist + 1)  # Normalize.

        if dist > 500:
            self.speed = 0

        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

    def move_towards_border(self):
        dx, dy = self.game.screen_rect.center[0] - self.rect.x, self.game.screen_rect.center[1] - self.rect.y
        dist = math.hypot(dx, dy)

        dx, dy = dx / (dist + 1), dy / (dist + 1)
        self.rect.x += dx * self.attractspeed
        self.rect.y += dy * self.attractspeed

    # def minions_movement(self, player_x, player_y):
    #     dx, dy = player_x - self.minions.rect.x, player_y - self.minions.rect.y
    #     dist = math.hypot(dx, dy)

    #     dx, dy = dx / (dist + 1), dy / (dist + 1)
    #     self.minions.rect.x += dx * self.minionspeed
    #     self.minions.rect.y += dy * self.minionspeed
        


      



