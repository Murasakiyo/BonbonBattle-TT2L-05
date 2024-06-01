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
from currency import Sugarcube
from parent_classes.particleeffect import *
from parent_classes.sugarcube import *


class Sec_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar, ParticleFunctions, SugarcubeSpawn):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()
        self.sugarcube_list = pygame.sprite.Group()
        self.fly_swarm = FlyEnemy(self.game)
        self.pause = Pause(self.game)

        self.ultimates()
        self.characters()
        self.load_health_bar()
        self.load_moxie_bar()

        self.current_time, self.end_time = 0,0
        self.swarming = True
        self.moxie_points = 0
        self.enemy_defeat = False
        
        self.end = False
        self.exit_game = False
        self.restart_game = False
        self.click = False
        self.state = "none"

        if self.game.current_level == 1:
            self.current_sugarcube_value = 50
        else:
            self.current_sugarcube_value = 10
        
        self.sugarcube_received = 0


    def update(self, deltatime, player_action):

        if player_action["reset_game"]:
            self.sugarcube_list.empty()
            for flies in self.fly_swarm.flylist.sprites():
                flies.kill()
                self.enemy_health_update(flies.rect.x,flies.rect.y, flies.HP)
            self.player.reset_player(200,200)
            self.ultimate_reset()
            self.load_health_bar()
            self.load_moxie_bar()
            if self.enemy_defeat:
                self.fly_swarm.flies_spawn()
                self.enemy_defeat = False
            self.swarming = True
            self.game.start = False
            self.sugarcube_received, self.current_time = 0, 0
            self.end_time += deltatime
            if self.end_time > 0.5:
                player_action["reset_game"] = False
                self.end_time = 0
                
        if self.game.init_reset:
            if player_action["reset_game"] == False:
                self.exit_state(-1)

        if self.end:
            # self.game.current_level = 2
            self.button_go()

        self.game_over(player_action)
        self.game_restart(player_action)
        self.ending_options(deltatime, player_action, 3, 2)

        if self.game.start == True:
            if self.game.ult == False:
                # Update player
                self.player.update(deltatime, player_action)
                self.update_ultimate(deltatime, player_action)
                self.cooldown_for_attacked(deltatime)
                self.health_update()
                self.moxie_update(player_action)
                self.particle_group.update(deltatime)

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
                            self.spawn_exploding_particles(100, flies)

                        if not self.fly_swarm.flylist.sprites():
                            self.swarming = False 
                            self.enemy_defeat = True

                    if not(self.end):
                        if player_action["pause"]:
                            new_state = self.pause
                            new_state.enter_state()
                            self.game.start = False

                    if self.game.win:
                        self.spawn_particles(200, deltatime)
                           

            self.add_ultimate(deltatime, player_action)
        else:
            self.game.start_timer()
                

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

        if not self.fly_swarm.flylist.sprites():
            self.sugarcube_list.draw(display)

        self.particle_group.draw(display)
        self.ultimate_display(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, True, "white", 500,150,200)

        if self.end:
            self.game.current_level = max(self.game.current_level, 2)
            self.ending_state(display)

