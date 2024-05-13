import pygame
from parent_classes.state import *
from states.pause_menu import *
from torres import *
from enemy2 import *
from confection import *
from parent_classes.ultimate_action import *
from parent_classes.health import *
from parent_classes.collisions import *
from parent_classes.moxie import *
from parent_classes.enemyhealthbar import *


class Sec_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.fly_swarm = FlyEnemy(self.game)
        self.pause = Pause(self.game)

        self.swarming = True
        self.ultimates()
        self.characters()
        self.load_health_bar()
        self.load_moxie_bar()
        self.moxie_points = 0
        self.enemy_defeat = False

    def update(self, deltatime, player_action):
        
        if self.game.reset_game:
            for flies in self.fly_swarm.flylist.sprites():
                flies.kill()
                self.enemy_health_update(flies.rect.x,flies.rect.y, flies.HP)
            self.player.reset_player(200,200)
            self.ultimate_reset()
            self.load_health_bar()
            self.load_moxie_bar()
            if self.enemy_defeat:
                self.fly_swarm.flies_spawn()
            self.swarming = True
            self.game.reset_game = False

        self.game_over(deltatime, player_action)

        if self.game.start == True:
            if self.game.ult == False:

                # Update player
                self.player.update(deltatime, player_action)
                self.update_ultimate(deltatime, player_action)
                self.health_update()
                self.moxie_update(player_action)
                self.cooldown_for_attacked(deltatime)

                if not(self.game.defeat):
                # Check if flies are all still alive
                    if self.swarming:
                        self.fly_swarm.update(deltatime, player_action, self.player.rect.center[0], 
                                            self.player.rect.center[1], self.player.rect, self.player.rect.x)
                    
                    for flies in self.fly_swarm.flylist.sprites():
                        if not(flies.HP <= 0):
                            self.flies_collisions(deltatime, player_action, self.fly_swarm.flylist, self.fly_swarm.flylist, flies, 
                                                flies.damage)
                        if flies.HP <= 0:
                            flies.kill()
                        if not self.fly_swarm.flylist.sprites():
                            self.swarming = False 
                            self.enemy_defeat = True

                    if player_action["pause"]:
                        new_state = self.pause
                        new_state.enter_state()
                        self.game.start = False
                        # self.game.reset_keys()
                           
                if self.player.healthpoints <= 0:
                    self.game.defeat = True
                    player_action["ultimate"] = False


            self.add_ultimate(deltatime, player_action)
        else:
            self.game.start_timer()
        # print(self.attack_time)

    def render(self, display):
        display.blit(pygame.transform.scale(self.game.forest2, (1100,600)), (0,0))
        self.confection_display(display)
        if self.game.defeat:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
        self.camera.custom_draw(display)
        display.blit(pygame.transform.scale(self.game.trees, (1200,600)), (-60,0))
        
        # Player stats
        self.health_render(display)
        self.moxie_render(display)
        
        for flies in self.fly_swarm.flylist.sprites():
            if not(flies.HP <= 0):
                self.fly_swarm.render(display)
                self.groupenemy_health_render(display,self.fly_swarm.flylist.sprites())

        self.ultimate_display(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, "white", 500,150,200)
