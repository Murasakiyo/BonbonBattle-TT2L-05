import pygame
import spritesheet
import math
import random

class FlyEnemy(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.flies = Fly(self.game)
        self.flylist = pygame.sprite.Group()  # List of the flies
        # self.current_frame, self.current_frame_unique, self.last_frame_update = 0,0,0 #animation
        # self.fps = 0.2

    def update(self, deltatime, player_action, player_x, player_y, player_rect):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]
       
        self.flies.rect.clamp_ip(self.game.screen_rect)

        self.flies_spawn()
        for i, flies in enumerate(self.flylist.sprites()):
        #    print(f"Debug Update Fly {i}")
           flies.update(deltatime, player_action, player_x, player_y, player_rect)

        # self.avoid_rect(deltatime)


    def render(self, display):
        for self.flies in self.flylist.sprites():
            self.flies.render(display)

    # To avoid overlap among flies
    def avoid_rect(self, deltatime):  
        FACTOR = 20
        for follower in self.flylist.sprites():
            for target in self.flylist.sprites():
                if follower == target:
                    continue
                if pygame.Rect.colliderect(follower.rect, target.rect):
                    # print("Flies collide")
                    if follower.rect.centerx <= target.rect.centerx:    
                        follower.rect.right = target.rect.left - FACTOR   # Move left
                    if follower.rect.centerx > target.rect.centerx:
                        follower.rect.left = target.rect.right + FACTOR   # Move right
                    if follower.rect.centery <= target.rect.centery:
                        follower.rect.bottom = target.rect.top - FACTOR   # Move up
                    if follower.rect.centery > target.rect.centery:
                        follower.rect.top = target.rect.bottom + FACTOR   # Move down


    def flies_spawn(self):
        color_list = [(255,0,0), (0,255,0), (0,0,255)]
        if len(self.flylist) == 0:
            for i in range(3):
                new_fly = Fly(self, moving_speed=1+(i*2), color = color_list[i])
                self.flylist.add(new_fly)


    def animate(self, deltatime, direction_x, direction_y, distance):
        # self.last_frame_update += deltatime
        pass
    

    def load_sprites(self):
        self.left_sprites, self.right_sprites = [], []
        self.jump_left, self.jump_right = [], [] 
        self.attack_left, self.attack_right = [], []


class Fly(pygame.sprite.Sprite):
    def __init__(self, game, moving_speed=2, color=(0,255,0)):
        super().__init__()
        self.game = game
        random_x = random.randint(0, 1100)
        random_y = random.randint(0, 600)
        self.rect = pygame.Rect(random_x, random_y, 60, 60)
        self.color = color
        self.speed = 0   # Move towards player
        self.attractspeed = 0   # Move opposite direction
        self.current_time = 0      
        self.bigger_rect = self.rect.scale_by(1.5)
        self.avoid = False
        self.moving_speed = moving_speed
        self.attacking = False
        self.teleport_x = None
        self.teleport_y = None

    def update(self, deltatime, player_action, player_x, player_y, player_rect):
        # direction_x = player_action["right"] - player_action["left"]
        # direction_y = player_action["down"] - player_action["up"]

        self.bigger_rect.center = self.rect.center

        if not self.attacking:
            self.move_towards_player(player_x, player_y)
        else:
            self.attacking_after_player()

        if pygame.Rect.collidepoint(self.rect, self.bigger_rect.topleft) == True:
            self.avoid = True
            # print("hit topleft")
        if pygame.Rect.collidepoint(self.rect, self.bigger_rect.topright) == True:
            self.avoid = True
            # print("hit topright")
        if pygame.Rect.collidepoint(self.rect, self.bigger_rect.bottomleft) == True:
            self.avoid = True
            # print("hit bottomleft")
        if pygame.Rect.collidepoint(self.rect, self.bigger_rect.bottomright) == True:
            self.avoid = True
            # print("hit bottomright")

        # if self.avoid == True:
        #     self.current_time += deltatime
        #     if self.current_time > 0.3:
        #         self.avoid= False
        #         self.current_time = 0

        if self.avoid == True:
            self.attractspeed = self.moving_speed * -1  # (-1)Move to the opposite direction
            self.speed = 0
        elif self.avoid == False:
            self.speed = self.moving_speed
            self.attractspeed = 0

        if self.bigger_rect.colliderect(player_rect):
            if not self.attacking:
                self.attacking = True
                FACTOR = 20
                if self.rect.centerx > player_rect.centerx:
                    self.teleport_x = player_rect.left - (self.rect.width / 2) - FACTOR
                    self.teleport_y = random.uniform(player_rect.bottom - FACTOR, player_rect.top + FACTOR)
                elif self.rect.centerx < player_rect.centerx:
                    self.teleport_x = player_rect.right + (self.rect.width / 2) + FACTOR
                    self.teleport_y = random.uniform(player_rect.bottom - FACTOR, player_rect.top + FACTOR)
                elif self.rect.centery > player_rect.centery:
                    self.teleport_y = player_rect.top - (self.rect.height / 2) - FACTOR
                    self.teleport_x = random.uniform(player_rect.left - FACTOR, player_rect.right + FACTOR)
                elif self.rect.centery < player_rect.centery:
                    self.teleport_y = player_rect.bottom + (self.rect.height / 2) + FACTOR
                    self.teleport_x = random.uniform(player_rect.left - FACTOR, player_rect.right + FACTOR)
        else:
            self.attacking = False
        
       
    def move_towards_player(self, player_x, player_y):
        dx, dy = player_x - self.rect.centerx, player_y - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        # Normalize
        dx, dy = dx / (distance + 1), dy / (distance + 1)
        # Move towards player
        self.rect.centerx += dx * self.speed
        self.rect.centery += dy * self.speed
        # Move to opposite direction
        self.rect.centerx += dx * self.attractspeed
        self.rect.centery += dy * self.attractspeed

    def attacking_after_player(self):
        dx, dy = self.teleport_x - self.rect.centerx, self.teleport_y - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        # Normalize
        dx, dy = dx / (distance + 1), dy / (distance + 1)

        self.rect.centerx += dx * (self.speed*2)
        self.rect.centery += dy * (self.speed*2)


    def render(self, display):
        pygame.draw.rect(display, self.color, self.rect)
        pygame.draw.rect(display, (255,255,255), self.bigger_rect, 2)