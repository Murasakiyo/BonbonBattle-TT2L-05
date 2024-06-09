import pygame
from random import randint, choice, uniform

class Snow(pygame.sprite.Sprite):
    def __init__(self, 
               groups: pygame.sprite.Group, 
               pos: list[int], 
               color: str, 
               direction: pygame.math.Vector2, 
               speed: int):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed 
        self.alpha = 255
        self.fade_speed = 200
        self.size = 4

        self.create_surf()


    def create_surf(self):
        self.image = pygame.Surface((self.size, self.size)).convert_alpha()
        self.image.set_colorkey("black")
        pygame.draw.circle(surface = self.image, color = self.color, center = (self.size/2, self.size/2), radius = self.size/2)
        self.rect = self.image.get_rect(center = self.pos)

    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)

    def check_pos(self):
        if (self.pos[0] < -50 or 
            self.pos[0] > 1100 + 50 or 
            self.pos[1] < -50 or
            self.pos[1] > 600 + 50):

            self.kill()

    def check_alpha(self):
        if self.alpha <= 0:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.check_pos()

class Particle(pygame.sprite.Sprite):
    def __init__(self, 
               groups: pygame.sprite.Group, 
               pos: list[int], 
               color: str, 
               direction: pygame.math.Vector2, 
               speed: int,
               game,
               heal_bool,
               for_stan_bool):
        super().__init__(groups)
        self.game = game
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed 
        self.alpha = 255
        self.fade_speed = 200
        self.size = 8
        self.stan_confetti_size = 12
        self.heal_size = randint(16, 32)
        self.angle = 0
        self.heal_bool = heal_bool
        self.for_stan = for_stan_bool

        self.create_surf(self.heal_bool, self.for_stan)


    def create_surf(self, heal_bool, for_stan):
        self.surface = pygame.Surface((self.size, self.size)).convert_alpha()
        self.surface.set_alpha(0)
        if not heal_bool and not for_stan:
            self.pic1 = pygame.image.load("sprites/particles/red.png").convert_alpha()
            self.pic2 = pygame.image.load("sprites/particles/yellow.png").convert_alpha()
            self.pic3 = pygame.image.load("sprites/particles/pink.png").convert_alpha()
            self.pic4 = pygame.image.load("sprites/particles/blue.png").convert_alpha()
            self.confetti = choice((self.pic1, self.pic2, self.pic3, self.pic4))
            self.image_set = self.confetti
            self.image = pygame.transform.scale(self.image_set, (self.size, self.size))
        if not heal_bool and for_stan:
            self.pic1 = pygame.image.load("sprites/particles/red.png").convert_alpha()
            self.pic2 = pygame.image.load("sprites/particles/yellow.png").convert_alpha()
            self.pic3 = pygame.image.load("sprites/particles/pink.png").convert_alpha()
            self.pic4 = pygame.image.load("sprites/particles/blue.png").convert_alpha()
            self.confetti = choice((self.pic1, self.pic2, self.pic3, self.pic4))
            self.image_set = self.confetti
            self.image = pygame.transform.scale(self.image_set, (self.stan_confetti_size, self.stan_confetti_size))
        if heal_bool:
            self.HealPic = pygame.image.load("sprites/particles/heal.png").convert_alpha()
            self.image = pygame.transform.scale(self.HealPic, (self.heal_size, self.heal_size))

        pygame.Surface.blit(self.game.screen, self.image, self.pos)
        self.rect = self.image.get_rect(center = self.pos)

    def rotate(self):
        self.angle += 1
        if self.angle > 360:
            self.angle = 0
        self.image = pygame.transform.rotate(self.image_set, self.angle - 90)

    def rotate2(self):
        self.angle += 1
        if self.angle > 360:
            self.angle = 0
        self.image_set = pygame.transform.scale(self.image_set, (self.stan_confetti_size, self.stan_confetti_size))
        self.image = pygame.transform.rotate(self.image_set, self.angle - 90)


    def move(self, dt):
        self.pos += self.direction * self.speed * dt
        self.rect.center = self.pos

    def fade(self, dt):
        self.alpha -= self.fade_speed * dt
        self.image.set_alpha(self.alpha)

    def check_pos(self):
        if (self.pos[0] < -50 or 
            self.pos[0] > 1100 + 50 or 
            self.pos[1] < -50 or
            self.pos[1] > 600 + 50):

            self.kill()

    def check_alpha(self):
        if self.alpha <= 0:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.check_pos()
        self.check_alpha()
        if not self.heal_bool and not self.for_stan:
            self.rotate()
        if self.for_stan:
            self.rotate2()
        self.fade(dt)





