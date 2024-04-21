import pygame
import spritesheet

class Enemy3(pygame.sprite.Sprite):
    def __init__(self, game, group):
        super().__init__(group)
        self.game = game
        self.rect = pygame.Rect(180, 180, 40, 40)


    def update(self,deltatime, player_action, player_x, player_y):
        self.current_time += deltatime

        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]
        pass
    
    def render(self, display):
        pygame.draw.rect(display, (255, 255, 255), self.rect)
        pygame.display.flip()




    def animate(self, deltatime, direction_x, direction_y):
        pass


    def load_sprites(self):
        pass
