import pygame
import sys
from states.menu import MainMenu
from torres import *
from states.level_4 import Quad_Stage
from states.pause_menu import Pause
from states.first_cutscene import Story
from states.lounge import Lounge
from states.level_choose import Level_Options
from states.game_set import Game_Settings
from parent_classes.particleeffect import *
# from parent_classes.ultimate_action import *
from settings import Settings
from music import Sounds
from savingsystem import *
from itertools import repeat

class Game():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Bonbon Battle: Treading Through Cotton Woods")
        icon = pygame.image.load("sprites/icon.png") 
        pygame.display.set_icon(icon)
        self.SCREENWIDTH, self.SCREENHEIGHT = 1100, 600
        self.game_canvas = pygame.Surface((self.SCREENWIDTH, self.SCREENHEIGHT), pygame.SRCALPHA)
        self.shakescreen = pygame.display.set_mode((self.SCREENWIDTH, self.SCREENHEIGHT))
        self.screen = self.shakescreen.copy()
        self.offset = repeat((0,0))
        self.screen_rect = self.screen.get_rect()
        self.run, self.play = True, True
        self.clock = pygame.time.Clock()
        self.black_surface = pygame.Surface((self.SCREENWIDTH, self.SCREENHEIGHT), pygame.SRCALPHA)
        self.alpha = 0
        self.start = True
        self.reset_game = False
        self.deltatime, self.prevtime, self.current_time, self.countdown, self.freeze_time = 0 , 0, 0, 4, 0
        self.settings = Settings()
        self.sounds = Sounds(self)
        self.backgrounds()
        self.buttons()

        # Action dictionary
        self.player_action = {"left":False, "right": False, "up": False, "down": False, "attack": False, "defend": False, 
                              "ultimate": False, "transition": False, "go": False, "pause": False, "reset_game":False, "next": False,
                              "E": False} 
    
        self.cutscene = {"Intro": False}
        self.state_stack = []
        self.load_states()
        self.battle_state()

        self.first_game = False
        self.skip_cutscenes = False
        self.current_currency = 0
        self.current_level = 0
        self.saving_system = SaveDataSystem('player_data.pickle', self)
        self.load_data() # load saved data when start a game
        
        self.particle = ParticleFunctions(self) # Changing all particle functions to have self.game.particle

    # Game loop
    def game_loop(self):
        while self.play:
            self.getdeltatime() # compute delta time
            self.get_events() # check what is press
            self.update() # update the game according to presses
            self.render() # render to screen
            self.clock.tick((60))


    # First state/room in the game (can be changed)
    def load_states(self):
        self.title_screen = MainMenu(self)
        self.state_stack.append(self.title_screen)

        
    # All key events are here. Receive input from player, display output for player
    def get_events(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run = False
                self.play = False
                self.save_data() # save data when quit the game
                sys.exit()

            self.mouse = pygame.mouse.get_pos()

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
                if event.key == pygame.K_RETURN:
                    self.player_action["go"] = True
                if event.key == pygame.K_BACKSPACE:
                    self.player_action["pause"] = True
                if event.key == pygame.K_SPACE:
                    self.player_action["next"] = True
                if event.key == pygame.K_e:
                    self.player_action["E"] = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.player_action["left"] = False
                if event.key == pygame.K_d:
                    self.player_action["right"] = False
                if event.key == pygame.K_w:
                    self.player_action["up"] = False
                if event.key == pygame.K_s:
                    self.player_action["down"] = False
                if event.key == pygame.K_k:
                    self.player_action["defend"] = False
                if event.key == pygame.K_q:
                    self.player_action["ultimate"] = False
                if event.key == pygame.K_RETURN:
                    self.player_action["go"] = False
                if event.key == pygame.K_BACKSPACE:
                    self.player_action["pause"] = False
                if event.key == pygame.K_SPACE:
                    self.player_action["next"] = False
                if event.key == pygame.K_e:
                    self.player_action["E"] = False
        
   
    # Updates the state stack
    def update(self):
        self.state_stack[-1].update(self.deltatime, self.player_action)
        self.ct_display = str(int(self.countdown - self.current_time))
        

    # Rendering images on screen
    def render(self):
        self.state_stack[-1].render(self.game_canvas)
        self.shakescreen.blit(self.screen, next(self.offset))
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
    def draw_text(self, surface, text, bold, colour, x, y, size):
        self.font = pygame.font.Font("Fonts/retro-pixel-cute-prop.ttf", size)
        text_surface = self.font.render(text, bold, colour, size).convert_alpha()
        text_surface.set_colorkey((0,0,0))
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_surface, text_rect)

    # Reset all player keys
    def reset_keys(self):
        for actions in self.player_action:
            self.player_action[actions] = False

    # For all battle states
    def battle_state(self):
        self.ult = False
        self.ult_finish = False
        self.freeze = False
        self.defeat = False
        self.win = False
        self.init_reset = False
    
    # Louie's freeze ultimate
    def frozen(self):
        if self.freeze:
            self.freeze_time += self.deltatime
            if self.freeze_time > 5:
                self.freeze = False
                self.freeze_time = 0

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

    # Screen shake
    def screen_shake(self, intensity, amplitude):
        s = -1
        for i in range(0,3):
            for x in range(0, amplitude, intensity):
                yield x * s, 0
            for x in range(0, amplitude, intensity):
                yield x * s, 0
            s *= -1
        while True:
            yield 0,0

    # Timer before Game Start
    def start_timer(self):
        self.current_time += self.deltatime
        if int(self.countdown - self.current_time) == 0:
            self.start = True
            self.current_time = 0
          
    # Backgrounds ingame
    def backgrounds(self):
        self.forest = pygame.image.load("sprites/backgrounds/bg_earlylvl.bmp").convert()
        self.black = pygame.image.load("sprites/black.png").convert_alpha()
        self.trees = pygame.image.load("sprites/asset_earlylvl.png").convert_alpha()
        self.mount_asset = pygame.image.load("sprites/asset_lvl4.png").convert_alpha()
        self.forest2 = pygame.image.load("sprites/backgrounds/bg_lvl2.bmp").convert()
        self.forest3 = pygame.image.load("sprites/backgrounds/bg_lvl3.bmp").convert()
        self.mountain = pygame.image.load("sprites/backgrounds/bg_lvl4.bmp").convert()
        self.lose_screen = pygame.image.load("sprites/lose_screen.png").convert_alpha()
        self.win_screen = pygame.image.load("sprites/win_screen.png").convert_alpha()
        self.circus = pygame.image.load("sprites/circus.png").convert()
        self.shop = pygame.image.load("sprites/shop.png").convert_alpha()
        self.end_screen = self.win_screen

        sugarcube_image = pygame.image.load("sprites/sugarcube.png").convert_alpha()
        self.sugarcube_image = pygame.transform.scale(sugarcube_image, (25,25)).convert_alpha()
    
    # Buttons for all
    def buttons(self):
        self.lvl1 = pygame.image.load("sprites/buttons/lvl1.png").convert_alpha()
        self.lvl2 = pygame.image.load("sprites/buttons/lvl2.png").convert_alpha()
        self.lvl3 = pygame.image.load("sprites/buttons/lvl3.png").convert_alpha()
        self.lvl4 = pygame.image.load("sprites/buttons/lvl4.png").convert_alpha()
        self.lvl5 = pygame.image.load("sprites/buttons/lvl5.png").convert_alpha()
        self.exit = pygame.image.load("sprites/buttons/exit.png").convert_alpha()
        self.button = pygame.image.load("sprites/buttons/button.png").convert_alpha()
        self.resume = pygame.image.load("sprites/buttons/resume.png").convert_alpha()
        self.restart = pygame.image.load("sprites/buttons/restart.png").convert_alpha()
        self.E_button = pygame.image.load("sprites/buttons/E.png").convert_alpha()
        self.A_button = pygame.image.load("sprites/buttons/A.png").convert_alpha()
        self.D_button = pygame.image.load("sprites/buttons/D.png").convert_alpha()
        self.backspace = pygame.image.load("sprites/buttons/backspace.png").convert_alpha()
        self.up = pygame.image.load("sprites/buttons/up.png").convert_alpha()
        self.down = pygame.image.load("sprites/buttons/down.png").convert_alpha()
        self.buy = pygame.image.load("sprites/buttons/buy.png").convert_alpha()

        self.lvl1_hover = pygame.image.load("sprites/buttons/lvl1_hover.png").convert_alpha()
        self.lvl2_hover = pygame.image.load("sprites/buttons/lvl2_hover.png").convert_alpha()
        self.lvl3_hover = pygame.image.load("sprites/buttons/lvl3_hover.png").convert_alpha()
        self.lvl4_hover = pygame.image.load("sprites/buttons/lvl4_hover.png").convert_alpha()
        self.lvl5_hover = pygame.image.load("sprites/buttons/lvl5_hover.png").convert_alpha()
        self.exit_hover = pygame.image.load("sprites/buttons/exit_hover.png").convert_alpha()
        self.button_hover = pygame.image.load("sprites/buttons/button_hover.png").convert_alpha()
        self.resume_hover = pygame.image.load("sprites/buttons/resume_hover.png").convert_alpha()
        self.restart_hover = pygame.image.load("sprites/buttons/restart_hover.png").convert_alpha()
        self.buy_hover = pygame.image.load("sprites/buttons/buy_hover.png").convert_alpha()

        self.lvl2_lock = pygame.image.load("sprites/buttons/lvl2_lock.png").convert_alpha()
        self.lvl3_lock = pygame.image.load("sprites/buttons/lvl3_lock.png").convert_alpha()
        self.lvl4_lock = pygame.image.load("sprites/buttons/lvl4_lock.png").convert_alpha()
        self.lvl5_lock = pygame.image.load("sprites/buttons/lvl5_lock.png").convert_alpha()

        self.button1 = self.lvl1.get_rect(width= 100, height=100)
        self.button1.x, self.button1.y = 75,225
        self.exit_rect = self.exit.get_rect(width= 126, height=126)
        self.exit_rect.x, self.exit_rect.y = 300,400
        self.restart_rect = self.restart.get_rect(width= 126, height=126)
        self.restart_rect.x, self.restart_rect.y = 690,400
        self.current_exit = self.exit
        self.current_restart = self.restart

    def save_data(self):
        self.saving_system.save_data_file()
        player_data = self.saving_system.get_save_data()
        print(f"Saving data: {player_data}")

    def load_data(self):
        if not self.first_game:
            loaded_data = self.saving_system.load_data_file()
            if loaded_data: 
                if 'current_level' in loaded_data:
                    self.current_level = loaded_data['current_level']
                if 'healthpoints' in loaded_data:
                    self.settings.current_healthpoints = loaded_data['healthpoints']
                if 'attackpoints' in loaded_data:
                    self.settings.current_attackpoints = loaded_data['attackpoints']
                if 'speed' in loaded_data:
                    self.settings.current_speed = loaded_data['speed']
                if 'skip_cutscenes' in loaded_data:
                    self.skip_cutscenes = loaded_data['skip_cutscenes']
                if 'current_currency' in loaded_data:
                    self.current_currency = loaded_data['current_currency']
        
if __name__ == "__main__":
    game = Game()
    while game.run:
        game.game_loop()
