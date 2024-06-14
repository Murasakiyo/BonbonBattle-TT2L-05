import pygame
import spritesheet
import copy


class Player(pygame.sprite.Sprite):
    def __init__(self, game, position_x, position_y):
        super().__init__()
        self.game = game
        self.current_time = 0
        self.attack = False
        self.defend = False
        self.right = 1
        self.load_sprites()
        self.cooldown_variable()
        self.rect = self.torres_walk.get_rect(width= 200, height=200)
        self.rect.x, self.rect.y = position_x, position_y
        self.torres_mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.torres_mask.to_surface()
        self.current_frame, self.current_frame_unique, self.last_frame_update = 0,0,0
        self.lines = [((self.rect.midbottom), (self.rect.midtop))]
        self.horiz_line = [((self.rect.midleft), (self.rect.midright))]
        self.fps = 0
        self.color = "white"
        self.collide = False
        self.collide_time = 0
        self.moxie_bool = False
        self.healthpoints = self.game.settings.current_healthpoints
        self.max_health = self.game.settings.current_healthpoints
        self.attackpoints = 100
        self.moxiepoints = 600
        self.speed = self.game.settings.current_speed
        self.lose = False
        self.win = False

        # print("initialize player")
    
    # to update the player's stats in each level
    def attribute_update(self):
        self.healthpoints = self.game.settings.current_healthpoints
        self.attackpoints = self.game.settings.current_attackpoints
        self.speed = self.game.settings.current_speed

    def update(self,deltatime,player_action):
        # print(f"current speed:{self.speed}, current attack: {self.attackpoints}, current health: {self.healthpoints}")
        
        if self.game.defeat and not(self.game.win):
            self.lose = True
        else:
            self.lose = False
        
        if self.game.win and not(self.game.defeat):
            self.win = True
        else:
            self.win = False

        if self.win or self.lose:
            player_action["right"] = False
            player_action["left"] = False
            player_action["up"] = False
            player_action["down"] = False
            player_action["attack"] = False
            player_action["defend"] = False

        if self.healthpoints > self.game.settings.current_healthpoints:
            self.healthpoints = self.game.settings.current_healthpoints
            
        # Get direction from input
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]
        
        # Check for defense button
        if player_action["defend"] == True:
            player_action["attack"] = False
            self.defend = True
            direction_x = 0
            direction_y = 0
        else:
            self.defend = False
                    
        # Check for attack button
        if player_action["attack"]:
            if self.defend:
                self.attack = False
            else:
                self.attack = True
                direction_x = 0
                direction_y = 0

        # Attack timer
        if self.attack == True:
            if not(self.defend):
                self.current_time += deltatime
                if self.current_frame >= 4:
                    if self.current_time > 0.2:
                        player_action["attack"] = False
                        self.attack = False
                        self.current_time = 0
            else:
                self.attack = False

        # animation for sprite
        self.animate(deltatime, direction_x, direction_y)

        # position
        self.rect.x += self.speed * deltatime * direction_x 
        self.rect.y += (self.speed + 50) * deltatime * direction_y

        self.lines = [((self.rect.midbottom), (self.rect.midtop))]
        self.horiz_line = [((self.rect.midleft), (self.rect.midright))]


    def render(self, display):
        # display.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(display, (255,255,255), self.rect,2)
        

        for line in self.lines:
            pygame.draw.line(display, "white", *line)
        # for line in self.enemy1_collision:
        #     pygame.draw.line(display, "white", *line)
        for line in self.horiz_line:
            pygame.draw.line(display, "white", *line)
            

    def render_camera(self, display, camera):
        display.blit(self.image, (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y))


    def reset_player(self, position_x, position_y):
        self.healthpoints = self.game.settings.current_healthpoints
        self.moxiepoints = 0
        self.rect.x, self.rect.y = position_x, position_y
        self.image = self.right_sprites[0]
        self.win = False
        self.lose = False
        self.current_anim_list = self.right_sprites
        self.defend = False
        self.attack = False
        self.current_frame, self.current_frame_unique, self.last_frame_update = 0,0,0
        self.current_time = 0
        self.cooldown_variable()

    def upgrade(self):
        self.healthpoints = self.game.settings.current_healthpoints
        self.max_health = self.healthpoints
        self.attackpoints = self.game.settings.current_attackpoints
        self.speed = self.game.settings.current_speed
                

    def animate(self, deltatime, direction_x, direction_y):

        #compute how much time has passed since the frame last update
        self.last_frame_update += deltatime

        
        #if no direction is pressed, set image to idle and return
        if not(direction_x or direction_y) and self.attack == False and not(self.defend) and not(self.game.defeat) and not(self.game.win):
            if self.current_anim_list == self.defend_sprites and self.current_frame == 0:
                self.current_anim_list = self.right_sprites
                self.image = self.current_anim_list[0]
            elif self.current_anim_list == self.defend_sprites and self.current_frame == 1:
                self.current_anim_list = self.left_sprites
                self.image = self.current_anim_list[0]
            else:
                self.image = self.current_anim_list[0]
            return
        
        #if an image was pressed, use the appropriate list of frames according to direction
        if direction_x and not(self.defend):
            if direction_x > 0 and not(self.defend):
                self.current_anim_list = self.right_sprites
            else: 
                self.current_anim_list = self.left_sprites

        #walk animation after attacking
        if direction_y != 0 and (self.image == self.attack_right[self.current_frame]) and not(self.defend) and not(self.win) and not(self.lose): 
            self.current_anim_list = self.right_sprites
        elif direction_y != 0 and (self.image == self.attack_left[self.current_frame]) and not(self.defend) and not(self.win) and not(self.lose): 
            self.current_anim_list = self.left_sprites


        #Attack animation
        if (self.image == self.right_sprites[self.current_frame]) and self.attack and not(self.win):
            self.current_anim_list.clear
            self.current_frame = 0
            self.current_anim_list = self.attack_right[0]
            self.current_anim_list = self.attack_right
        if (self.image == self.left_sprites[self.current_frame]) and self.attack and not(self.win):
            self.current_anim_list.clear
            self.current_frame = 0
            self.current_anim_list = self.attack_left[0]
            self.current_anim_list = self.attack_left

        #Defend animation
        if self.defend == True and ((self.image == self.right_sprites[self.current_frame]) or (self.image == self.attack_right[self.current_frame])):
            self.current_anim_list = self.defend_sprites
            self.current_frame = 0
            self.image = self.current_anim_list[self.current_frame]
            # self.right = 1
        if self.defend == True and ((self.image == self.left_sprites[self.current_frame]) or (self.image == self.attack_left[self.current_frame])):
            self.current_anim_list = self.defend_sprites
            self.current_frame = 1
            self.image = self.current_anim_list[self.current_frame]
            # self.right = 0

        # fps differs 
        if self.attack:
            self.fps = 0.06
        else:
            self.fps = 0.1

        # lose
        if self.lose:
            self.fps = 1
            self.current_anim_list = self.lose_sprites

        # win
        if self.win:
            self.fps = 0.2
            self.current_anim_list = self.win_sprites
            
        if self.lose:
            if (self.last_frame_update > self.fps):
                if self.current_frame_unique != 3:
                    self.current_frame_unique = (self.current_frame_unique + 1) % len(self.current_anim_list)
                    self.image = self.current_anim_list[self.current_frame_unique]
                    self.last_frame_update = 0
                else:
                    self.image = self.current_anim_list[3]
                    self.last_frame_update = 0

        #Advance the animation if enough time has elapsed
        if self.last_frame_update > self.fps:
            if self.current_anim_list == self.defend_sprites:
                self.image = self.current_anim_list[self.current_frame]
                # self.last_frame_update = 0  
            else:
                self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
                self.image = self.current_anim_list[self.current_frame]
                self.last_frame_update = 0  
        #-----------------------------------------------------------------------------------------
        


    def load_sprites(self):
        self.right_sprites, self.left_sprites = [], []
        self.attack_right, self.attack_left = [], []
        self.defend_sprites = []
        self.lose_sprites, self.win_sprites = [], []
        torres = pygame.image.load("sprites/torres_sp1.png").convert()
        self.torres_walk = pygame.transform.scale(torres, (1038,1200)).convert_alpha()
        SP = spritesheet.Spritesheet(self.torres_walk)

        #load frames for each direction
        self.defend_sprites.append(SP.get_sprite(0, 800, 198, 200, (0,0,0)))
        self.defend_sprites.append(SP.get_sprite(1, 800, 198, 200, (0,0,0)))
        self.lose_sprites.append(SP.get_sprite(0, 0, 193, 190, (0,0,0)))
        for x in range(5):
            self.right_sprites.append(SP.get_sprite(x, 0, 193,190, (0,0,0)))
        for x in range(5):
            self.left_sprites.append(SP.get_sprite(x, 190, 171, 190, (0,0,0)))
        for x in range(5):
            self.attack_right.append(SP.get_sprite(x, 395, 190, 193, (0,0,0)))
        for x in range(5):
            self.attack_left.append(SP.get_sprite(x, 595, 198, 200, (0,0,0)))
        for x in range(2,5):
            self.lose_sprites.append(SP.get_sprite(x, 800, 205, 200, (0,0,0)))
        for x in range(2):
            self.win_sprites.append(SP.get_sprite(x, 1000, 180, 200, (0,0,0)))
            
        self.image = self.right_sprites[0]
        self.current_anim_list = self.right_sprites

    def cooldown_variable(self):
        self.take_damage = False
        self.attack_time = 0
        self.let_attack = True
        self.deal_damage = False
        self.attack_cooldown = 0




        

