import pygame

class Ultimate(pygame.sprite.Group):
    def __init__(self, game):
        super.__init__(self, game)
        self.game = game
        self.torres_ult = Torres_Ult(game)
        self.stan_ult = Stan_Ult(game)
        self.louie_ult = Louie_Ult(game)
        self.krie_ult = Krie_Ult(game)
        self.newctime = pygame.time.get_ticks()
        self.countdown = 0
        self.immunity = False
        


    def update(self, deltatime, player_action):
        self.torres.update(deltatime, player_action)


    def render(self, display):
        display.blit(pygame.transform.scale(self.background, (1100,600)), (0,0))
        self.torres.render(display)



class Torres_Ult(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.load_sprites()
        self.current_frame, self.last_frame_update = 0,0

    def update(self, deltatime, player_action):
        self.animate(deltatime)


    def render(self, display):
        display.blit(self.image, (0,0))


    def animate(self, deltatime):
        self.last_frame_update += deltatime

        if self.last_frame_update > 0.05:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0


    def load_sprites(self):
        self.ultimate = []
        self.ultimate.append(pygame.image.load("sprites/ult_anim/torres_ult/ult_torres1.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/torres_ult/ult_torres2.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/torres_ult/ult_torres3.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/torres_ult/ult_torres4.png").convert_alpha())
        
        self.image = self.ultimate[0]
        self.current_anim_list = self.ultimate



class Stan_Ult(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.load_sprites()
        self.current_frame, self.last_frame_update = 0,0

    def update(self, deltatime, player_action):
        self.animate(deltatime)


    def render(self, display):
        display.blit(self.image, (0,0))


    def animate(self, deltatime):
        self.last_frame_update += deltatime

        if self.last_frame_update > 0.1:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0


    def load_sprites(self):
        self.ultimate = []
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/000.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/001.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/002.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/003.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/004.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/005.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/006.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/007.png").convert_alpha())

        
        self.image = self.ultimate[0]
        self.current_anim_list = self.ultimate



class Louie_Ult(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.load_sprites()
        self.current_frame, self.last_frame_update = 0,0

    def update(self, deltatime, player_action):
        self.animate(deltatime)


    def render(self, display):
        display.blit(self.image, (0,0))


    def animate(self, deltatime):
        self.last_frame_update += deltatime

        if self.last_frame_update > 0.1:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0


    def load_sprites(self):
        self.ultimate = []
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/000.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/001.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/002.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/003.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/004.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/005.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/006.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/007.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/008.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/009.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/010.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/011.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/012.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/009.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/010.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/011.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/012.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/013.png").convert_alpha())

        self.image = self.ultimate[0]
        self.current_anim_list = self.ultimate


class Krie_Ult(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        self.load_sprites()
        self.current_frame, self.last_frame_update = 0,0

    def update(self, deltatime, player_action):
        self.animate(deltatime)


    def render(self, display):
        display.blit(self.image, (0,0))


    def animate(self, deltatime):
        self.last_frame_update += deltatime

        if self.last_frame_update > 0.1:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0


    def load_sprites(self):
        self.ultimate = []
        self.ultimate.append(pygame.image.load("sprites/ult_anim/krie_ult/000.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/krie_ult/001.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/krie_ult/002.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/krie_ult/003.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/krie_ult/004.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/krie_ult/005.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/krie_ult/006.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/krie_ult/007.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/krie_ult/008.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/krie_ult/009.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/krie_ult/010.png").convert_alpha())
        
        self.image = self.ultimate[0]
        self.current_anim_list = self.ultimate