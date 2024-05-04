import pygame

class State():
    def __init__(self, game):
        self.game = game
        self.prev_state = None

    def update(self, deltatime, player_action):
        pass

    def render(self,surface):
        pass

    def enter_state(self):
        if len(self.game.state_stack) > 1:
            self.prev_state = self.game.state_stack[-1]
        self.game.state_stack.append(self) #push

    # Modified from original code
    def exit_state(self, x):
        self.game.state_stack.pop(x) 

class CameraGroup(pygame.sprite.Group):
    def __init__(self, game):
        super().__init__()
        self.game = game

    def custom_draw(self, display):
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            display.blit(sprite.image, sprite.rect)
            
