import pygame
from SaveLoadManager import SaveLoadSystem

pygame.init()

display = pygame.display.set_mode((600,600))
clock = pygame.time.Clock()

# entities = []

saveloadmanager = SaveLoadSystem(".save", "save_data")

entities = saveloadmanager.load_data("entities")

# entities, number = saveloadmanager.load_game_data(["entities", "number"], [[], 1])

while True:
    display.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
            saveloadmanager.save_data(entities, "entities")
            # saveloadmanager.save_game_data([entities, number], ["entities", "number"])
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                entities.append(mouse_pos)

            if event.button == 3:
                number = 3


    for entity in entities:
        pygame.draw.circle(display, (255,0,0), (entity[0], entity[1]), 10)


    pygame.display.update()
    clock.tick(60)
