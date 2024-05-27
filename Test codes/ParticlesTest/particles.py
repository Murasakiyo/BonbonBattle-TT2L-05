import pygame
from random import randint, choice

class Particle(pygame.sprite.Sprite):
    def __init__(self, 
               groups: pygame.sprite.Group, 
               pos: list[int], 
               color: str, 
               direction: pygame.math.Vector2, 
               speed: int,
               display):
        super().__init__(groups)
        self.pos = pos
        self.color = color
        self.direction = direction
        self.speed = speed 
        self.display = display
        self.alpha = 255
        self.fade_speed = 200
        self.size = 4
        self.angle = 0

        self.create_surf()


    def create_surf(self):
        self.surface = pygame.Surface((self.size, self.size)).convert_alpha()
        self.surface.set_alpha(0)
        self.pic1 = pygame.image.load("sprites/red.png").convert_alpha()
        self.pic2 = pygame.image.load("sprites/yellow.png").convert_alpha()
        self.pic3 = pygame.image.load("sprites/pink.png").convert_alpha()
        self.pic4 = pygame.image.load("sprites/blue.png").convert_alpha()
        self.confetti = choice((self.pic1, self.pic2, self.pic3, self.pic4))
        self.image_set = self.confetti
        self.rotate()
        self.image = pygame.transform.scale(self.image_set, (self.size, self.size))
        # self.image = pygame.transform.rotate(self.confetti, self.spin)
        pygame.Surface.blit(self.display, self.image, self.pos)
        self.rect = self.image.get_rect(center = self.pos)

    def rotate(self):
        self.angle += 1
        if self.angle > 360:
            self.angle = 0
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
        self.rotate()
        self.fade(dt)



class ExplodingParticle(Particle):
    def __init__(self, 
               groups: pygame.sprite.Group, 
               pos: list[int], 
               color: str, 
               direction: pygame.math.Vector2, 
               speed: int,
               display):
        self.display = display
        super().__init__(groups, pos, color, direction, speed, display)
        self.t0 = pygame.time.get_ticks()
        self.lifetime = randint(1000, 1200)
        self.exploding = False
        self.size = 4
        self.max_size = 50
        self.inflate_speed = 500
        self.fade_speed = 300

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

        self.explosion_timer()
        if self.exploding:
            self.inflate(dt)
            self.fade(dt)

# class FloatingParticle(Particle):
#     def __init__(self, 
#                groups: pygame.sprite.Group, 
#                pos: list[int], 
#                color: str, 
#                direction: pygame.math.Vector2, 
#                speed: int):
#         super().__init__(groups, pos, color, direction, speed, )