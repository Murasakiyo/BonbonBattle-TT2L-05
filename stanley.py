import pygame
import time
import math
import spritesheet
from parent_classes.support_dolls import *
from parent_classes.dialogue import *
# from torres import Player

class Stanley(pygame.sprite.Sprite, Support):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.rect = self.stanley.get_rect(width=150, height=200)
        self.rect.x, self.rect.y = 0, 200
        self.current_frame, self.current_frame_unique, self.last_frame_update = 0,0,0
        self.fps = 0.2
        self.attack = False
        self.current_time = 0
        self.attack_cooldown = 0
        self.min_step, self.max_step = 0,0
 
    def update(self,deltatime, player, player_action, player_x, player_y, enemy_moxie):
        if self.attack:
            if not(self.attack_cooldown > 0.02):
                player.attackpoints = player.attackpoints + (player.attackpoints * 0.5)
                enemy_moxie -= 10
        else:
            player.attackpoints = self.game.settings.current_attackpoints
        self.update_movement(deltatime, player, player_action, player_x, player_y, self.animate)
        
    def update_lounge(self, deltatime, player, player_action):
        
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]
        self.animate(deltatime, player, direction_x, direction_y, 0)

       
    
    def render(self, display):
        # display.blit(self.image, (self.doll_vector.x, self.doll_vector.y))
        pygame.draw.rect(display, (255,255,255), self.rect, 2)


    def animate(self, deltatime, player, direction_x, direction_y, distance):
        self.last_frame_update += deltatime

        # Code for all support doll's walking and idle animation
        self.idle_walking(player, direction_x, direction_y, distance, 0.15)

        # Fps for each animation
        if self.current_anim_list == self.right_sprites or self.current_anim_list == self.left_sprites:
            self.fps = 0.5
        if self.current_anim_list == self.walk_right or self.current_anim_list == self.walk_left:
            self.fps = 0.2

        # Updating frames
        if self.last_frame_update > self.fps:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0 


    def load_sprites(self):
        self.right_sprites, self.left_sprites = [], []
        self.walk_right, self.walk_left = [], []
        self.attack_right, self.attack_left = [], []
        stan = pygame.image.load("sprites/stanley_sp.png").convert()
        self.stanley = pygame.transform.scale(stan, (650,800)).convert_alpha()
        SP = spritesheet.Spritesheet(self.stanley)

        # Walking sprites
        for x in range(2):
            self.right_sprites.append(SP.get_sprite(x, 0, 159,190, (0,0,0)))
        for x in range(2, 4):
            self.left_sprites.append(SP.get_sprite(x, 0, 160, 190, (0,0,0)))
        for x in range(2):
            self.walk_right.append(SP.get_sprite(x, 200, 160, 190, (0,0,0)))
        for x in range(2,4):
            self.walk_left.append(SP.get_sprite(x, 200, 160, 190, (0,0,0)))
        for x in range(3):
            self.attack_right.append(SP.get_sprite(x,400, 180, 190, (0,0,0)))
        for x in range(3):
            self.attack_left.append(SP.get_sprite(x, 600, 180, 190, (0,0,0)))

        self.image = self.right_sprites[0]
        self.current_anim_list = self.right_sprites