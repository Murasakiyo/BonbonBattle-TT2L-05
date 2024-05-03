import pygame

# def changColor(image, maskImage, newColor):
#     colouredImage = pygame.Surface(image.get_size())
#     colouredImage.fill(newColor)
    
#     masked = maskImage.copy()
#     masked.set_colorkey((0, 0, 0))
#     masked.blit(colouredImage, (0, 0), None, pygame.BLEND_RGBA_MULT)

#     finalImage = image.copy()
#     finalImage.blit(masked, (0, 0), None)

#     return finalImage

# pygame.init()
# window = pygame.display.set_mode((1000,500))

# image = pygame.image.load('sprites/ult_anim/krie_ult/004.png').convert_alpha()
# maskImage = pygame.image.load('sprites/ult_anim/krie_ult/004.png').convert_alpha()

# colors = []
# colors.append(pygame.Color(0))
# colors[-1].hsla = (0, 100, 68)

# images = [changColor(image, maskImage, c) for c in colors]

# clock = pygame.time.Clock()
# nextColorTime = 0
# run = True
# while run:
#     clock.tick(60)
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False

#     window.fill((255, 255, 255))
#     for i, image in enumerate(images):
#         window.blit(image, (0,0))
#     pygame.display.flip()

# pygame.quit()
# exit()


def damage_animation(self):
    """
    Put a red overlay over sprite to indicate damage.
    """
    if self.damaged:
        damage_image = copy.copy(self.image).convert_alpha()
        damage_image.fill((255, 0, 0, self.damage_alpha), special_flags=pg.BLEND_RGBA_MULT)
        self.image.blit(damage_image, (0, 0))
        if self.fade_in:
            self.damage_alpha += 25
            if self.damage_alpha >= 255:
                self.fade_in = False
                self.damage_alpha = 255
        elif not self.fade_in:
            self.damage_alpha -= 25
            if self.damage_alpha <= 0:
                self.damage_alpha = 0
                self.damaged = False
                self.fade_in = True
                self.image = self.spritesheet_dict['facing left 2']
                self.image = pg.transform.scale2x(self.image)