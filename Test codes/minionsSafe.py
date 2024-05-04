import pygame
import math
import parent_classes.state as state

# This file is just for safekeeping in case the original code descends to hell

class Minions(pygame.sprite.Sprite):
    def __init__(self, game, enemy3_rectx, enemy3_recty):
        super().__init__()
        self.game = game
        self.camera = state.CameraGroup(self.game)
        self.rect = pygame.Rect(enemy3_rectx - 100, enemy3_recty, 30, 30) #left
        # self.rect2 = pygame.Rect(enemy3_rectx + 100, enemy3_recty, 30, 30) #right
        # self.rect3 = pygame.Rect(enemy3_rectx, enemy3_recty + 100, 30, 30) #bottom
        # self.rect4 = pygame.Rect(enemy3_rectx, enemy3_recty - 100, 30, 30) #top
        self.speed = 3

    def update(self, deltatime, player_action, player_x, player_y, enemy3_rectx, enemy3_recty):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]


        self.rect.clamp_ip(self.game.screen_rect)
        # player_rect.clamp_ip(self.game.screen_rect)

        self.move_towards_player(player_x, player_y)



    def render(self, display):
        pygame.draw.rect(display, (255, 0, 255), self.rect)
        pygame.draw.rect(display, (255, 0, 255), self.rect2)
        pygame.draw.rect(display, (255, 0, 255), self.rect3)
        pygame.draw.rect(display, (255, 0, 255), self.rect4)
        pygame.display.flip()

    def move_towards_player(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player_x - self.rect.x, player_y - self.rect.y
        dx2, dy2 = player_x - self.rect2.x, player_y - self.rect2.y
        dx3, dy3 = player_x - self.rect3.x, player_y - self.rect3.y
        dx4, dy4 = player_x - self.rect4.x, player_y - self.rect4.y
        dist = math.hypot(dx, dy)

        dx, dy = dx / (dist + 1), dy / (dist + 1)
        dx2, dy2 = dx2 / (dist + 1), dy2 / (dist + 1)
        dx3, dy3 = dx3 / (dist + 1), dy3 / (dist + 1)
        dx4, dy4 = dx4 / (dist + 1), dy4 / (dist + 1)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect.x += dx * self.speed
        self.rect.y += dy * self.speed

        self.rect2.x += dx2 * self.speed
        self.rect2.y += dy2 * self.speed

        self.rect3.x += dx3 * self.speed
        self.rect3.y += dy3 * self.speed

        self.rect4.x += dx4 * self.speed
        self.rect4.y += dy4 * self.speed


    def minion_spawn(self):
        if len(self.minionlist) == 0:
                new_minion = Minions(self.game,self.enemy3_rect.x, self.enemy3_rect.y)
                self.minionlist.add(new_minion) 

        if len(self.minionlist) == 1:
            for self.minions in self.minionlist.sprites():
                # if self.cupcake.rect.bottom > 200:
                    new_minion = Minions2(self.game,self.enemy3_rect.x, self.enemy3_rect.y)
                    self.minionlist.add(new_minion)

        if len(self.minionlist) == 2:
            for self.minions in self.minionlist.sprites():
                # if self.cupcake.rect.bottom > 200:
                    new_minion = Minions3(self.game,self.enemy3_rect.x, self.enemy3_rect.y)
                    self.minionlist.add(new_minion)

        if len(self.minionlist) == 3:
            for self.minions in self.minionlist.sprites():
                # if self.cupcake.rect.bottom > 200:
                    new_minion = Minions4(self.game,self.enemy3_rect.x, self.enemy3_rect.y)
                    self.minionlist.add(new_minion)