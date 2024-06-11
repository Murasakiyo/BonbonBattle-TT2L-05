import pygame

class Torres_Ult(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.current_frame, self.last_frame_update = 0,0
        self.ult_mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.ult_mask.to_surface()
        self.rect = self.image.get_rect(x = 0, y = 0)
        

    def update(self, deltatime, player_action):
        self.animate(deltatime)
        if self.image == self.current_anim_list[2]:
            self.game.offset = self.game.screen_shake(8,20)
        if self.image == self.current_anim_list[4]:
            self.game.ult_finish = True
            self.game.ult = False
            self.image = self.current_anim_list[0]
            self.current_frame = 0


    def render(self, display):
        display.blit(self.image, (0,0))
        pygame.draw.rect(display, "red", self.rect, 2)



    def animate(self, deltatime):
        self.last_frame_update += deltatime

        if self.last_frame_update > 0.07:
            self.current_frame = (self.current_frame + 1) % len(self.current_anim_list)
            self.image = self.current_anim_list[self.current_frame]
            self.last_frame_update = 0


    def load_sprites(self):
        self.ultimate = []
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/000.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/torres_ult/ult_torres1.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/torres_ult/ult_torres2.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/torres_ult/ult_torres3.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/torres_ult/ult_torres4.png").convert_alpha())
        
        self.image = self.ultimate[0]
        self.current_anim_list = self.ultimate



class Stan_Ult(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.current_frame, self.last_frame_update = 0,0
        self.rect = self.image.get_rect(x = 0, y = 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

    def update(self, deltatime, player_action, enemies):
        self.animate(deltatime)
        if self.image == self.current_anim_list[13]:
            self.ult_collisions(enemies)
            self.game.ult_finish = True
            self.game.ult = False
            self.image = self.current_anim_list[0]
            self.current_frame = 0

    def ult_collisions(self, enemies):
        if pygame.sprite.spritecollide(self, enemies, False): #first check: rectangular collision
                for enemy in enemies:
                    enemy.HP -= 50

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
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/008.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/009.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/010.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/011.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/012.png").convert_alpha())
        self.ultimate.append(pygame.image.load("sprites/ult_anim/stan_ult/000.png").convert_alpha())

        self.image = self.ultimate[0]
        self.current_anim_list = self.ultimate



class Louie_Ult(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.current_frame, self.last_frame_update = 0,0
        self.rect = self.image.get_rect(x = 0, y = 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

    def update(self, deltatime, player_action):
        self.animate(deltatime)
        if self.image == self.current_anim_list[18]:
            self.game.freeze = True
            self.game.ult_finish = True
            self.game.ult = False
            self.image = self.current_anim_list[0]
            self.current_frame = 0
            
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
        self.ultimate.append(pygame.image.load("sprites/ult_anim/louie_ult/014.png").convert_alpha())

        self.image = self.ultimate[0]
        self.current_anim_list = self.ultimate



class Krie_Ult(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.load_sprites()
        self.current_frame, self.last_frame_update = 0,0
        self.rect = self.image.get_rect(x = 0, y = 0)
        self.mask = pygame.mask.from_surface(self.image)
        self.mask_image = self.mask.to_surface()

    def update(self, deltatime, player_action, target):
        self.animate(deltatime)
        if self.image == self.current_anim_list[10]:
            target.healthpoints += 100
            self.game.ult_finish = True
            self.game.ult = False
            self.image = self.current_anim_list[0]
            self.current_frame = 0

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
        