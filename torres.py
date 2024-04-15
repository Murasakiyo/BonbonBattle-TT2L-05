import pygame
import spritesheet


class Player(pygame.sprite.Sprite):
    def __init__(self, game, group):
        super().__init__(group)
        self.game = game
        self.current_time = 0
        self.attack = False
        self.defend = False
        self.right = 1
        self.load_sprites()
        self.rect = self.torres_walk.get_rect(width= 150, height=200)
        # self.rect.center = (295, 373)
        self.rect.x, self.rect.y = 200,150
        # self.line = self.rect.clipline(50, 50)
        self.current_frame, self.last_frame_update = 0,0
        self.fps = 0
        

    def update(self,deltatime,player_action):
        # Get direction from input
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        # collision with the screen
        if self.rect.right >= self.game.SCREENWIDTH:
            self.rect.x = 950
        if self.rect.left <= 0:
            self.rect.x = -1

        # Check for defense button
        if player_action["defend"]:
            self.attack = False
            self.defend = True
            direction_x = 0
            direction_y = 0
            
        # Defense timer
        if self.defend:
            self.current_time += deltatime
            if self.current_time > 0.5:
                player_action["defend"] = False
                self.defend = False
                self.current_time = 0
                if self.right == 1:
                    self.current_anim_list = self.right_sprites
                else:
                    self.current_anim_list = self.left_sprites

        # Check for attack button
        if player_action["attack"]:
            self.attack = True
            direction_x = 0
            direction_y = 0


        # if direction_y != 0:
        #     self.attack = False
            
        # if self.attack == True:
        #     self.current_time = time.time()
        #     if self.current_frame >= 4:
        #         if self.current_time - self.prev_time > 1:
        #             player_action["attack"] = False
        #             self.attack = False
        #             self.prev_time = self.current_time

        # Attack timer
        if self.attack == True:
            self.current_time += deltatime
            if self.current_frame >= 4:
                if self.current_time > 0.3:
                    player_action["attack"] = False
                    self.attack = False
                    self.current_time = 0

        # animation for sprite
        self.animate(deltatime, direction_x, direction_y)

        # position
        self.rect.x += 400 * deltatime * direction_x
        self.rect.y += 450 * deltatime * direction_y
        



    def render(self, display):
        # display.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(display, (255,255,255), self.rect,2)
        



    def animate(self, deltatime, direction_x, direction_y):

        #compute how much time has passed since the frame last update
        self.last_frame_update += deltatime

        #if no direction is pressed, set image to idle and return
        if not(direction_x or direction_y) and self.attack == False and self.defend == False:
            self.image = self.current_anim_list[0]
            return
        
        #if an image was pressed, use the appropriate list of frames according to direction
        if direction_x:
            if direction_x > 0:
                self.current_anim_list = self.right_sprites
            else: 
                self.current_anim_list = self.left_sprites

        #walk animation after attacking
        if direction_y != 0 and (self.image == self.attack_right[self.current_frame]): 
            self.current_anim_list = self.right_sprites
        elif direction_y != 0 and (self.image == self.attack_left[self.current_frame]): 
            self.current_anim_list = self.left_sprites


        #Attack animation
        if (self.image == self.right_sprites[self.current_frame]) and self.attack:
            self.current_anim_list.clear
            self.current_anim_list = self.attack_right[0]
            self.current_anim_list = self.attack_right
        if (self.image == self.left_sprites[self.current_frame]) and self.attack:
            self.current_anim_list.clear
            self.current_anim_list = self.attack_left[0]
            self.current_anim_list = self.attack_left

        #Defend animation
        if ((self.image == self.right_sprites[self.current_frame]) or (self.image == self.attack_right[self.current_frame])) and self.defend:
            self.current_anim_list.clear
            self.current_anim_list = self.defend_sprites
            self.current_frame = 0
            self.right = 1
        if ((self.image == self.left_sprites[self.current_frame]) or (self.image ==self.attack_left[self.current_frame])) and self.defend:
            self.current_anim_list.clear
            self.current_anim_list = self.defend_sprites
            self.current_frame = 1
            self.right = 0

        # fps differs 
        if self.attack:
            self.fps = 0.08
        else:
            self.fps = 0.1

        #Advance the animation if enough time has elapsed
        if self.last_frame_update > self.fps:
            if self.current_anim_list == self.defend_sprites:
                self.image = self.current_anim_list[self.current_frame]
                self.last_frame_update = 0  
            else:
                self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
                self.image = self.current_anim_list[self.current_frame]
                self.last_frame_update = 0  
        #-----------------------------------------------------------------------------------------
        

    def load_sprites(self):
        self.right_sprites, self.left_sprites = [], []
        self.attack_right, self.attack_left = [], []
        self.defend_sprites = []
        torres = pygame.image.load("sprites/torres_sp.png").convert()
        self.torres_walk = pygame.transform.scale(torres, (1038,1200)).convert_alpha()
        SP = spritesheet.Spritesheet(self.torres_walk)

        #load frames for each direction
        self.defend_sprites.append(SP.get_sprite(0, 800, 198, 200, (0,0,0)))
        self.defend_sprites.append(SP.get_sprite(1, 800, 198, 200, (0,0,0)))
        for x in range(5):
            self.right_sprites.append(SP.get_sprite(x, 0, 171,190, (0,0,0)))
        for x in range(5):
            self.left_sprites.append(SP.get_sprite(x, 190, 171, 190, (0,0,0)))
        for x in range(5):
            self.attack_right.append(SP.get_sprite(x, 395, 190, 193, (0,0,0)))
        for x in range(5):
            self.attack_left.append(SP.get_sprite(x, 595, 198, 200, (0,0,0)))
            
        self.image = self.right_sprites[0]
        self.current_anim_list = self.right_sprites

class Hitbox(pygame.sprite.Sprite):
    pass