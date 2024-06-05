import pygame
import math

pygame.init()

#define screen size
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

#create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Rotating Objects")

#define colours
BG = (255, 255, 255)
BLACK = (0, 0, 0)

turret_original = pygame.image.load("sprites/heal.png").convert_alpha()
x = 500
y = 300
# x_dist = 0
# y_dist = 0
angle = 0

    #game loop
run = True
while run:

    #update background
    screen.fill(BG)

    #get mouse position
    # pos = pygame.mouse.get_pos()
    # pygame.mouse.get_pos()
    #calculate turret angle
    # x_dist = pos[0] - x
    # y_dist = -(pos[1] - y)#-ve because pygame y coordinates increase down the screen
    angle += 1
    if angle > 360:
        angle = 0
    print(angle)
    #rotate turret
    turret = pygame.transform.rotate(turret_original, angle - 90)
    turret_rect = turret.get_rect(center = (x, y))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        turret_rect.x += 1

    #draw image
    screen.blit(turret, turret_rect)

    #event handler
    for event in pygame.event.get():
        #quit program
        if event.type == pygame.QUIT:
            run = False

    #update display
    pygame.display.flip()



# windowSize = [800, 500]
# screen = pygame.display.set_mode(windowSize)
# white = pygame.color.Color('#FFFFFF')
# angle = 0
# picture = pygame.image.load("turret.png")
# picture_rect = picture.get_rect(center = (300, 300))
# finished = False
# while not finished:
#     screen.fill(white)
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_w]:
#         angle += 1
#     rotated = pygame.transform.rotate(picture, angle)
#     screen.blit(rotated, picture_rect.center)
#     pygame.display.flip()
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             finished = True

pygame.quit()