import pygame
import math
import state

class Minions(pygame.sprite.Sprite):
    def __init__(self, game, enemy3_rect):
        # super().__init__(group)
        self.game = game
        self.camera = state.CameraGroup(self.game)
        self.mini_rect = pygame.Rect(enemy3_rect.x - 100, enemy3_rect.y + 10, 30, 30)
        self.speed = 3

    def update(self, deltatime, player_action, player_x, player_y, player_rect):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        player_rect.x += 400 * deltatime * direction_x 
        player_rect.y += 450 * deltatime * direction_y 

        self.mini_rect.clamp_ip(self.game.screen_rect)
        player_rect.clamp_ip(self.game.screen_rect)

        self.move_towards_player(player_x, player_y)



    def render(self, display):
        pygame.draw.rect(display, (255, 0, 255), self.mini_rect)
        pygame.display.flip()

    def move_towards_player(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player_x - self.mini_rect.x, player_y - self.mini_rect.y
        dist = math.hypot(dx, dy)

        dx, dy = dx / (dist + 1), dy / (dist + 1)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.mini_rect.x += dx * self.speed
        self.mini_rect.y += dy * self.speed