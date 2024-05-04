import pygame
import time
import math
import spritesheet
import parent_classes.state as state
from minions import *

class Enemy3(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.rect_draw = pygame.Rect(180, 180, 40, 40)
        self.enemy3_rect = pygame.Rect(180, 180, 40, 40)
        self.enemyborder1 = pygame.Rect(-895, 40, 900, 570) #left
        self.enemyborder2 = pygame.Rect(1095, 40, 900, 570) #right
        self.enemyborder3 = pygame.Rect(0, 560, 1100, 370) #bottom
        self.enemyborder4 = pygame.Rect(0, -330, 1100, 370) #top         
        self.color = "white"
        self.speed = 0
        self.attractspeed = 0
        self.minionspeed = 0
        self.current_time = 0
        self.start_time = time.time()
        self.avoid = False
        self.minions = Minions(self.game, self.enemy3_rect.centerx, self.enemy3_rect.centery)
        self.minions2 = Minions2(self.game, self.enemy3_rect.centerx, self.enemy3_rect.centery)
        self.minions3 = Minions3(self.game, self.enemy3_rect.centerx, self.enemy3_rect.centery)
        self.minions4 = Minions4(self.game, self.enemy3_rect.centerx, self.enemy3_rect.centery)
        self.minionlist = pygame.sprite.Group()
        


    def update(self, deltatime, player_action, player_x, player_y, player_lines):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        self.enemy3_movement(player_x, player_y)
        self.move_towards_border()
        # self.minions_movement(player_x, player_y)
        self.enemy3_rect.clamp_ip(self.game.screen_rect)

        if pygame.Rect.colliderect(self.enemy3_rect, self.enemyborder1) == True:
            self.avoid = True

        if pygame.Rect.colliderect(self.enemy3_rect, self.enemyborder2) == True:
            self.avoid = True

        if pygame.Rect.colliderect(self.enemy3_rect, self.enemyborder3) == True:
            self.avoid = True

        if pygame.Rect.colliderect(self.enemy3_rect, self.enemyborder4) == True:
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
            self.speed = -4
            self.attractspeed = 0

        self.minion_spawn()   
        self.minionlist.update(deltatime, player_action, player_x, player_y)
        self.update_minions(player_lines)

        ################## Print zone #############################

        print(self.current_time)
        # print(self.minionlist)




    def render(self, display):
        pygame.draw.rect(display, self.color, self.enemy3_rect)
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

        for self.minions2 in self.minionlist.copy():
            if any(self.minions2.rect.clipline(*line) for line in player_lines):
                self.minionlist.remove(self.minions2)

        for self.minions3 in self.minionlist.copy():
            if any(self.minions3.rect.clipline(*line) for line in player_lines):
                self.minionlist.remove(self.minions3)

        for self.minions4 in self.minionlist.copy():
            if any(self.minions4.rect.clipline(*line) for line in player_lines):
                self.minionlist.remove(self.minions4)


    def minion_spawn(self):
        if len(self.minionlist) == 0:
                new_minion = Minions(self.game,self.enemy3_rect.x, self.enemy3_rect.y)
                self.minionlist.add(new_minion) 
                new_minion = Minions2(self.game,self.enemy3_rect.x, self.enemy3_rect.y)
                self.minionlist.add(new_minion) 
                new_minion = Minions3(self.game,self.enemy3_rect.x, self.enemy3_rect.y)
                self.minionlist.add(new_minion) 
                new_minion = Minions4(self.game,self.enemy3_rect.x, self.enemy3_rect.y)
                self.minionlist.add(new_minion) 

##############################################

    def enemy3_movement(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player_x - self.enemy3_rect.x, player_y - self.enemy3_rect.y
        dist = math.hypot(dx, dy)

        dx, dy = dx / (dist + 1), dy / (dist + 1)  # Normalize.

        if dist > 500:
            self.speed = 0

        # Move along this normalized vector towards the player at current speed.
        self.enemy3_rect.x += dx * self.speed
        self.enemy3_rect.y += dy * self.speed

    def move_towards_border(self):
        dx, dy = self.game.screen_rect.center[0] - self.enemy3_rect.x, self.game.screen_rect.center[1] - self.enemy3_rect.y
        dist = math.hypot(dx, dy)

        dx, dy = dx / (dist + 1), dy / (dist + 1)
        self.enemy3_rect.x += dx * self.attractspeed
        self.enemy3_rect.y += dy * self.attractspeed

    # def minions_movement(self, player_x, player_y):
    #     dx, dy = player_x - self.minions.rect.x, player_y - self.minions.rect.y
    #     dist = math.hypot(dx, dy)

    #     dx, dy = dx / (dist + 1), dy / (dist + 1)
    #     self.minions.rect.x += dx * self.minionspeed
    #     self.minions.rect.y += dy * self.minionspeed
        


      



