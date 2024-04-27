import pygame
import time
import math
import spritesheet
import state
import torres
# from minions import Minions

class Enemy3(pygame.sprite.Sprite):
    def __init__(self, game):
        # super().__init__(group)
        self.game = game
        self.camera = state.CameraGroup(self.game)
        self.player = torres.Player(self.game, self.camera)
        self.rect_draw = pygame.Rect(180, 180, 40, 40)
        self.enemyborder = pygame.Rect(100, 90, 900, 370)
        self.enemyborder1 = pygame.Rect(-895, 40, 900, 570) #left
        self.enemyborder2 = pygame.Rect(1095, 40, 900, 570) #right
        self.enemyborder3 = pygame.Rect(0, 560, 1100, 370) #bottom
        self.enemyborder4 = pygame.Rect(0, -330, 1100, 370) #top         
        self.color = "white"
        self.speed = -4
        self.attractspeed = 0
        self.current_time = 0
        self.start_time = time.time()
        self.spawnx = self.rect_draw.x - 10
        self.spawny = self.rect_draw.y + 10
        self.avoid = False


    def update(self, deltatime, player_action, player_x, player_y):
        direction_x = player_action["right"] - player_action["left"]
        direction_y = player_action["down"] - player_action["up"]

        self.move_towards_player(player_x, player_y)
        self.move_towards_border()
        self.rect_draw.clamp_ip(self.game.screen_rect)

        if pygame.Rect.colliderect(self.rect_draw, self.enemyborder1) == True:
            self.avoid = True

        if pygame.Rect.colliderect(self.rect_draw, self.enemyborder2) == True:
            self.avoid = True

        if pygame.Rect.colliderect(self.rect_draw, self.enemyborder3) == True:
            self.avoid = True

        if pygame.Rect.colliderect(self.rect_draw, self.enemyborder4) == True:
            self.avoid = True

        if self.avoid == True:
            self.current_time += deltatime
            if self.current_time > 0.75:
                self.avoid = False
                self.current_time = 0

        if self.avoid == True:
            self.attractspeed = 8
            self.speed = 0
        elif self.avoid == False:
            self.speed = -4
            self.attractspeed = 0


        # if self.follow == True:
        #     self.speed = 4
        # elif self.follow == False:
        #     self.speed = -4



                # if self.current_time > 0.3:
                #     player_action["attack"] = False
                #     self.attack = False
                #     self.current_time = 0
        print(self.current_time)





    def render(self, display):
        pygame.draw.rect(display, self.color, self.rect_draw)
        # pygame.draw.rect(display, "red", self.enemyborder)
        pygame.draw.rect(display, self.color, self.enemyborder1)
        pygame.draw.rect(display, self.color, self.enemyborder2)
        pygame.draw.rect(display, self.color, self.enemyborder3)
        pygame.draw.rect(display, self.color, self.enemyborder4) #draws the enemy border for refference
        pygame.display.flip()

    def move_towards_player(self, player_x, player_y):
        # Find direction vector (dx, dy) between enemy and player.
        dx, dy = player_x - self.rect_draw.x, player_y - self.rect_draw.y
        dist = math.hypot(dx, dy)

        dx, dy = dx / (dist + 1), dy / (dist + 1)  # Normalize.
        # Move along this normalized vector towards the player at current speed.
        self.rect_draw.x += dx * self.speed
        self.rect_draw.y += dy * self.speed

    def move_towards_border(self):
        dx, dy = self.game.screen_rect.center[0] - self.rect_draw.x, self.game.screen_rect.center[1] - self.rect_draw.y
        dist = math.hypot(dx, dy)

        dx, dy = dx / (dist + 1), dy / (dist + 1)
        self.rect_draw.x += dx * self.attractspeed
        self.rect_draw.y += dy * self.attractspeed

    # def timer(self):
    #     self.elapsed_time = time.time() - self.start_time
    #     self.time_remaining = int(self.countdown - self.elapsed_time)
    #     # print(self.time_remaining)

    #     if self.time_remaining < 0:
    #         self.running = False
    #         self.end = True
    #         # print("stop")
      