class ExplodingParticle(Particle):
    def __init__(self, 
               groups: pygame.sprite.Group, 
               pos: list[int], 
               color: str, 
               direction: pygame.math.Vector2, 
               speed: int,
               game):
        self.game = game
        super().__init__(groups, pos, color, direction, speed, self.game, False, False)
        self.t0 = pygame.time.get_ticks()
        self.lifetime = randint(1000, 1200)
        self.exploding = False
        self.size = 4
        self.max_size = 50
        self.inflate_speed = 500
        self.fade_speed = 100

    def explosion_timer(self):
        t = pygame.time.get_ticks()
        if t - self.t0 > self.lifetime:
            self.exploding = True

    def inflate(self, dt):
        self.size += self.inflate_speed * dt
        self.create_surf()

    def check_size(self):
        if self.size > self.max_size:
            self.kill()

    def update(self, dt):
        self.move(dt)
        self.check_pos()
        self.check_size()
        self.check_alpha()
        self.rotate()
        self.fade(dt)
        # self.explosion_timer()
        # if self.exploding:
        #     self.inflate(dt)

class ParticleFunctions():
    def __init__(self, game):
        self.game = game
        self.particle_group = pygame.sprite.Group


    def spawn_particles(self, n: int, deltatime):
            self.pos = ((randint(0, 1100)), 0)
            color = choice(("purple", "blue", "green", "red", "yellow"))
            direction = pygame.math.Vector2(0,1)
            direction = direction.normalize()
            speed = randint(50, 400)
            Particle(self.particle_group, self.pos, color, direction, speed, self.game, False, False)

    def spawn_exploding_particles(self, n: int, enemy):
        for _ in range(n):
            pos = (enemy.rect.center[0], enemy.rect.center[1] + 82.5)
            color = choice(("purple", "blue", "green", "red", "yellow"))
            direction = pygame.math.Vector2(uniform(-0.2, 0.2), uniform(-1, 0))
            direction = direction.normalize()
            speed = randint(75, 600)
            ExplodingParticle(self.particle_group, pos, color, direction, speed, self.game)
            
    def snow_particles(self, n: int):
        for _ in range(n):
            pos = ((randint(0, 1100)), 0)
            color = "white"
            direction = pygame.math.Vector2(0, 1)
            direction = direction.normalize()
            speed = randint(25, 200)
            Snow(self.particle_group, pos, color, direction, speed)

    def louie_particles(self, n: int):
        for _ in range(n):
            pos = (1100, (randint(0, 600)))
            color = "white"
            direction = pygame.math.Vector2(-1, 0)
            direction = direction.normalize()
            speed = randint(100, 800)
            Snow(self.particle_group, pos, color, direction, speed)

    def heal_particles(self, n: int):
        for _ in range(n):
            pos = ((randint(0, 1100)), (randint(0, 600)))
            color = "white"
            direction = pygame.math.Vector2(0, -1)
            direction = direction.normalize()
            speed = randint(50, 400)
            Particle(self.particle_group, pos, color, direction, speed, self.game, True, False)


    def confetti_fireworks(self, n: int, effect_time):
        for _ in range(n):
            spot1 = ((200, 100))
            spot2 = ((200, 500))
            spot3 = ((900, 100))
            spot4 = ((900, 500))
            if effect_time > 0.1:
                self.pos = spot1
            if effect_time > 0.2:
                self.pos = spot2
            if effect_time > 0.3:
                self.pos = spot3
            if effect_time > 0.4:
                self.pos = spot4
            # pos = choice((spot1, spot2, spot3, spot4, spot5, spot6))
            color = choice(("red", "green", "blue"))
            direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
            direction = direction.normalize()
            speed = randint(100, 800)
            Particle(self.particle_group, self.pos, color, direction, speed, self.game, False, True)