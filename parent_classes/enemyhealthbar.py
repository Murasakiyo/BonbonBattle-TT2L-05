import pygame

class EnemyHealthBar():
    def __init__(self, game):
        self.game = game

    def enemy_health_update(self, enemyrectx, enemyrecty, HP):
        self.enemy_health = pygame.Rect(enemyrectx, enemyrecty, HP, 10)

    def enemy_health_render(self, display, enemyrectx, enemyrecty):
        pygame.draw.rect(display, "black", (enemyrectx, enemyrecty, 150, 10))
        pygame.draw.rect(display, "green", self.enemy_health)
    
    # For sprite groups
    def groupenemy_health_render(self, display, group):
        for sprite in group:
            self.enemy_health_update(sprite.rect.x,sprite.rect.y, sprite.HP)
            pygame.draw.rect(display, "black", (sprite.rect.x, sprite.rect.y, 150, 10))
            pygame.draw.rect(display, "green", self.enemy_health)
    

