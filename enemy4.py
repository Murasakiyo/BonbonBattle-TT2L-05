import pygame
import time
import math
import random

class Enemy5(pygame.sprite.Sprite):
    def __init__(self, game, player_x, player_y):
        self.game = game
        self.rect_string1 = pygame.Rect(player_x - 25, self.game.screen_rect.midtop[1] - 600, 50, 600 )
        self.rect_string2 = pygame.Rect(self.game.screen_rect.midleft[0] - 1100, player_y - 25, 1100, 50 )
        self.pos_x, self.pos_y = 0, 0
        self.rect = pygame.Rect(self.pos_x, self.pos_y, 40, 40)
        self.positional = random.randrange(1, 6)
        self.extend_count = 0
        self.extend_count2 = 0
        self.change_pos_timer = 0
        self.test_bool = False
        self.test_bool2 = False
        self.extend_vert = False
        self.extend_horiz = False
        self.speed = 20
        self.move_speed = 5


    def update(self, deltatime, player_action, player_x, player_y):
       
        self.string_extension(deltatime, player_x, player_y)
        self.placement(deltatime)
        self.move_towards_player(self.pos_x, self.pos_y)




        # print(self.rect_string1.y)
        # print(self.extend_count)
        # print(self.positional)


    def render(self, display):
        pygame.draw.rect(display, "violet", self.rect_string1)
        pygame.draw.rect(display, "violet", self.rect_string2)
        pygame.draw.rect(display, "violet", self.rect)




    def string_extension(self, deltatime, player_x, player_y):
        if self.extend_vert == True:
            if self.test_bool == False:
                if self.rect_string1.y <= 0:
                    self.rect_string1.y += 1 * self.speed
                if self.rect_string1.y >= 0:
                    self.test_bool = True

            if self.test_bool == True:
                self.rect_string1.y -= 1 * self.speed
                if self.rect_string1.y <= -600:
                    self.test_bool = False
                    self.extend_vert = False
            
        if self.extend_vert == False:
            self.extend_count += deltatime
            self.rect_string1.x = player_x - 25
            if self.extend_count > 2:
                self.extend_vert = True
                self.extend_count = 0

#####

        if self.extend_horiz == True:
            if self.test_bool2 == False:
                if self.rect_string2.x <= 0:
                    self.rect_string2.x += 1 * self.speed
                if self.rect_string2.x >= 0:
                    self.test_bool2 = True

            if self.test_bool2 == True:
                self.rect_string2.x -= 1 * self.speed
                if self.rect_string2.x <= -1100:
                    self.test_bool2 = False
                    self.extend_horiz = False
            
        if self.extend_horiz == False:
            self.extend_count2 += deltatime
            self.rect_string2.y = player_y - 25
            if self.extend_count2 > 2:
                self.extend_horiz = True
                self.extend_count2 = 0
    

    def move_towards_player(self, pos_x, pos_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = pos_x - self.rect.x, pos_y - self.rect.y
        dist = math.hypot(dx, dy)
        dx, dy = dx / (dist + 0.01), dy / (dist + 0.01)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.move_speed
        self.rect.y += dy * self.move_speed

        print(self.rect.x)

    def placement(self, deltatime):
        self.change_pos_timer += deltatime
        if self.change_pos_timer > 3:
            self.positional = random.randrange(1, 5)
            self.change_pos_timer = 0

        if self.positional == 1:
            self.pos_x, self.pos_y = 10, 50 # top left

        if self.positional == 2:
            self.pos_x, self.pos_y = 10, 550 # bottom left

        if self.positional == 3:
            self.pos_x, self.pos_y = 1050, 10 # top right

        if self.positional == 4:
            self.pos_x, self.pos_y = 1050, 550 # bottom right

        if self.positional == 5:
            self.pos_x, self.pos_y = self.game.screen_rect.centerx, self.game.screen_rect.centery