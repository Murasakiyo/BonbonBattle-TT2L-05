import pygame
import spritesheet

class Enemy3(pygame.sprite.Sprite):
    def __init__(self, game, group):
        super().__init__(group)
        self.game = game
        self.rect = pygame.Rect(180, 180, 40, 40)


    def update():
        pass

    def render(self, display):
        pygame.draw.rect(display, (255, 255, 255), self.rect)
        pygame.display.flip()

    def animate(self, deltatime, direction_x, direction_y):
        self.last_frame_update += deltatime




    def load_sprites(self):
        self.right_sprites, self.left_sprites = [], []
        enemy3 = pygame.image.load("sprites/louie_walk_sprite.png").convert()
        self.enemy3_walk = pygame.transform.scale(enemy3, (600, 120)).convert_alpha()
        SP = spritesheet.Spritesheet(self.enemy3_walk)

        for x in range(4):
            self.right_sprites.append(SP.get_sprite(x,75,120, (21, 255, 0)))
        for x in range(4,8):
            self.left_sprites.append(SP.get_sprite(x,75,120, (21, 255, 0)))

        self.image = self.right_sprites[0]
        self.current_anim_list = self.right_sprites
