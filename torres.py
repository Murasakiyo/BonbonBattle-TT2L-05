import pygame
import spritesheet
import copy


class Player(pygame.sprite.Sprite):
    def __init__(self, game, group, position_x, position_y):
        super().__init__(group)
        self.game = game
        self.current_time = 0
        self.attack = False
        self.defend = False
        self.right = 1
        self.load_sprites()
        self.rect = self.torres_walk.get_rect(width= 200, height=200)
        self.rect.x, self.rect.y = position_x, position_y
        self.torres_mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.torres_mask.to_surface()
        self.current_frame, self.last_frame_update = 0,0
        self.lines = [((self.rect.midbottom), (self.rect.midtop))]
        self.horiz_line = [((self.rect.midleft), (self.rect.midright))]
        self.fps = 0
        self.color = "white"
        self.collide = False
        self.collide_time = 0
        self.c_time = 0
        # self.moxie_points = 0
        self.moxie_bool = False
        self.healthpoints = 250
        self.attackpoints = 10
        self.defensepoints = 10
        self.moxiepoints = 0
        

    def update(self,deltatime,player_action):
        # Get direction from input
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        # collision with the screen
        self.rect.clamp_ip(self.game.screen_rect)


        # Check for defense button
        if player_action["defend"]:
            player_action["attack"] = False
            self.defend = True
            direction_x = 0
            direction_y = 0
            
        # Defense timer
        if self.defend:
            self.attack = False
            self.current_time += deltatime
            if self.current_time > 0.8:
                player_action["defend"] = False
                self.defend = False
                self.current_time = 0
                if self.right == 1:
                    self.current_anim_list = self.right_sprites
                else:
                    self.current_anim_list = self.left_sprites
                    
        # Check for attack button
        if player_action["attack"]:
            if player_action["defend"]:
                self.attack = False
            else:
                self.attack = True
                direction_x = 0
                direction_y = 0

        # Attack timer
        if self.attack == True and self.defend != True:
            self.current_time += deltatime
            if self.current_frame >= 4:
                if self.current_time > 0.2:
                    player_action["attack"] = False
                    self.attack = False
                    self.current_time = 0

        
        # animation for sprite
        self.animate(deltatime, direction_x, direction_y)

        # position
        # if collide_bool == False:
        self.rect.x += 400 * deltatime * direction_x 
        self.rect.y += 450 * deltatime * direction_y

##################################################################################
        self.lines = [((self.rect.midbottom), (self.rect.midtop))]
        # self.enemy1_collision = [((self.rect.midleft[0] - 100, self.rect.midleft[1]), (self.rect.midright[0] + 100, self.rect.midright[1]))]
        # self.enemy3_collisions(deltatime, direction_x, direction_y, collide_bool)




        # print(self.collide_time)
        # print(self.collide)
        # print(self.moxie_points)
        # print(collide_bool)

        


        self.horiz_line = [((self.rect.midleft), (self.rect.midright))]
        # self.enemy2_collision = [((self.rect.midleft), (self.rect.midright))]


    def render(self, display):
        # display.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(display, (255,255,255), self.rect,2)
        pygame.display.flip()
        

        for line in self.lines:
            pygame.draw.line(display, "white", *line)
        # for line in self.enemy1_collision:
        #     pygame.draw.line(display, "white", *line)
        for line in self.horiz_line:
            pygame.draw.line(display, "white", *line)
            
        # pygame.draw.rect(display, self.color, self.rect_draw)

    def player_stats(self):
        self.healthpoints = 100
        self.attackpoints = 10
        self.defense = 10 # defense formula

    def enemy3_collisions(self, deltatime, direction_x, direction_y, collide_bool):       
       if collide_bool == True:
            self.collide_time += deltatime
            if self.collide_time > 0.1:
                self.rect.x += 200 * deltatime * direction_x 
                self.rect.y += 225 * deltatime * direction_y

            if self.collide_time > 3:
                self.collide = True
                self.collide_time = 0
                
        

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
            self.current_frame = 0
            self.current_anim_list = self.attack_right[0]
            self.current_anim_list = self.attack_right
        if (self.image == self.left_sprites[self.current_frame]) and self.attack:
            self.current_anim_list.clear
            self.current_frame = 0
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
            self.fps = 0.06
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
        torres = pygame.image.load("sprites/torres_sp1.png").convert()
        self.torres_walk = pygame.transform.scale(torres, (1038,1200)).convert_alpha()
        SP = spritesheet.Spritesheet(self.torres_walk)

        #load frames for each direction
        self.defend_sprites.append(SP.get_sprite(0, 800, 198, 200, (0,0,0)))
        self.defend_sprites.append(SP.get_sprite(1, 800, 198, 200, (0,0,0)))
        for x in range(5):
            self.right_sprites.append(SP.get_sprite(x, 0, 193,190, (0,0,0)))
        for x in range(5):
            self.left_sprites.append(SP.get_sprite(x, 190, 171, 190, (0,0,0)))
        for x in range(5):
            self.attack_right.append(SP.get_sprite(x, 395, 190, 193, (0,0,0)))
        for x in range(5):
            self.attack_left.append(SP.get_sprite(x, 595, 198, 200, (0,0,0)))
            
        self.image = self.right_sprites[0]
        self.current_anim_list = self.right_sprites

    def cooldown_variable(self):
        self.take_damage = False
        self.attack_time = 0
        self.let_attack = True
        self.deal_damage = False
        self.attack_cooldown = 0

    



        

