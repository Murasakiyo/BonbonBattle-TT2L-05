import pygame
import spritesheet


class Aira(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.posx, self.posy = 30, 200
        self.load_sprites()
        self.rect = self.aira.get_rect(width=150, height=200)
        self.rect.x, self.rect.y = self.posx, self.posy
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.current_frame, self.current_frame2, self.last_frame_update, self.last_frame_update2 = 0,0,0,0
        self.transition_time, self.dance_time = 0, 0
        self.fps = 0.3
        self.hand_fps = 0.05
        self.show_attack = False

    def update(self, deltatime, idle, attack, run, spin):
        self.animate(deltatime, idle, attack, run, spin)

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
        if self.show_attack:
            display.blit(self.hand_image, (self.rect.x + 20, self.rect.y - 300))
        # pygame.draw.rect(display, (255,255,255), self.rect, 2)


    def animate(self, deltatime, idle, attack, run, spin):
        self.last_frame_update += deltatime
        if idle:
            self.fps = 0.3
            self.current_anim_list = self.idle_sprites

        if attack:
            self.fps = 0.1
            self.current_anim_list = self.transition_sprites
            self.transition_time += deltatime
            if self.transition_time > 0.6:
                self.current_anim_list = self.attack_up
                self.show_attack = True

        if not(attack):
            self.transition_time = 0
            self.current_frame2 = 0
            self.show_attack = False
            self.last_frame_update2 = 0

        if self.show_attack:
            self.last_frame_update2 += deltatime
            self.current_hand_list = self.hand

        if run == 1 :
            self.fps = 0.05
            self.current_anim_list = self.run_sprites
            self.dance_time += deltatime
            if self.dance_time > 0.6:
                self.fps = 0.1
                self.current_anim_list = self.dance_sprites

        if spin:
            self.fps = 0.1
            self.dance_time = 0
            self.current_anim_list = self.spin_sprites
            
        
         # Updating frames
        if self.last_frame_update > self.fps:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0 

        if self.show_attack:
            if self.last_frame_update2 > self.hand_fps:
                if self.current_frame2 != 3:
                    self.current_frame2 = (self.current_frame2 + 1) % len(self.current_hand_list)
                    self.hand_image = self.current_hand_list[self.current_frame2]
                    self.last_frame_update2 = 0 
                else:
                    self.hand_image = self.current_hand_list[3]
                    self.last_frame_update2 = 0


    def load_sprites(self):
        self.idle_sprites, self.attack_up = [], []
        self.dance_sprites, self.spin_sprites = [], []
        self.run_sprites = []
        self.hand = []
        self.transition_sprites= []
        aira = pygame.image.load("sprites/aira_sp.png").convert()
        self.aira = pygame.transform.scale(aira, (600,1000)).convert_alpha()
        SP = spritesheet.Spritesheet(self.aira)

        # Walking sprites
        for x in range(2):
            self.idle_sprites.append(SP.get_sprite(x, 0, 145, 200, (0,0,0)))
        for x in range(2, 4):
            self.transition_sprites.append(SP.get_sprite(x, 0, 155, 200, (0,0,0)))
        for x in range(4):
            self.attack_up.append(SP.get_sprite(x, 200, 150, 200, (0,0,0)))
        for x in range(3):
            self.dance_sprites.append(SP.get_sprite(x, 600, 145, 200, (0,0,0)))
        for x in range(4):
            self.run_sprites.append(SP.get_sprite(x, 400, 145, 200, (0,0,0)))
        for x in range(3):
            self.spin_sprites.append(SP.get_sprite(x, 800, 150, 200, (0,0,0)))


        self.hand.append(pygame.transform.scale(pygame.image.load("sprites/twins_attack/attack_up/000.png"), (113,400)).convert_alpha())
        self.hand.append(pygame.transform.scale(pygame.image.load("sprites/twins_attack/attack_up/001.png"), (113,400)).convert_alpha())
        self.hand.append(pygame.transform.scale(pygame.image.load("sprites/twins_attack/attack_up/002.png"), (113,400)).convert_alpha())
        self.hand.append(pygame.transform.scale(pygame.image.load("sprites/twins_attack/attack_up/003.png"), (113,400)).convert_alpha())

        self.image = self.idle_sprites[0]
        self.current_anim_list = self.idle_sprites

        self.hand_image = self.hand[0]
        self.current_hand_list = self.hand


class Lyra(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.posx, self.posy = 930, 200
        self.load_sprites()
        self.rect = self.lyra.get_rect(width=150, height=200)
        self.rect.x, self.rect.y = self.posx, self.posy
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.current_frame, self.current_frame2, self.last_frame_update, self.last_frame_update2 = 0,0,0,0
        self.transition_time, self.dance_time = 0, 0
        self.fps = 0.3
        self.hand_fps = 0.05
        self.show_attack = False

    def update(self, deltatime, idle, attack, run, spin):
        self.animate(deltatime, idle, attack, run, spin)

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))
        if self.show_attack:
            display.blit(self.hand_image, (self.rect.x + 15, self.rect.y - 300))
        # pygame.draw.rect(display, (255,255,255), self.rect, 2)


    def animate(self, deltatime, idle, attack, run, spin):
        self.last_frame_update += deltatime

        if idle:
            self.fps = 0.3
            self.current_anim_list = self.idle_sprites

        if attack:
            self.fps = 0.1
            self.current_anim_list = self.transition_sprites
            self.transition_time += deltatime
            if self.transition_time > 0.6:
                self.current_anim_list = self.attack_up
                self.show_attack = True

        if not(attack):
            self.transition_time = 0
            self.current_frame2 = 0
            self.show_attack = False
            self.last_frame_update2 = 0

        if self.show_attack:
            self.last_frame_update2 += deltatime
            self.current_hand_list = self.hand

        if run == 1:
            self.fps = 0.05
            self.current_anim_list = self.run_sprites
            self.dance_time += deltatime
            if self.dance_time > 0.6:
                self.fps = 0.1
                self.current_anim_list = self.dance_sprites

        if spin:
            self.fps = 0.1
            self.dance_time = 0
            self.current_anim_list = self.spin_sprites
        
         # Updating frames
        if self.last_frame_update > self.fps:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0 

        if self.show_attack:
            if self.last_frame_update2 > self.hand_fps:
                if self.current_frame2 != 3:
                    self.current_frame2 = (self.current_frame2 + 1) % len(self.current_hand_list)
                    self.hand_image = self.current_hand_list[self.current_frame2]
                    self.last_frame_update2 = 0 
                else:
                    self.hand_image = self.current_hand_list[3]
                    self.last_frame_update2 = 0


    def load_sprites(self):
        self.idle_sprites, self.attack_up = [], []
        self.dance_sprites, self.spin_sprites = [], []
        self.run_sprites = []
        self.hand = []
        self.transition_sprites = []
        lyra = pygame.image.load("sprites/lyra_sp.png").convert()
        self.lyra = pygame.transform.scale(lyra, (600,1000)).convert_alpha()
        SP = spritesheet.Spritesheet(self.lyra)

        # Walking sprites
        for x in range(2):
            self.idle_sprites.append(SP.get_sprite(x, 0, 150, 200, (0,0,0)))
        for x in range(2, 4):
            self.transition_sprites.append(SP.get_sprite(x, 0, 155, 200, (0,0,0)))
        for x in range(4):
            self.attack_up.append(SP.get_sprite(x, 200, 150, 200, (0,0,0)))
        for x in range(3):
            self.dance_sprites.append(SP.get_sprite(x, 600, 155, 200, (0,0,0)))
        for x in range(4):
            self.run_sprites.append(SP.get_sprite(x, 400, 155, 200, (0,0,0)))
        for x in range(3):
            self.spin_sprites.append(SP.get_sprite(x, 800, 150, 200, (0,0,0)))

        self.image = self.idle_sprites[0]
        self.current_anim_list = self.idle_sprites

        self.hand.append(pygame.transform.scale(pygame.image.load("sprites/twins_attack/attack_up/000.png"), (113,400)).convert_alpha())
        self.hand.append(pygame.transform.scale(pygame.image.load("sprites/twins_attack/attack_up/001.png"), (113,400)).convert_alpha())
        self.hand.append(pygame.transform.scale(pygame.image.load("sprites/twins_attack/attack_up/002.png"), (113,400)).convert_alpha())
        self.hand.append(pygame.transform.scale(pygame.image.load("sprites/twins_attack/attack_up/003.png"), (113,400)).convert_alpha())

        self.image = self.idle_sprites[0]
        self.current_anim_list = self.idle_sprites

        self.hand_image = self.hand[0]
        self.current_hand_list = self.hand


