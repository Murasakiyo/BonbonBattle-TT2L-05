import pygame

class EnemyHealthBar():
    def __init__(self, game):
        self.game = game

    def enemy_health_update(self, enemyrectx, enemyrecty, HP, max_HP):
        self.enemy_health = pygame.Rect(enemyrectx, enemyrecty, (HP/max_HP) * 300, 10)
        self.boss_health = pygame.Rect(self.game.screen_rect.x + 750, self.game.screen_rect.y + 10, (300 - HP), 40)

    def enemy_moxie_update(self, moxie, max_moxie):
        self.enemy_moxie_rect = pygame.Rect(1060, 150, 30, 250)
        self.enemy_moxie_bar = pygame.Rect(1060, 150, 30, 250 - ((moxie/max_moxie) * 250))
        

    def enemy_health_render(self, display, enemyrectx, enemyrecty):
        pygame.draw.rect(display, "black", (enemyrectx, enemyrecty, 150, 10))
        pygame.draw.rect(display, "green", self.enemy_health)
    
    def boss_health_render(self, display):
        pygame.draw.rect(display, "red", (self.game.screen_rect.x + 750, self.game.screen_rect.y + 10, 300, 40))
        pygame.draw.rect(display, "black", self.boss_health)
        pygame.draw.rect(display, "purple", self.enemy_moxie_rect)
        pygame.draw.rect(display, "black", self.enemy_moxie_bar)

    # For sprite groups
    def groupenemy_health_render(self, display, group):
        for sprite in group:
            self.enemy_health_update(sprite.rect.x,sprite.rect.y, sprite.HP)
            pygame.draw.rect(display, "black", (sprite.rect.x, sprite.rect.y, 150, 10))
            pygame.draw.rect(display, "green", self.enemy_health)
    

