import pygame

class EnemyHealthBar():
    def __init__(self, game):
        self.game = game

    def enemy_health_update(self, enemyrectx, enemyrecty, HP):
        self.enemy_health = pygame.Rect(enemyrectx, enemyrecty, HP, 10)
        self.boss_health = pygame.Rect(self.game.screen_rect.x + 600, self.game.screen_rect.y + 10, HP, 40)

    def enemy_health_render(self, display, enemyrectx, enemyrecty):
        pygame.draw.rect(display, "black", (enemyrectx, enemyrecty, 150, 10))
        pygame.draw.rect(display, "green", self.enemy_health)
    
    def boss_health_render(self, display):
        pygame.draw.rect(display, "black", (self.game.screen_rect.x + 600, self.game.screen_rect.y + 10, 300, 40))
        pygame.draw.rect(display, "red", self.boss_health)

    # For sprite groups
    def groupenemy_health_render(self, display, group):
        for sprite in group:
            self.enemy_health_update(sprite.rect.x,sprite.rect.y, sprite.HP)
            pygame.draw.rect(display, "black", (sprite.rect.x, sprite.rect.y, 150, 10))
            pygame.draw.rect(display, "green", self.enemy_health)
    

