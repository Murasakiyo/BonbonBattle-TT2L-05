import pygame
import math

class Minions(pygame.sprite.Sprite):
    def __init__(self, game, enemy3_rectx, enemy3_recty, speed):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.rect = self.gummy.get_rect(width = 50, height= 44)
        self.rect.x, self.rect.y = enemy3_rectx -100, enemy3_recty 
        self.minion_speed = speed # 2
        self.damage = 10
        self.last_frame_update, self.current_frame = 0, 0

    def update(self, deltatime, player_action, player_x, player_y):
        self.rect.clamp_ip(self.game.screen_rect)

        self.move_towards_player(player_x, player_y)
        self.animate(deltatime)

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))


    def move_towards_player(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player_x - self.rect.x, player_y - self.rect.y
        dist = math.hypot(dx, dy)

        dx, dy = dx / (dist + 1), dy / (dist + 1)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.minion_speed
        self.rect.y += dy * self.minion_speed

    def animate(self, deltatime):
        self.last_frame_update += deltatime
         
        self.current_anim_list = self.walk

        if self.last_frame_update > 0.07:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0  

    def load_sprites(self, x =50, y = 44):
        self.walk = []
        # Load frog sprite
        self.gummy = pygame.image.load("sprites/gummy_enemy/000.png").convert_alpha()
        gummy1 = pygame.image.load("sprites/gummy_enemy/001.png").convert_alpha()
        gummy2 = pygame.image.load("sprites/gummy_enemy/002.png").convert_alpha()
        gummy3 = pygame.image.load("sprites/gummy_enemy/003.png").convert_alpha()
        
        self.walk.append(pygame.transform.scale(self.gummy, (x, y)).convert_alpha())
        self.walk.append(pygame.transform.scale(gummy1, (x, y)).convert_alpha())
        self.walk.append(pygame.transform.scale(gummy2, (x, y)).convert_alpha())
        self.walk.append(pygame.transform.scale(gummy3, (x, y)).convert_alpha())

        self.image = self.walk[0]
        self.current_anim_list = self.walk


        