import pygame
import spritesheet
import math
import torres
import state

class FrogEnemy(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.camera = state.CameraGroup(self.game)
        self.player = torres.Player(self.game, self.camera)
        # self.rect = self.frog.get_rect(width=800, height=0)
        # self.rect.x, self.rect.y = 800, 0 # Initial position
        # self.current_frame, self.current_frame_unique, self.last_frame_update = 0,0,0 #animation
        # self.fps = 0.2
        # self.attack = False
        self.current_time = 0
        self.previous_player_pos = (self.player.rect.x, self.player.rect.y)  # Player's previous position
        # self.attack_cooldown = 0 # Before the next attack
        # self.min_step, self.max_step = 0,0
        self.speed = 1

        # Add placeholder for enemy frog #
        self.rect = pygame.Rect(800, 0, 150, 100)

    def update(self, deltatime, player_action):
        # collision with the screen
        self.rect.clamp_ip(self.game.screen_rect)

        # Get direction towards player
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        # Update player's position based on input
        self.player.rect.x += 500 * deltatime * direction_x 
        self.player.rect.y += 450 * deltatime * direction_y 

        # Increment current_time
        self.current_time += deltatime

        self.move_towards_player()

        # Check distance between enemy and player
        dx, dy = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)

        # Put condition where the enemy will stop for a while
        if distance > 2:
            self.speed = 0   # Stop moving
            # To resume movement
            if self.current_time > 5:
                self.speed = 1
                self.move_to_player_previous_pos()

        # Update previous player's position
        self.previous_player_pos = (self.player.rect.x, self.player.rect.y)

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(display, (255,255,255), self.rect, 2)

    def animate(self, deltatime, direction_x, direction_y, distance):
        # self.last_frame_update += deltatime
        pass


    def move_towards_player(self):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)

        # Move along this normalized vector towards the player at current speed.
        if distance != 0:
            dx, dy = dx / distance, dy / distance  # Normalize.
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def move_to_player_previous_pos(self):
        dx, dy = self.previous_player_pos[0] - self.rect.x, self.previous_player_pos[1] - self.rect.y
        distance = math.sqrt(dx**2 + dy**2)

        if distance > 5:
            dx, dy = dx / distance, dy / distance
            self.rect.x += dx * self.speed
            self.rect.y += dy * self.speed

    def load_sprites(self):
        self.left_sprites, self.right_sprites = [], []
        self.jump_left, self.jump_right = [], [] 
        self.attack_left, self.attack_right = [], []

        # # Load frog sprite
        # frog = pygame.image.load("sprites/frog_enemy.png").convert()
        # self.frog = pygame.transform.scale(frog, (1175, 525)).convert_alpha() #Note for Yaro: 1175,525 - 25% of the initial sprite png
        # SP = spritesheet.Spritesheet(self.frog)   

    ## NOT SURE - HAVENT TEST WITH SPRITE ##    
        # # Walking sprites 
        # for x in range(3):
        #     self.left_sprites.append(SP.get_sprite(x, 0, 187, 175, (0,0,0)))
        # for x in range(3):
        #     self.right_sprites.append(SP.get_sprite(x, 175, 187, 175, (0,0,0)))
        # for x in range(3,6):
        #     self.jump_left.append(SP.get_sprite(x, 0, 198, 175, (0,0,0)))
        # for x in range(3,6):
        #     self.jump_right.append(SP.get_sprite(x, 175, 198, 175, (0,0,0)))
        # for x in range(2):
        #     self.attack_left.append(SP.get_sprite(x, 350, 187, 175, (0,0,0)))
        # for x in range(2):
        #     self.attack_right.append(SP.get_sprite(x, 350, 187, 175, (0,0,0)))

        # self.image = self.right_sprites[0]
        # # self.current_anim_list = self.right_sprites

        # Testing enemy movement with placeholder image
        self.image = pygame.image.load("sprites/placeholder.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (150,100))