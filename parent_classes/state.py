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

    def game_over(self, deltatime, player_action):
        if self.player.image == self.player.lose_sprites[3] and self.game.defeat:
            if self.game.defeat:
                player_action["transition"] = True
                if self.game.alpha >= 200:
                    self.game.reset_game = True
                    
        if self.game.alpha == 255:
            self.exit_state(-1)
            player_action["transition"] =  False
            self.game.defeat = False
            self.game.start = False

class CameraGroup(pygame.sprite.Group):
    def __init__(self, game):
        super().__init__()
        self.game = game

    def custom_draw(self, display):
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            display.blit(sprite.image, sprite.rect)
            