class Twin_ult(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.rect = self.ultimate_sprites[0].get_rect(x=0, y=0)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.current_frame, self.last_frame_update = 0,0
        self.fps = 0.083

    def update(self, deltatime, ult):
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.animate(deltatime)
        
    
    def anim_reset(self, ult):
        if not ult:
            self.current_frame = 0
            self.current_image = self.ultimate_sprites[0]
            self.last_frame_update = 0
            self.fps = 0.083

    
    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def animate(self, deltatime):
        self.last_frame_update += deltatime

        if self.current_frame == 2:
            self.game.offset = self.game.screen_shake(3,8,30)

        if self.current_frame == 9:
            self.game.offset = self.game.screen_shake(3,8,30)

        if self.last_frame_update > self.fps:
            if self.current_frame != 29:
                self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
                self.image = self.current_anim_list[self.current_frame]
                self.last_frame_update = 0
            else:
                self.image = self.current_anim_list[29]
                self.last_frame_update = 0

    def load_sprites(self):
        self.ultimate_sprites = []
        for x in range(10):
            self.ultimate_sprites.append(pygame.image.load(f"sprites/ult_anim/twins_ult/00{x}.png").convert_alpha())
        for x in range(6):
            self.ultimate_sprites.append(pygame.image.load(f"sprites/ult_anim/twins_ult/01{x}.png").convert_alpha())
        for x in range(1,6):
            self.ultimate_sprites.append(pygame.image.load(f"sprites/ult_anim/twins_ult/01{x}.png").convert_alpha())
        for x in range(1,6):
            self.ultimate_sprites.append(pygame.image.load(f"sprites/ult_anim/twins_ult/01{x}.png").convert_alpha())
        self.ultimate_sprites.append(pygame.image.load(f"sprites/ult_anim/twins_ult/011.png").convert_alpha())
        self.ultimate_sprites.append(pygame.image.load(f"sprites/ult_anim/twins_ult/012.png").convert_alpha())
        self.ultimate_sprites.append(pygame.image.load(f"sprites/ult_anim/twins_ult/001.png").convert_alpha())
        self.ultimate_sprites.append(pygame.image.load(f"sprites/ult_anim/twins_ult/000.png").convert_alpha())

        self.image = self.ultimate_sprites[0]
        self.current_anim_list = self.ultimate_sprites

class Horiz_hand(pygame.sprite.Sprite):
    def __init__(self, game, player_y):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.rect = self.atk_sprites[0].get_rect(x = self.game.screen_rect.midleft[0] - 1100 - 25, y = player_y - 25)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.current_frame, self.last_frame_update = 0,0
        self.fps = 0.1

    def update(self):
        pass

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def animate(self, deltatime):
        self.last_frame_update += deltatime

        if self.last_frame_update > self.fps:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0
    

    def load_sprites(self):
        self.atk_sprites = []
        for x in range(3):
            self.atk_sprites.append(pygame.image.load(f"sprites/twins_attack/horizontal_atk/00{x}.png").convert_alpha())

        self.image = self.atk_sprites[0]
        self.current_anim_list = self.atk_sprites
    
class Vert_hand(pygame.sprite.Sprite):
    def __init__(self, game, player_x):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.rect = self.atk_sprites[0].get_rect(x = player_x - 25, y= self.game.screen_rect.midtop[1] - 600)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()
        self.current_frame, self.last_frame_update = 0,0
        self.fps = 0.1

    def update(self):
        pass

    def render(self, display):
        display.blit(self.image, (self.rect.x, self.rect.y))

    def animate(self, deltatime):
        self.last_frame_update += deltatime

        if self.last_frame_update > self.fps:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0
    

    def load_sprites(self):
        self.atk_sprites = []
        for x in range(3):
            self.atk_sprites.append(pygame.image.load(f"sprites/twins_attack/vert_atk/00{x}.png").convert_alpha())

        self.image = self.atk_sprites[0]
        self.current_anim_list = self.atk_sprites


       