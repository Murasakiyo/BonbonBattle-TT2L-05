import pygame
from parent_classes.state import *
from torres import *
from enemy4 import *
from confection import *
from parent_classes.ultimate_action import *
from parent_classes.health import *
from parent_classes.collisions import *
from parent_classes.moxie import *
from parent_classes.enemyhealthbar import *


class Penta_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.ultimate = False

        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.body_group = pygame.sprite.Group()
        self.attack_group = pygame.sprite.Group()

        self.ultimates()
        self.characters()
        self.load_health_bar()
        self.load_moxie_bar()

        self.enemy4 = Enemy5(self.game, self.player.rect.centerx, self.player.rect.centery)





    def update(self, deltatime, player_action):
        # print(int(self.enemy2.flies.rect.x-self.player.rect.x))

        if self.game.start == True:
            if self.game.ult == False:
                

                # Update player and enemies
                self.player.update(deltatime, player_action)


                self.health_update()
                self.moxie_update(player_action)

                self.enemy4.update(deltatime, player_action, self.player.rect.centerx, self.player.rect.centery)
                self.update_ultimate(deltatime, player_action)

            self.add_ultimate(deltatime, player_action)
        else:
            self.game.start_timer()


    def render(self, display):
        display.blit(pygame.transform.scale(self.game.forest, (1100,600)), (0,0))
        self.camera.custom_draw(display)

        display.blit(pygame.transform.scale(self.game.trees, (1200,600)), (-60,0))
        self.player.render(display)
        self.enemy4.render(display)

        self.health_render(display)
        self.moxie_render(display)

        
        self.ultimate_display(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, "white", 500,150,200)
