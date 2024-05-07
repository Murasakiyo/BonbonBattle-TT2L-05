import pygame
import spritesheet
import math
import random
from parent_classes.enemyhealthbar import *


class FlyEnemy(pygame.sprite.Sprite, EnemyHealthBar):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.flies = Fly(self.game)
        self.flylist = pygame.sprite.Group()  # List of the flies
        # self.current_frame, self.current_frame_unique, self.last_frame_update = 0,0,0 #animation
        # self.fps = 0.2

    def update(self, deltatime, player_action, player_x, player_y, player_rect, player_rectx):

        self.flies.rect.clamp_ip(self.game.screen_rect)

        self.flies_spawn()
        for flies in self.flylist.sprites():
            flies.update(deltatime, player_action, player_x, player_y, player_rect, player_rectx)
            self.load_enemy_health(flies, flies.rect.x, flies.rect.y, flies.HP)


        # self.avoid_rect(deltatime)


    def render(self, display):
        for self.flies in self.flylist.sprites():
            self.flies.render(display)
            # pygame.draw.rect(display, "black", (self.flies.rect.x, self.flies.rect.y, 150, 10))
            # pygame.draw.rect(display, "green", self.flies.enemy_health)

    # # To avoid overlap among flies
    # def avoid_rect(self, deltatime):  
    #     FACTOR = 20
    #     for follower in self.flylist.sprites():
    #         for target in self.flylist.sprites():
    #             if follower == target:
    #                 continue
    #             if pygame.Rect.colliderect(follower.rect, target.rect):
    #                 # print("Flies collide")
    #                 if follower.rect.centerx <= target.rect.centerx:    
    #                     follower.rect.right = target.rect.left - FACTOR   # Move left
    #                 if follower.rect.centerx > target.rect.centerx:
    #                     follower.rect.left = target.rect.right + FACTOR   # Move right
    #                 if follower.rect.centery <= target.rect.centery:
    #                     follower.rect.bottom = target.rect.top - FACTOR   # Move up
    #                 if follower.rect.centery > target.rect.centery:
    #                     follower.rect.top = target.rect.bottom + FACTOR   # Move down


    def flies_spawn(self):
        if len(self.flylist) == 0:
            for i in range(3):
                new_fly = Fly(self, moving_speed= 1+(i+1))
                self.flylist.add(new_fly)


class Fly(pygame.sprite.Sprite):
    def __init__(self, game, moving_speed=0.5, color=(0,255,0)):
        super().__init__()
        self.game = game
        random_x = random.randint(600, 1100)
        random_y = random.randint(0, 600)
        self.load_sprites()
        self.rect = self.fly.get_rect(width= 130, height=119)
        self.fly_mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.fly_mask.to_surface()
        self.rect.x, self.rect.y = random_x, random_y
        self.color = color
        self.bigger_rect = self.rect.scale_by(1.5)
        self.fps = 0.07
        self.current_frame, self.current_frame_unique, self.last_frame_update = 0,0,0
        self.cooldown_duration = 2
        self.cooldown_timer = 0
        self.moving_speed = moving_speed
        self.attack = False
        self.teleport_x = None
        self.teleport_y = None
        self.HP = 150
        self.damage = 10
        self.body_damage = 15
        # LAST RESORT
        # self.enemy_health = pygame.Rect(self.rect.x, self.rect.y, self.HP, 10)


    def update(self, deltatime, player_action, player_x, player_y, player_rect, player_rectx):

        # self.enemy_health = pygame.Rect(self.rect.x, self.rect.y, self.HP, 10)
        
        self.bigger_rect.center = self.rect.center
        if not self.attack:
            if self.cooldown_timer <= 0:  # When the cooldown timer is end // when the player starts the game
                self.move_towards_player(player_x, player_y)
            else:
                self.cooldown_timer -= deltatime   # Update the remaining timer 
        else:
            self.attacking_after_player()

        self.direction = int(self.rect.x - player_rectx)

        # Teleport flies
        if self.bigger_rect.colliderect(player_rect):
            if self.cooldown_timer <= 0:
                if not self.attack:
                    self.attack = True
                    FACTOR = 200
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
                self.cooldown_timer -= deltatime
        else:
            self.attack = False
        self.animate(deltatime, self.direction)
        
       
    def move_towards_player(self, player_x, player_y):
        dx, dy = player_x - self.rect.centerx, player_y - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        # Normalize
        dx, dy = dx / (distance + 1), dy / (distance + 1)
        # Move towards player
        self.rect.centerx += dx * self.moving_speed
        self.rect.centery += dy * self.moving_speed


    def attacking_after_player(self):
        dx, dy = self.teleport_x - self.rect.centerx, self.teleport_y - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)

        # Normalize
        dx, dy = dx / (distance + 1), dy / (distance + 1)

        self.rect.centerx += dx * (self.moving_speed*2) 
        self.rect.centery += dy * (self.moving_speed*2)

        # Set a cooldown timer after attack
        self.cooldown_timer = self.cooldown_duration

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

        # LAST RESORT
        # pygame.draw.rect(display, "green", self.enemy_health)
        # pygame.draw.rect(display, (255,0,0), self.rect, 2)
        # pygame.draw.rect(display, (255,255,255), self.bigger_rect, 2)


    def animate(self, deltatime, direction):
        self.last_frame_update += deltatime

        if direction > 0 and not(self.attack):
            self.current_anim_list = self.right_sprites
        elif direction < 0 and not(self.attack):
            self.current_anim_list = self.left_sprites

        if self.attack and self.image == self.right_sprites[self.current_frame]:
            self.current_anim_list = self.attack_right
        elif self.attack and self.image == self.left_sprites[self.current_frame]:
            self.current_anim_list = self.attack_left



        if self.last_frame_update > self.fps:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0  


    def load_sprites(self):
        self.left_sprites, self.right_sprites = [], []
        self.attack_left, self.attack_right = [], []
        # Load frog sprite
        fly = pygame.image.load("sprites/fly_enemy.png").convert()
        self.fly = pygame.transform.scale(fly, (413, 250)).convert_alpha() 
        SP = spritesheet.Spritesheet(self.fly)   
  
        # Walking sprites 
        for x in range(2):
            self.left_sprites.append(SP.get_sprite(x, 0, 130, 119, (0,0,0)))
        for x in range(2):
            self.right_sprites.append(SP.get_sprite(x, 130, 130, 119, (0,0,0)))
        for x in range(2,3):
            self.attack_left.append(SP.get_sprite(x, 0, 130, 119, (0,0,0)))
        for x in range(2,3):
            self.attack_right.append(SP.get_sprite(x, 130, 130, 119, (0,0,0)))


        self.image = self.right_sprites[0]
        self.current_anim_list = self.right_sprites