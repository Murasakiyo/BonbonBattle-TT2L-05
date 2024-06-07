import pygame
from currency import Sugarcube

class SugarcubeSpawn():
    def __init__(self, game):
        self.game = game

    def spawn_sugarcubes(self, num_sugarcubes, x):
        if len(self.sugarcube_list) < num_sugarcubes - x:
            if self.sugarcube_received < num_sugarcubes:
                for x in range(num_sugarcubes):
                    sugarcube = Sugarcube(self.game, self.current_sugarcube_value)
                    self.sugarcube_list.add(sugarcube)

    def reset_sugarcubes(self, x, y):
        self.current_sugarcube_value = x 
        self.sugarcube_list.empty()  # clear the current sugarcubes
        self.spawn_sugarcubes(y)  # Spawn new sugarcubes based on the level

    def sugarcube_collision(self):
        # self.sugarcube_list.update()
        for sugarcube in self.sugarcube_list:
            if sugarcube.rect.colliderect(self.player.rect):
                # print("collide")
                sugarcube.collect(self.player)
                self.sugarcube_received += 1
                # print(f"Remaining sugarcubes: {len(self.sugarcube_list)}")