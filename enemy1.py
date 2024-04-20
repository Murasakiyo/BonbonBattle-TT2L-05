import pygame
import spritesheet

class Enemy1(pygame.sprite.Sprite):
    def __init__(self, game, group):
        super().__init__(group)
        self.game = game
        self.load_sprites()
        # self.rect = self.enemy.get_rect(width=, height=)
        # #initialize enemy position
        # self.rect.x, self.rect.y = 
        # self.current_frame = 0
        # self.last_frame_update = 0
        # self.fps =  #Animation speed


    def update(self, deltatime):
        pass

    def render(self, display):
        pass

    def animate(self, deltatime, direction_x, direction_y, distance):
        self.last_frame_update += deltatime


    def load_sprites(self):
        self.right_sprites, self.left_sprites = [], []
        self.walk_right, self.walk_left = [], []
        self.attack_right, self.attack_left = [], []
        #load enemy sprites from spritesheet
        # enemy_image = pygame.image.load().convert_alpha()

    