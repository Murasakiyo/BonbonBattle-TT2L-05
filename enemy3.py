import pygame
import time
import math
import spritesheet
from minions import *

class Enemy3(pygame.sprite.Sprite):
    def __init__(self, game, group):
        super().__init__(group)
        self.game = game
        self.load_sprites()
        self.rect = self.snake.get_rect(width= 163, height=170)
        self.rect.x, self.rect.y = 700,200
        self.snake_mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.snake_mask.to_surface()
        self.enemyborder1 = pygame.Rect(-895, 40, 900, 570) #left
        self.enemyborder2 = pygame.Rect(1095, 40, 900, 570) #right
        self.enemyborder3 = pygame.Rect(0, 560, 1100, 370) #bottom
        self.enemyborder4 = pygame.Rect(0, -330, 1100, 370) #top         
        self.color = "white"
        self.speed, self.attractspeed = 0,0
        self.dist = 0
        self.minionspeed, self.current_time, self.minion_time, self.collide_time, self.attack_time = 0,0,0,0,0
        self.start_time = time.time()
        self.avoid = False
        self.collide = False
        self.moxie_activate = False
        self.minions = Minions(self.game, self.rect.centerx, self.rect.centery, speed=0)
        self.minionlist = pygame.sprite.Group()
        self.fps = 0.07
        self.current_frame, self.last_frame_update = 0,0
        self.HP = 300
        self.body_damage = 50
        self.attack = False
        self.ult_timer = 0
        self.ult = False
        self.atk_timer = 0
        self.moxie = 0
        self.leech = False

    def update(self, deltatime, player_action, player_x, player_y, player_rectx):

        if not self.leech:
            self.enemy3_movement(player_x, player_y)

        if self.attack:
            self.moxie +=  150 * deltatime

        if self.leech:
            self.atk_timer += deltatime
        if not self.leech:
            self.atk_timer = 0

        self.move_towards_border()
        self.rect.clamp_ip(self.game.screen_rect)
        
        self.direction = int(self.rect.x - player_rectx)

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

        if self.moxie < 300:
            self.minion_spawn(deltatime)   
        self.minionlist.update(deltatime, player_action, player_x, player_y)
        self.enemy3_moxie_function(deltatime)
        self.animate(deltatime, self.direction)

       

    def render(self, display):
        for self.minions in self.minionlist.sprites():
            self.minions.render(display)


    def minion_spawn(self, deltatime):
        if len(self.minionlist) == 0 and not self.leech:
            self.minion_time += deltatime
            if self.minion_time > 3:
                self.attack = True
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

       
                    


    def enemy3_moxie_function(self, deltatime):

        if self.moxie >= 300:
            self.ult = True
            

        if self.moxie < 300 and self.atk_timer > 3:
            self.ult = False
            self.leech = False

        if self.moxie <= 0:
            self.moxie = 0
            
        if self.ult == True and len(self.minionlist) == 1:
            self.attack = False
            self.leech = True
            self.moxie = 0


    def enemy3_movement(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player_x - self.rect.x, player_y - self.rect.y
        self.dist = math.hypot(dx, dy)

        dx, dy = dx / (self.dist + 1), dy / (self.dist + 1)  # Normalize.

        if self.dist > 500:
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
        

    def animate(self, deltatime, direction):
        self.last_frame_update += deltatime

        if self.speed == -4 and self.attractspeed == 0 and self.dist > 500 and not(self.attack) and not(self.leech):
            self.image = self.current_anim_list[0]
            if self.current_anim_list == self.ultimate_sprites:
                self.current_anim_list= self.right_sprites
                self.image = self.current_anim_list[0]
            return
        
        if self.leech:
            self.fps = 0.1
            self.current_anim_list = self.ultimate_sprites
            if not self.leech:
                self.current_anim_list = self.right_sprites

         # To stop the attacking animation
        if self.attack:
            self.attack_time += deltatime
            if self.attack_time > 1:
                self.attack = False
                if self.direction > 0:
                    self.current_anim_list = self.right_sprites
                elif self.direction < 0:
                    self.current_anim_list = self.left_sprites
                self.attack_time = 0

        if self.attack and not(self.leech):
            self.fps = 0.1
            if direction > 0:
                self.current_anim_list = self.attack_right
            elif direction < 0:
                self.current_anim_list = self.attack_left

        if not self.attack:
            self.fps = 0.07

        if direction > 0 and self.dist < 500 and not(self.attack) and not(self.leech):
            self.current_anim_list = self.right_sprites
        elif direction < 0 and self.dist < 500 and not(self.attack) and not(self.leech):
            self.current_anim_list = self.left_sprites

        if self.last_frame_update > self.fps:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0  

    def load_sprites(self):
        self.left_sprites, self.right_sprites = [], []
        self.attack_left, self.attack_right = [], []
        self.ultimate_sprites = []
        # Load frog sprite
        snake = pygame.image.load("sprites/snake_enemy.png").convert()
        self.snake = pygame.transform.scale(snake, (1250,875)).convert_alpha() 
        SP = spritesheet.Spritesheet(self.snake)
  
        # Walking sprites 
        for x in range(7):
            self.right_sprites.append(SP.get_sprite(x, 0, 163, 170, (0,0,0)))
        for x in range(7):
            self.left_sprites.append(SP.get_sprite(x, 170, 163, 170, (0,0,0)))
        for x in range(5):
            self.attack_right.append(SP.get_sprite(x, 345, 163, 170, (0,0,0)))
        for x in range(5):
            self.attack_left.append(SP.get_sprite(x, 520, 163, 170, (0,0,0)))
        for x in range(5):
            self.ultimate_sprites.append(SP.get_sprite(x, 700, 163, 170, (0,0,0)))


        self.image = self.right_sprites[0]
        self.current_anim_list = self.right_sprites

    def reset_minions(self):
        self.minionlist.empty()
        self.minion_time = 0
        self.attack = False
        self.minions = None  # Reset the minions variable
      
    def enemy_reset(self):
        self.attack = False
        self.rect.x, self.rect.y = 700,200
        self.image = self.right_sprites[0]
        self.current_time = 0
        self.HP = 300
        self.ult_timer = 0
        self.ult = False
        self.leech = False
        self.reset_minions()
