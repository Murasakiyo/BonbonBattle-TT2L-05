import pygame
import spritesheet
import math

class FrogEnemy(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.rect = self.frog.get_rect(width= 200, height=165)   # Placeholder for enemy froggie 
        self.rect.x, self.rect.y = 700,200
        self.rect_draw = pygame.Rect(900,70,200,20)  # Placeholder for tongue
        self.color = (255,255,255)
        self.current_time = 0
        self.attack = False
        self.attack_cooldown = 0 
        self.current_frame, self.current_frame_unique, self.last_frame_update = 0,0,0 #animation
        self.fps = 0.05
        self.speed = 3
        self.stop = False
        self.collision = False
        self.left = False
        self.right = False



    def update(self, deltatime, player_action, player_x, player_y, player_rect):
        # Tongue's position
        self.rect_draw = pygame.Rect(self.rect.centerx, self.rect.centery, 150, 20)

        # Collision with the screen
        self.rect.clamp_ip(self.game.screen_rect)
        
        # Get direction towards player # animation
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        if self.collision == False:
            if any(self.rect.clipline(*line) for line in player_rect):
                self.stop = True

        if self.stop == True:
            self.current_time += deltatime
            self.speed = 0
            self.attack = True
            if self.current_time > 2.5:
                self.attack = False
                self.speed = 3
                self.stop = False
            if self.current_time > 3.2:
                self.collision = False
                self.current_time = 0

        # if pygame.Rect.colliderect(self.rect.left, rect_right):
        #     self.left = True
        # if pygame.Rect.colliderect(self.rect.right, rect_left):
        #     self.right = True
        
        self.move_towards_player(player_x, player_y)
        self.animate(deltatime, direction_x, direction_y, self.dx, self.speed)


    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(display, (255,255,255), self.rect, 2)
        # pygame.draw.rect(display, self.color, self.rect_draw, 2)


    def animate(self, deltatime, direction_x, direction_y, distance, speed):
        self.last_frame_update += deltatime

        if int(speed) == 0:
            if (self.current_anim_list == self.right_sprites or self.current_anim_list == self.attack_right):
                self.current_anim_list = self.right_sprites
                self.image = self.current_anim_list[0]
            elif self.current_anim_list == self.left_sprites or self.current_anim_list == self.attack_left:
                self.current_anim_list = self.left_sprites
                self.image = self.current_anim_list[0]
            return self.image
        
        if speed != 0:
            if distance > 0:
                self.current_anim_list = self.right_sprites
            else:
                self.current_anim_list = self.left_sprites

        if self.last_frame_update > self.fps:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0  
        
    
    def move_towards_player(self, player_x, player_y):
        # Find direction vector (dx, dy) and distance between enemy and player.
        self.dx, self.dy = player_x - self.rect.centerx, player_y - self.rect.centery
        if self.dx > 0:
            self.dx -= 200
        elif self.dx < 0:
            self.dx += 200
        else:
            self.dx = self.dx
        self.distance = math.sqrt(self.dx**2 + self.dy**2)

        # Normalize
        self.dx, self.dy = self.dx / (self.distance + 1), self.dy / (self.distance + 1)

        self.rect.centerx += self.dx * self.speed
        self.rect.centery += self.dy * self.speed
        print(self.rect.left)



    def take_damage(self, damage):
        pass

    def destroy(self):
        pass


    def load_sprites(self):
        self.left_sprites, self.right_sprites = [], []
        self.attack_left, self.attack_right = [], []

        # Load frog sprite
        frog = pygame.image.load("sprites/frog_enemy.png").convert()
        self.frog = pygame.transform.scale(frog, (1175, 525)).convert_alpha() #Note for Yaro: 1175,525 - 25% of the initial sprite png
        SP = spritesheet.Spritesheet(self.frog)   
  
        # Walking sprites 
        for x in range(6):
            self.left_sprites.append(SP.get_sprite(x, 0, 194, 165, (0,0,0)))
        for x in range(6):
            self.right_sprites.append(SP.get_sprite(x, 175, 190, 165, (0,0,0)))
        for x in range(3):
            self.attack_left.append(SP.get_sprite(x, 350, 194, 165, (0,0,0)))
        for x in range(3,6):
            self.attack_right.append(SP.get_sprite(x, 350, 194, 165, (0,0,0)))

        self.image = self.left_sprites[0]
        self.current_anim_list = self.left_sprites
