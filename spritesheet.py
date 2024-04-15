import pygame

class Spritesheet:
    def __init__(self, image):
        self.sprite_sheet = image

    def get_sprite(self, frame, y, width, height, colour):
        sprite = pygame.Surface((width, height)).convert_alpha()
        sprite.blit(self.sprite_sheet, (0,0), ((frame*width), y, width, height))
        sprite.set_colorkey(colour)
        return sprite