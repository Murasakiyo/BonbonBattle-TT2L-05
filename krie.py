import pygame
import time
import math
import spritesheet


class Krie(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.rect = self.krie.get_rect(width=150, height=200)
        self.rect.x, self.rect.y = 0, 200
        self.current_frame, self.current_frame_unique, self.last_frame_update = 0,0,0
        self.fps = 0.2
        self.attack = False
        self.current_time = 0
        self.attack_cooldown = 0
        self.min_step, self.max_step = 0,0
 


    def update(self,deltatime, player_action, player_x, player_y):
        self.current_time += deltatime

        # Check player direction
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        # Cooldown for attack
        if self.current_time > 3:
            self.attack = True
            self.attack_cooldown += deltatime
            if self.attack_cooldown > 0.8:
                self.attack = False
                self.attack_cooldown = 0
                self.current_time = 0
        
        # Move towards player always
        if not self.attack:
            self.move(player_x, player_y)

        self.animate(deltatime, direction_x, direction_y, self.step_distance)
                
    
    def render(self, display):
        display.blit(self.image, (self.krie_vector.x, self.krie_vector.y))
        # pygame.draw.rect(display, (255,255,255), self.rect,2)


    def animate(self, deltatime, direction_x, direction_y, distance):
        self.last_frame_update += deltatime

        # Support doll idle
        if not(direction_x or direction_y) and (self.attack == False):
            if self.current_anim_list == self.right_sprites or self.current_anim_list == self.walk_right or self.current_anim_list == self.attack_right:
                self.current_anim_list = self.right_sprites
                self.image = self.current_anim_list[self.current_frame_unique]
            elif self.current_anim_list == self.left_sprites or self.current_anim_list == self.walk_left or self.current_anim_list == self.attack_left:
                self.current_anim_list = self.left_sprites
                self.image = self.current_anim_list[self.current_frame_unique]
            if self.last_frame_update > 0.5:
                self.current_frame_unique = (self.current_frame_unique + 1) % len(self.right_sprites)
                self.last_frame_update = 0 
            return
        
        # Support doll walking
        if direction_x and self.attack == False:
            if direction_x > 0:
                if distance > 0.4:
                    self.current_anim_list = self.walk_right
                else:
                    self.current_anim_list = self.right_sprites
            else: 
                if distance > 0.4:
                    self.current_anim_list = self.walk_left
                else:
                    self.current_anim_list =self.left_sprites

        # walk animation after attacking
        if direction_y != 0 and (self.image == self.attack_right[self.current_frame]) and self.attack == False: 
            self.current_anim_list = self.right_sprites
        elif direction_y != 0 and (self.image == self.attack_left[self.current_frame]) and self.attack == False: 
            self.current_anim_list = self.left_sprites

        # Support doll attacking animation
        if self.attack == True and (self.current_anim_list == self.right_sprites or self.current_anim_list == self.walk_right):
            self.current_anim_list.clear
            self.fps = 0.15
            self.current_frame = 0
            self.current_anim_list = self.attack_right[0]
            self.current_anim_list = self.attack_right
        if self.attack == True and (self.current_anim_list == self.left_sprites or self.current_anim_list == self.walk_left):
            self.current_anim_list.clear
            self.fps = 0.15
            self.current_frame = 0
            self.current_anim_list = self.attack_left[0]
            self.current_anim_list = self.attack_left


        # Fps for each animation
        if self.current_anim_list == self.right_sprites or self.current_anim_list == self.left_sprites:
            self.fps = 0.5
        if self.current_anim_list == self.walk_right or self.current_anim_list == self.walk_left:
            self.fps = 0.2

        # Updating frames
        if self.last_frame_update > self.fps:
            if self.current_anim_list == self.attack_right or self.current_anim_list == self.attack_left:
                if self.current_frame != 3:
                    self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
                    self.image = self.current_anim_list[self.current_frame]
                    self.last_frame_update = 0
                else:
                    self.image = self.current_anim_list[3]
                    self.last_frame_update = 0
            else:
                self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
                self.image = self.current_anim_list[self.current_frame]
                self.last_frame_update = 0 

        


    # This code is to make sure Support doll is always in range of Player
    def move(self, player_x, player_y):

        self.torres_vector = pygame.math.Vector2(player_x, player_y)
        self.krie_vector = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.step_distance = 0
        self.min_distance = 250
        self.max_distance = 500
        # print(self.follower_vector)


        # distance_to returns the pythagorean distance between two points
        self.distance = self.krie_vector.distance_to(self.torres_vector)
        
        if self.distance > self.min_distance:
            self.direction_vector = (self.torres_vector - self.krie_vector) / self.distance
            self.min_step        = max(0, self.distance - self.max_distance)
            self.max_step        = self.distance - self.min_distance
            #step_distance       = min(max_step, max(min_step, VELOCITY))
            self.step_distance   = self.min_step + (self.max_step - self.min_step) 
            self.krie_vector += self.direction_vector * self.step_distance * 0.1
            self.rect.x, self.rect.y = self.krie_vector.x, self.krie_vector.y


        

    def load_sprites(self):
        self.right_sprites, self.left_sprites = [], []
        self.walk_right, self.walk_left = [], []
        self.attack_right, self.attack_left = [], []
        klubnika = pygame.image.load("sprites/krie_sp.png").convert()
        self.krie = pygame.transform.scale(klubnika, (600,800)).convert_alpha()
        SP = spritesheet.Spritesheet(self.krie)

        # Walking sprites
        for x in range(2):
            self.right_sprites.append(SP.get_sprite(x, 0, 132,186, (0,0,0)))
        for x in range(2, 4):
            self.left_sprites.append(SP.get_sprite(x, 0, 132, 186, (0,0,0)))
        for x in range(2):
            self.walk_right.append(SP.get_sprite(x, 200, 132, 190, (0,0,0)))
        for x in range(2,4):
            self.walk_left.append(SP.get_sprite(x, 200, 132, 190, (0,0,0)))
        for x in range(4):
            self.attack_right.append(SP.get_sprite(x, 400, 146, 190, (0,0,0)))
        for x in range(4):
            self.attack_left.append(SP.get_sprite(x, 590, 144, 190, (0,0,0)))

        self.image = self.right_sprites[0]
        self.current_anim_list = self.right_sprites