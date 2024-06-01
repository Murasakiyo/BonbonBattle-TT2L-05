import pygame
vec = pygame.math.Vector2

class LoungeCamera(pygame.sprite.Group):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()
        self.offset_float = vec(0, 0)
        self.background = {
            "grass": pygame.image.load("sprites/backgrounds/ground.bmp").convert(),
            "sky": pygame.transform.scale(pygame.image.load("sprites/lounge.bmp"), (2125,750)).convert(),
        }
        self.h_width = self.display_surface.get_size()[0] // 2
        self.h_height = self.display_surface.get_size()[1] // 2
        self.bg = self.background["sky"]
        self.bg_rect = self.bg.get_rect(topleft=(0,-330))
        self.grass = self.background["grass"]
        self.grass_rect = self.bg.get_rect(topleft=(0,410))
        self.circus_rect = pygame.Rect(0,260,100,200)
        self.level_rect = pygame.Rect(0,260,500,200)


    def center_target(self, target):
        self.offset.x = target.rect.centerx - self.h_width
        self.offset.y = target.rect.centery - self.h_height
        target.rect.clamp_ip(self.bg_rect)

        if self.offset.x >= 1010:
            self.offset.x = 1010
        if self.offset.x <= 15:
            self.offset.x = 15


    def custom_draw(self, display, player):
        self.center_target(player)
        sky_offset = self.bg_rect.topleft - self.offset
        grass_offset = self.grass_rect.topleft - self.offset 
        self.circus_rect.x = grass_offset.x + 700
        self.level_rect.x = grass_offset.x + 1600
        display.blit(self.bg, sky_offset)
        display.blit(self.grass, grass_offset)


        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.midleft - self.offset
            display.blit(sprite.image, offset_pos)

        # print(f"offset:{}, rect: x={}, y={}")
        