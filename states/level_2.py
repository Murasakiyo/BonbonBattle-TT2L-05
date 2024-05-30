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

class Sec_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar, ParticleFunctions):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()
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
        self.victory = False
        self.confetti_time = 0

        self.current_sugarcube_value = 50
        self.sugarcube_list = pygame.sprite.Group()
        self.spawn_sugarcubes(3)


    def spawn_sugarcubes(self, num_sugarcubes):
        for _ in range(num_sugarcubes):
            sugarcube = Sugarcube(self.game, self.current_sugarcube_value)
            self.sugarcube_list.add(sugarcube)

    def reset_sugarcubes(self):
        self.current_sugarcube_value = 10  
        self.sugarcube_list.empty()  
        self.spawn_sugarcubes(3) 


    def update(self, deltatime, player_action):
        
        if player_action["reset_game"]:
            for flies in self.fly_swarm.flylist.sprites():
                flies.kill()
                self.enemy_health_update(flies.rect.x,flies.rect.y, flies.HP)
            self.player.reset_player(200,200)
            self.ultimate_reset()
            self.load_health_bar()
            self.load_moxie_bar()
            self.reset_sugarcubes()
            if self.enemy_defeat:
                self.fly_swarm.flies_spawn()
                self.enemy_defeat = False
            self.swarming = True
            self.game.start = False
            self.current_time = 0
            self.end_time += deltatime
            if self.end_time > 0.5:
                player_action["reset_game"] = False
                self.end_time = 0
                
        if self.game.init_reset:
            if player_action["reset_game"] == False:
                self.exit_state(-1)

        if self.end:
            self.button_go()

        self.game_over(player_action)
        self.game_restart(player_action)
        self.ending_options(deltatime, player_action)

        if self.game.start == True:
            if self.game.ult == False:

                # Update player
                self.player.update(deltatime, player_action)
                self.update_ultimate(deltatime, player_action)
                self.health_update()
                self.moxie_update(player_action)
                self.particle_group.update(deltatime)
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
                            self.spawn_exploding_particles(100, flies)

                        if not self.fly_swarm.flylist.sprites():
                            self.swarming = False 
                            self.enemy_defeat = True

                    if not(self.end):
                        if player_action["pause"]:
                            new_state = self.pause
                            new_state.enter_state()
                            self.game.start = False

                    if self.enemy_defeat:
                        self.confetti_time += deltatime
                        if self.confetti_time > 2:
                            self.victory = True
                    
                    if self.victory == True:
                        self.spawn_particles(200, deltatime)

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

        self.sugarcube_list.update()
        for sugarcube in self.sugarcube_list:
            if sugarcube.rect.colliderect(self.player.rect):
                print("collide")
                sugarcube.collect(self.player)
                print(f"Remaining sugarcubes: {len(self.sugarcube_list)}")
                

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
        self.particle_group.draw(display)
        
        for flies in self.fly_swarm.flylist.sprites():
            if not(flies.HP <= 0):
                self.fly_swarm.render(display)
                self.groupenemy_health_render(display,self.fly_swarm.flylist.sprites())

        self.sugarcube_list.draw(display)

        self.ultimate_display(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, "white", 500,150,200)

        if self.end:
            self.ending_state(display)

