import pygame

class Moxie():
    def __init__(self, game):
        self.game = game
        
    def load_moxie_bar(self):
        self.moxie_rect = pygame.Rect(10, 150, 30, 250)
        self.moxie_bar = pygame.Rect(10, 150, 30, 250 - self.player.moxiepoints)
        self.chocolate = pygame.image.load("sprites/chocolate.png")
        self.image = pygame.transform.scale(self.chocolate, (50, 63))

    def moxie_update(self, player_action):
        self.moxie_bar = pygame.Rect(10, 150, 30, 250 - self.player.moxiepoints)
        if player_action["ultimate"]:
            if self.player.moxiepoints >= 250:
                self.game.ult = True
                if not(self.init_stan):
                    self.player.moxiepoints = 0
                else:
                    self.player.moxiepoints = self.player.moxiepoints


    def moxie_render(self, display):
        pygame.draw.rect(display, "purple", self.moxie_rect)
        pygame.draw.rect(display, "black", self.moxie_bar)
        display.blit(self.image, (self.moxie_bar.x - 10, self.moxie_bar.y + 250))