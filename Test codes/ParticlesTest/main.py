import pygame
from random import choice, randint, uniform
from particles import *

SCREENWIDTH, SCREENHEIGHT = 1100, 600

display_surface = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
clock = pygame.time.Clock()

particle_group = pygame.sprite.Group()
effect_time = 0

floating_particle_timer = pygame.event.custom_type()
pygame.time.set_timer(floating_particle_timer, 10)

def spawn_particles(n: int):
    for _ in range(n):
        pos = pygame.mouse.get_pos()
        color = choice(("red", "green", "blue"))
        direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
        direction = direction.normalize()
        speed = randint(50, 200)
        Particle(particle_group, pos, color, direction, speed, display_surface, False, False)

def spawn_exploding_particles(n: int):
    for _ in range(n):
        pos = pygame.mouse.get_pos()
        color = choice(("red", "yellow", "orange"))
        direction = pygame.math.Vector2(uniform(-0.2, 0.2), uniform(-1, 0))
        direction = direction.normalize()
        speed = randint(50, 400)
        ExplodingParticle(particle_group, pos, color, direction, speed, display_surface)

def heal_particles(n: int):
    for _ in range(n):
        pos = ((randint(0, 1100)), (randint(0, 600)))
        color = "white"
        direction = pygame.math.Vector2(0, -1)
        direction = direction.normalize()
        speed = randint(50, 400)
        Particle(particle_group, pos, color, direction, speed, display_surface, True, False)

def confetti_fireworks(n: int):
    for _ in range(n):
        spot1 = ((200, 100))
        spot2 = ((200, 500))
        spot3 = ((900, 100))
        spot4 = ((900, 500))
        pos = choice((spot1, spot2, spot3, spot4))
        color = choice(("red", "green", "blue"))
        direction = pygame.math.Vector2(uniform(-1, 1), uniform(-1, 1))
        direction = direction.normalize()
        speed = randint(50, 200)
        Particle(particle_group, pos, color, direction, speed, display_surface, False, True)





# def spawn_floating_particles():
#     init_pos = pygame.mouse.get_pos()
#     pos = init_pos[0] + randint(-10, 10), init_pos[1] + randint(-10, 10)
#     color = "white"
#     direction = pygame.math.Vector2(0, -1)
#     direction = direction.normalize()
#     speed = randint(50, 100)
#     FloatingParticle(particle_group, pos, color, direction, speed)



def main_loop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    confetti_fireworks(50)
                elif pygame.mouse.get_pressed()[2]:
                    heal_particles(75)
                
            # if event.type == floating_particle_timer:
            #     spawn_floating_particles()


        dt = clock.tick() / 1000

        display_surface.fill("white")
        particle_group.draw(display_surface)

        # Update
        particle_group.update(dt)
        pygame.display.update()

        # print(len(particle_group.sprites()))
        # print(pygame.mouse.get_pos())

if __name__ == "__main__":
    pygame.init()
    main_loop()