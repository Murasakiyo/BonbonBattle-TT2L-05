import pygame
import sys
from states.level_1 import First_Stage
from states.menu import MainMenu
from savefile import *

class Game():
    def __init__(self):
        pygame.init()
        self.SCREENWIDTH, self.SCREENHEIGHT = 1100, 600
        self.game_canvas = pygame.Surface((self.SCREENWIDTH, self.SCREENHEIGHT), pygame.SRCALPHA)
        self.screen = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        self.screen_rect = self.screen.get_rect()
        self.run, self.play = True, True
        self.damaged = False
        self.clock = pygame.time.Clock()
        self.black_surface = pygame.Surface((self.SCREENWIDTH, self.SCREENHEIGHT), pygame.SRCALPHA)
        self.alpha = 0
        self.start = True
        # self.ct_display = 1
        self.deltatime, self.prevtime, self.current_time, self.countdown = 0 , 0, 0, 5
        self.backgrounds()

        # Action dictionary
        self.player_action = {"left":False, "right": False, "up": False, "down": False, "attack": False, "defend": False, 
                              "ultimate": False, "transition": False} 
    
        self.state_stack = []
        self.load_states()
        self.ultimates()
        
        self.save_system = SaveDataSystem()     
        self.save_file_path = 'saved_state.pickle'  # File path for saving the game state  
        # self.clear_save_file()  # call ONLY when want to RESTART the game
        
        if self.check_saved_state(): # check if saved game state data file exists
            # print("check_save_state returns true")
            self.load_saved_state(self.save_file_path)
        else:
            # print("check_save_state returns false")
            self.load_states() 

    # Game loop
    def game_loop(self):
        while self.play:
            self.getdeltatime() # compute delta time
            self.get_events() # check what is press
            self.update() # update the game according to presses
            self.render() # render to screen
            self.clock.tick((60))
            # print(self.deltatime)


    # All key events are here. Receive input from player, display output for player
    def get_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                self.play = False
                self.save_game_state(self.save_file_path) # save game state before exiting
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.player_action["left"] = True
                if event.key == pygame.K_d:
                    self.player_action["right"] = True
                if event.key == pygame.K_w:
                    self.player_action["up"] = True
                if event.key == pygame.K_s:
                    self.player_action["down"] = True
                if event.key == pygame.K_j:
                    self.player_action["attack"] = True
                if event.key == pygame.K_k:
                    self.player_action["defend"] = True
                if event.key == pygame.K_q:
                    self.player_action["ultimate"] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player_action["left"] = False
                if event.key == pygame.K_d:
                    self.player_action["right"] = False
                if event.key == pygame.K_w:
                    self.player_action["up"] = False
                if event.key == pygame.K_s:
                    self.player_action["down"] = False
                if event.key == pygame.K_q:
                    self.player_action["ultimate"] = False
        
   


    # Updates the state stack
    def update(self):
        self.state_stack[-1].update(self.deltatime, self.player_action)
        self.ct_display = str(int(self.countdown -self.current_time))


    # Rendering images on screen
    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        self.screen.blit(pygame.transform.scale(self.game_canvas,(self.SCREENWIDTH, self.SCREENHEIGHT)), (0,0)) #image, (width, height), coordinates
        self.transition()
        pygame.display.flip()


    # Frame time (Delta time: elapsed time since the last update/ 
    # Time difference between last frame and current frame)
    def getdeltatime(self):
        currenttime = pygame.time.get_ticks()
        self.deltatime = (currenttime - self.prevtime) / 1000.0
        self.prevtime = currenttime
        

    # Function to draw texts
    def draw_text(self, surface, text, colour, x, y, size):
        self.font = pygame.font.Font("Fonts/retro-pixel-cute-prop.ttf", size)
        text_surface = self.font.render(text, True, colour, size).convert_alpha()
        text_surface.set_colorkey((0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)

    # First state/room in the game (can be changed)
    def load_states(self):
        self.title_screen = MainMenu(self)
        self.state_stack.append(self.title_screen)

    # Reset all player keys
    def reset_keys(self):
        for actions in self.player_action:
            self.player_action[actions] = False

    # For all ultimates
    def ultimates(self):
        self.ult = False
        self.ult_finish = False
    
    # Transition screen between states
    def transition(self):
        if self.player_action["transition"]:
            self.alpha = min(self.alpha + 10, 255)
        else:
            if self.alpha != 0:
                self.alpha = max(self.alpha - 10, 0)
        self.black_surface.fill((0,0,0, self.alpha))

        self.screen.blit(self.black_surface, (0,0))
        pygame.display.flip()

    # Timer before Game Start
    def start_timer(self):
        self.current_time += self.deltatime
        if int(self.countdown - self.current_time) == 0:
            self.start = True
            self.current_time = 0
        
    def backgrounds(self):
        self.forest = pygame.image.load("sprites/bg_earlylvl.bmp").convert()
        self.black = pygame.image.load("sprites/black.png").convert_alpha()
        self.trees = pygame.image.load("sprites/asset_earlylvl.png").convert_alpha()


    ### FILE SAVING ###
    def check_saved_state(self):
        return self.save_system.check_saved_state(self.save_file_path)

    def save_game_state(self, file_path):
        current_state = self.state_stack[-1]
        current_state_data = current_state.get_state_data()  # saved in dictionary
        self.save_system.save_game_state(current_state_data, file_path)
         
    def load_saved_state(self, file_path):
        saved_state_data = self.save_system.load_game_state(file_path)  # return data in dictionary (saved_state_data is a dictionary)
        
        if saved_state_data:
            saved_level = saved_state_data['level']
            if saved_level == 1:
                level_object = First_Stage(self)
                level_object.player.rect.x, level_object.player.rect.y = saved_state_data['player_position']
                level_object.player_attack = saved_state_data['player_attack']
                level_object.healthpoints = saved_state_data['player_health']
                # level_object.moxie_points = saved_state_data['player_moxie_points']
                level_object.take_damage = saved_state_data['playerEnemy_take_damage']
                level_object.ultimate = saved_state_data['player_ultimate']
                level_object.attack_time = saved_state_data['player_attack_time']
                level_object.let_attack = saved_state_data['player_let_attack']
                level_object.attack_cooldown = saved_state_data['player_attack_cooldown']
                level_object.enemy1.rect.x, level_object.enemy1.rect.y = saved_state_data['enemy_position']
                # level_object.frog_HP = saved_state_data['enemy_health']
                self.state_stack.append(level_object)
            # elif saved_level == 2:
            #     level_object = Sec_Stage(self)
            #     self.state_stack.append(level_object)
            # print("Game state loaded successfully.")
        else:
            print("No saved state data available.")

    # be called when want to restart the game 
    def clear_save_file(self):
        import os
        if os.path.exists(self.save_file_path):
            os.remove(self.save_file_path)
        self.save_game_state(self.save_file_path)


if __name__ == "__main__":
    game = Game()
    while game.run:
        game.game_loop()
