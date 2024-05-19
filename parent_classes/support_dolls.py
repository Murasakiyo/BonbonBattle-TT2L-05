import pygame

class Support():
    def __init__(self, game):
        self.game = game

    def update_movement(self, deltatime, player_action, player_x, player_y, animate):
        self.current_time += deltatime

        if self.game.defeat or self.game.win:
            self.attack = False
            
        # Check player direction
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        # Cooldown for attack
        if not self.game.defeat:
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

        animate(deltatime, direction_x, direction_y, self.step_distance)


    # This code is to make sure Support doll is always in range of Player
    def move(self, player_x, player_y):

        self.torres_vector = pygame.math.Vector2(player_x, player_y)
        self.doll_vector = pygame.math.Vector2(self.rect.x, self.rect.y)
        self.step_distance = 0
        self.min_distance = 400
        self.max_distance = 500
        # print(self.follower_vector)


        # distance_to returns the pythagorean distance between two points
        self.distance = self.doll_vector.distance_to(self.torres_vector)
        
        if self.distance > self.min_distance:
            self.direction_vector = (self.torres_vector - self.doll_vector) / self.distance
            self.min_step        = max(0, self.distance - self.max_distance)
            self.max_step        = self.distance - self.min_distance
            #step_distance       = min(max_step, max(min_step, VELOCITY))
            self.step_distance   = self.min_step + (self.max_step - self.min_step) 
            # self.new_stan_vector = self.stan_vector + self.direction_vector * self.step_distance
            self.doll_vector += self.direction_vector * self.step_distance * 0.1
            self.rect.x, self.rect.y = self.doll_vector.x, self.doll_vector.y

    def idle_walking(self, direction_x, direction_y, distance, fps):

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

        # Walk animation after attacking
        if direction_y != 0 and (self.image == self.attack_right[self.current_frame]) and not(self.attack): 
            self.current_anim_list = self.right_sprites
        elif direction_y != 0 and (self.image == self.attack_left[self.current_frame]) and not(self.attack): 
            self.current_anim_list = self.left_sprites

        # Support doll attacking animation
        if self.attack == True and (self.current_anim_list == self.right_sprites or self.current_anim_list == self.walk_right):
            self.fps = fps
            self.current_frame = 0
            self.current_anim_list = self.attack_right

        if self.attack == True and (self.current_anim_list == self.left_sprites or self.current_anim_list == self.walk_left):
            self.fps = fps
            self.current_frame = 0
            self.current_anim_list = self.attack_left