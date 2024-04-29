import pygame
import spritesheet
import math
import random

class FlyEnemy(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.current_time = 0       
        # self.rect = self.fly.get_rect(width=800, height=0)
        # self.rect.x, self.rect.y = 800, 0 # Initial position
        # self.current_frame, self.current_frame_unique, self.last_frame_update = 0,0,0 #animation
        # self.fps = 0.2
        self.attack = False
        self.attack_cooldown = 0 # Before the next attack
        # self.min_step, self.max_step = 0,0
        self.speed = 3
        self.rect = pygame.Rect(900,70,60,60)  # Placeholder
        self.color = (255,0,0)
        self.mask = None
        self.enemies = pygame.sprite.Group()
        # self.spawn_enemies()


    def update(self, deltatime, player_action, player_x, player_y):
        # collision with the screen
        self.rect.clamp_ip(self.game.screen_rect)
    

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

        if distance != 0:  # Ensure to not divide by zero
            dx, dy = dx / distance, dy / distance
        
        self.rect.centerx += dx * self.speed
        self.rect.centery += dy * self.speed


    # Test code
    # def spawn_enemies(self):
    #     for i in range(3):
    #         random_x = random.randint(0, self.game.SCREENWIDTH)
    #         random_y = random.randint(0, self.game.SCREENHEIGHT)
    #         new_enemy = FlyEnemy(self.game)  # Create a new enemy instance
    #         new_enemy.rect.center = (random_x, random_y)  # Position
    #         self.enemies.add(new_enemy)  # Add the enemy to the grp
            

    def take_damage(self, damage):
        # self.health -= damage
        pass

    def destroy(self):
        # self.image.remove(self)
        pass


    def render(self, display):
        # display.blit(self.image, (self.rect.x, self.rect.y))
        # pygame.draw.rect(display, (255,255,255), self.rect, 2)
        # for enemy in self.enemies.sprites():
        pygame.draw.rect(display, self.color, self.rect)


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




        # Test code - enemy movement with placeholder image
        # self.image = pygame.image.load("sprites/placeholder.png").convert_alpha()
        # self.image = pygame.transform.scale(self.image, (150,100))
        # self.mask = pygame.mask.from_surface(self.image)