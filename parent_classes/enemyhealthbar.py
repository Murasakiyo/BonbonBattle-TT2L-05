import pygame

class EnemyHealthBar():
    def __init__(self, game):
        self.game = game


    def load_enemy_health(self, enemy, enemyrectx, enemyrecty, HP, activate_code):
        if activate_code == False:
            self.enemy_health = pygame.Rect(enemyrectx, enemyrecty, enemy.HP, 10)

        if activate_code == True:
            self.enemy_health = pygame.Rect(enemyrectx, enemyrecty, HP, 10)

    def enemy_health_update(self, enemy, enemyrectx, enemyrecty, HP, activate_code):
        if activate_code == False:
            self.enemy_health = pygame.Rect(enemyrectx, enemyrecty, enemy.HP, 10)
        if activate_code == True:
            self.enemy_health = pygame.Rect(enemyrectx, enemyrecty, HP, 10)

# if self.check_type == self.enemies2 # code suggestion idea for fix

    def enemy_health_render(self, display, enemyrectx, enemyrecty):
        pygame.draw.rect(display, "black", (enemyrectx, enemyrecty, 150, 10))
        pygame.draw.rect(display, "green", self.enemy_health)

