import pygame

class Sounds():
    def __init__(self):
        # self.game = game
        pygame.mixer.init()
        self.start_game = pygame.mixer.Sound("sounds/start.wav")
        self.upgrade_clicked = pygame.mixer.Sound("sounds/upgrade.wav")
        self.no_upgrade = pygame.mixer.Sound("sounds/no_upgrade.wav")
        self.enemies_death = pygame.mixer.Sound("sounds/enemy_death.wav")
        self.collect_sugarcube = pygame.mixer.Sound("sounds/sugarcubes.wav")
        self.circus_bgmusic = pygame.mixer.Sound("sounds/lounge.wav")
        self.lvl1_bgmusic = pygame.mixer.Sound("sounds/lvl1.wav")
        self.lvl2_bgmusic = pygame.mixer.Sound("sounds/lvl2.wav")
        self.lvl3_bgmusic = pygame.mixer.Sound("sounds/lvl3.wav")
        self.lvl4_bgmusic = pygame.mixer.Sound("sounds/lvl4.wav")
        self.lvl5_bgmusic = pygame.mixer.Sound("sounds/lvl5.wav")
        self.current_bg = None
        

    def is_playing(self, sound):
        return sound.get_busy()
    
    def play_bg(self, selected_bg_music):
        bg_musics = [self.circus_bgmusic, self.lvl1_bgmusic, self.lvl2_bgmusic, self.lvl3_bgmusic, self.lvl4_bgmusic, self.lvl5_bgmusic]
        for bg_music in bg_musics:
            if bg_music == selected_bg_music:
                if self.current_bg == bg_music:
                    pass
                else:
                    if self.current_bg:
                        self.current_bg.stop()
                    bg_music.play(-1)
                    self.current_bg = bg_music
            else:
                bg_music.stop()

    def stop_bg(self):
        if self.current_bg:
            self.current_bg.stop()
            self.current_bg = None