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

        if self.exit_game:
            player_action["transition"] = True
            self.game.reset_game = True
            
        if self.game.alpha == 255:
            if self.game.reset_game == False:
                self.exit_state(-1)
                player_action["transition"] =  False
                self.end = False
                self.game.win = False
                self.game.defeat = False
                self.game.start = False
                
                
        # if self.player.image == self.player.lose_sprites[3] and self.game.defeat:
        #     if self.game.defeat:
        #         player_action["transition"] = True
        #         if self.game.alpha >= 220:
        #             self.game.reset_game = True
                    
        # if self.game.alpha == 255:
        #     if self.game.reset_game == False:
        #         self.exit_state(-1)
        #         player_action["transition"] =  False
        #         self.game.defeat = False
        #         self.game.start = False

    def ending_state(self, display):
        if self.game.defeat:
            self.game.end_screen = self.game.lose_screen
        else:
            self.game.end_screen = self.game.win_screen
            
        display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
        display.blit(self.game.end_screen, (250,5))
        self.hover_button(display, self.game.exit_rect, self.game.current_exit, self.game.exit, self.game.exit_hover)
        self.hover_button(display, self.game.restart_rect, self.game.current_restart, self.game.restart, self.game.restart_hover)

        
    def ending_update(self, player_action, button_rect):
        if button_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.exit_game = True
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.exit_game = False
                self.click = False
        
    def hover_button(self, display, button_rect, current_button, norm_but, hover_but):
        if button_rect.collidepoint(self.game.mouse):
            current_button = hover_but
        else:
            current_button = norm_but

        display.blit(current_button, (button_rect.x, button_rect.y))

class CameraGroup(pygame.sprite.Group):
    def __init__(self, game):
        super().__init__()
        self.game = game

    def custom_draw(self, display):
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            display.blit(sprite.image, sprite.rect)
            
