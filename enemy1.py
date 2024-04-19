import pygame
import spritesheet

class Enemy1(pygame.sprite.Sprite):
    def __init__(self, game, group):
        super().__init__(group)
        self.game = game
        # # self.load_sprites()
        # self.rect = self.enemy.get_rect(width=, height=)
        # #initialize enemy position
        # self.rect.x, self.rect.y = 
        # self.current_frame = 0
        # self.last_frame_update = 0
        # self.fps =  #Animation speed
        # self.speed =  #Enemy speed
        # self.player = None #Reference to the player object

        # Using a circle as a placeholder for enemy1
        self.image = pygame
        self.radius = 20
        self.color = (0, 0, 0)
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()

    def update(self):
        pass

    def render(self, display):
        pass
        # pygame.draw.rect(display, (255,255,255), self.rect,2)

    def animate(self, deltatime, direction_x, direction_y, distance):
        self.last_frame_update += deltatime


    def load_sprites(self):
        pass
        #load enemy sprites from spritesheet
        # enemy_image = pygame.image.load().convert_alpha()
