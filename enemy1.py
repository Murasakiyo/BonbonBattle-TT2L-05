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
        self.current_time = 0
        self.camera = state.CameraGroup(self.game)
        self.player = torres.Player(self.game, self.camera)
        # self.rect = self.frog.get_rect(width=800, height=0)
        # self.rect.x, self.rect.y = 800, 0 # Initial position
        # self.current_frame, self.current_frame_unique, self.last_frame_update = 0,0,0 #animation
        # self.fps = 0.2
        self.attack = False
        self.attack_cooldown = 0 # Before the next attack
        # self.min_step, self.max_step = 0,0
        self.speed = 3
        self.rect = pygame.Rect(800,10,200,150)   # Add placeholder for enemy frog 
        self.mask = None
        self.rect_draw = pygame.Rect(900,70,200,20)  # Placeholder for tongue
        self.color = (255,255,255)


    def update(self, deltatime, player_action, player_x, player_y):
        # Tongue's position
        self.rect_draw = pygame.Rect(self.rect.centerx, self.rect.centery, 150, 20)

        # Collision with the screen
        self.rect.clamp_ip(self.game.screen_rect)
        self.player.rect.clamp_ip(self.game.screen_rect)

        # Increment current_time
        self.current_time += deltatime
        
        # Get direction towards player # animation
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        self.move_towards_player(player_x, player_y)

        # Check distance between enemy and player
        dx, dy = player_x - self.rect.centerx, player_y - self.rect.centery
        if dx > 0:
            dx -= 200
        elif dx < 0:
            dx += 200
        else:
            dx = dx
        distance = math.sqrt(dx**2 + dy**2)

        # Attack and Cooldown
        if distance == 0:
            # print("You get hit!")
            self.attack = True
            self.attack_cooldown += deltatime
            
            if self.attack_cooldown > 0.5:
                # print("Wait, let me rest first.")
                self.attack = False
                self.attack_cooldown = 0
                self.current_time = 0


    def move_towards_player(self, player_x, player_y):
        # Find direction vector (dx, dy) and distance between enemy and player.
        dx, dy = player_x - self.rect.centerx, player_y - self.rect.centery
        if dx > 0:
            dx -= 200
        elif dx < 0:
            dx += 200
        else:
            dx = dx
        distance = math.sqrt(dx**2 + dy**2)
        # print(int(distance))

        # Normalize
        if distance != 0:  # Ensure to not divide by zero
            dx, dy = dx / distance, dy / distance
        # dx, dy = dx / (distance + 1), dy / (distance + 1)

        self.rect.centerx += dx * self.speed
        self.rect.centery += dy * self.speed


    def take_damage(self, damage):
        # self.health -= damage
        pass

    def destroy(self):
        # self.image.remove(self)
        pass


    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
        pygame.draw.rect(display, (255,255,255), self.rect, 2)
        pygame.draw.rect(display, self.color, self.rect_draw)


    def animate(self, deltatime, direction_x, direction_y, distance):
        # self.last_frame_update += deltatime
        pass
    

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
        self.image = pygame.transform.scale(self.image, (200,150))
        self.mask = pygame.mask.from_surface(self.image)