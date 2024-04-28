import pygame
import math
import state

class Minions(pygame.sprite.Sprite):
    def __init__(self, game, enemy3_rectx, enemy3_recty):
        super().__init__()
        self.game = game
        self.camera = state.CameraGroup(self.game)
        self.rect = pygame.Rect(enemy3_rectx - 100, enemy3_recty, 30, 30) #left
        self.speed = 3

    def update(self, deltatime, player_action, player_x, player_y, enemy3_rectx, enemy3_recty):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]


        self.rect.clamp_ip(self.game.screen_rect)
        # player_rect.clamp_ip(self.game.screen_rect)

        self.move_towards_player(player_x, player_y)



    def render(self, display):
        pygame.draw.rect(display, (255, 0, 255), self.rect)
        pygame.display.flip()

    def move_towards_player(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player_x - self.rect.x, player_y - self.rect.y
        dist = math.hypot(dx, dy)

        dx, dy = dx / (dist + 1), dy / (dist + 1)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

#############################################################################################

class Minions2(pygame.sprite.Sprite):
    def __init__(self, game, enemy3_rectx, enemy3_recty):
        super().__init__()
        self.game = game
        self.camera = state.CameraGroup(self.game)
        self.rect = pygame.Rect(enemy3_rectx + 100, enemy3_recty, 30, 30) #right
        self.speed = 3

    def update(self, deltatime, player_action, player_x, player_y, enemy3_rectx, enemy3_recty):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]


        self.rect.clamp_ip(self.game.screen_rect)
        # player_rect.clamp_ip(self.game.screen_rect)

        self.move_towards_player(player_x, player_y)



    def render(self, display):
        pygame.draw.rect(display, (255, 0, 255), self.rect)
        pygame.display.flip()

    def move_towards_player(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx2, dy2 = player_x - self.rect.x, player_y - self.rect.y
        dist = math.hypot(dx2, dy2)

        dx2, dy2 = dx2 / (dist + 1), dy2 / (dist + 1)  # Normalize.
        # Move along this normalized vector towards the player at current speed.

        self.rect.x += dx2 * self.speed
        self.rect.y += dy2 * self.speed

#######################################################################################

class Minions3(pygame.sprite.Sprite):
    def __init__(self, game, enemy3_rectx, enemy3_recty):
        super().__init__()
        self.game = game
        self.camera = state.CameraGroup(self.game)
        self.rect = pygame.Rect(enemy3_rectx, enemy3_recty + 100, 30, 30) #bottom
        self.speed = 3

    def update(self, deltatime, player_action, player_x, player_y, enemy3_rectx, enemy3_recty):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]


        self.rect.clamp_ip(self.game.screen_rect)
        # player_rect.clamp_ip(self.game.screen_rect)

        self.move_towards_player(player_x, player_y)



    def render(self, display):
        pygame.draw.rect(display, (255, 0, 255), self.rect)
        pygame.display.flip()

    def move_towards_player(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx3, dy3 = player_x - self.rect.x, player_y - self.rect.y
        dist = math.hypot(dx3, dy3)

        dx3, dy3 = dx3 / (dist + 1), dy3 / (dist + 1)  # Normalize.
        # Move along this normalized vector towards the player at current speed.

        self.rect.x += dx3 * self.speed
        self.rect.y += dy3 * self.speed

###############################################################################################

class Minions4(pygame.sprite.Sprite):
    def __init__(self, game, enemy3_rectx, enemy3_recty):
        super().__init__()
        self.game = game
        self.camera = state.CameraGroup(self.game)
        self.rect = pygame.Rect(enemy3_rectx, enemy3_recty - 100, 30, 30) #top
        self.speed = 3

    def update(self, deltatime, player_action, player_x, player_y, enemy3_rectx, enemy3_recty):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]


        self.rect.clamp_ip(self.game.screen_rect)
        # player_rect.clamp_ip(self.game.screen_rect)

        self.move_towards_player(player_x, player_y)



    def render(self, display):
        pygame.draw.rect(display, (255, 0, 255), self.rect)
        pygame.display.flip()

    def move_towards_player(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx4, dy4 = player_x - self.rect.x, player_y - self.rect.y
        dist = math.hypot(dx4, dy4)

        dx4, dy4 = dx4 / (dist + 1), dy4 / (dist + 1)  # Normalize.
        # Move along this normalized vector towards the player at current speed.

        self.rect.x += dx4 * self.speed
        self.rect.y += dy4 * self.speed
        