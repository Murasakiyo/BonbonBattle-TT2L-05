import pygame
import time
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

    def game_over(self,player_action):
        if self.exit_game:
            player_action["transition"] = True
            self.state = "exiting"
            player_action["reset_game"] = True
            
        if self.game.alpha == 255 and self.state == "exiting":
            if not(player_action["reset_game"]):
                self.exit_state(-1)
                player_action["transition"] =  False
                self.end = False
                self.game.win = False
                self.game.defeat = False
                self.state = "none"
                # self.game.start = False

    def game_restart(self, player_action):

        if self.restart_game:
            player_action["transition"] = True
            self.state = "restarting"
            player_action["reset_game"] = True
            
        if self.game.alpha == 255 and self.state == "restarting":
            if not(player_action["reset_game"]):
                player_action["transition"] =  False
                self.end = False
                self.game.win = False
                self.game.defeat = False
                self.state = "none"

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

    def button_go(self):
        if self.game.exit_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.exit_game = True
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.exit_game = False
                self.click = False

        if self.game.restart_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.restart_game = True
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.restart_game = False
                self.click = False

    def ending_options(self, deltatime, player_action, x, y):
        if self.enemy_defeat:
            self.current_time += deltatime
            self.spawn_sugarcubes(x, y)
            if not(self.sugarcube_received > x):
                self.sugarcube_collision()
            player_action["ultimate"] = False
            if self.current_time > 4:
                self.game.win = True
                if self.current_time > 5.5:
                    self.current_time = 0
                    self.end = True

        if self.player.healthpoints <= 0:
            self.game.defeat = True
            player_action["ultimate"] = False
            if self.player.image == self.player.lose_sprites[3]:
                self.end = True

class CameraGroup(pygame.sprite.Group):
    def __init__(self, game):
        super().__init__()
        self.game = game

    def custom_draw(self, display):
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            sprite.rect.clamp_ip(self.game.screen_rect)
            display.blit(sprite.image, sprite.rect)

            
