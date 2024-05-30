import pygame
from parent_classes.state import *
from torres import *
from enemy2 import *
from confection import *
from states.pause_menu import *
from parent_classes.ultimate_action import *
from parent_classes.health import *
from parent_classes.collisions import *
from parent_classes.moxie import *
from parent_classes.enemyhealthbar import *
from currency import Sugarcube
from parent_classes.particleeffect import *


class Trio_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar, ParticleFunctions):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.fly_swarm = FlyEnemy(self.game)
        self.pause = Pause(self.game)

        self.enemy1 = FrogEnemy(self.game)
        self.tongue = Tongue(self.game)
        self.tongue2 = Tongue2(self.game)
        self.attack_group = pygame.sprite.Group()
        self.body_group = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()

        self.ultimates()
        self.characters()
        self.load_health_bar()
        self.load_moxie_bar()
        self.enemy_health_update(self.enemy1.rect.x, self.enemy1.rect.y, self.enemy1.HP)

        self.attack_group.add(self.tongue, self.tongue2)
        self.body_group.add(self.enemy1)
        self.moxie_points = 0
        self.confetti_time = 0
        self.victory = False
        self.swarming = True
        self.swamping = False
        self.enemy_defeat = False
        self.enemyflies_defeat = False

        self.current_sugarcube_value = 50
        self.sugarcube_list = pygame.sprite.Group()
        self.spawn_sugarcubes(4)


    def spawn_sugarcubes(self, num_sugarcubes):
        for _ in range(num_sugarcubes):
            sugarcube = Sugarcube(self.game, self.current_sugarcube_value)
            self.sugarcube_list.add(sugarcube)

    def reset_sugarcubes(self):
        self.current_sugarcube_value = 10  
        self.sugarcube_list.empty()  
        self.spawn_sugarcubes(4) 


    def update(self, deltatime, player_action):

        if self.game.reset_game:
            self.swamping = False
            self.swarming = True
            self.enemy1.kill()
            self.tongue.kill()
            self.tongue2.kill()
            self.enemy1.enemy_reset()
            self.player.reset_player(200,200)
            self.ultimate_reset()
            self.enemy_health_update(self.enemy1.rect.x, self.enemy1.rect.y, self.enemy1.HP)
            self.load_health_bar()
            self.load_moxie_bar()
            self.reset_sugarcubes()
            for flies in self.fly_swarm.flylist.sprites():
                flies.kill()
                self.enemy_health_update(flies.rect.x,flies.rect.y, flies.HP)
            if self.enemy_defeat or self.enemyflies_defeat:
                self.attack_group.add(self.tongue, self.tongue2)
                self.body_group.add(self.enemy1)
                self.fly_swarm.flies_spawn()
            self.game.reset_game = False

        self.game_over(deltatime, player_action)

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
                            self.swamping = True
                            self.enemyflies_defeat = True
                            self.camera.add(self.enemy1)

                    if self.swamping:
                        if not(self.enemy1.HP <= 0):
                            self.enemy1.update(deltatime, player_action, self.player.rect.center[0], 
                                            self.player.rect.center[1], self.player.horiz_line, self.player.rect.x) 
                            self.tongue.update(deltatime, player_action, self.enemy1.rect.centerx - 190, self.enemy1.rect.centery - 5, self.enemy1.attack)
                            self.tongue2.update(deltatime, player_action, self.enemy1.rect.centerx -10, self.enemy1.rect.centery - 5, self.enemy1.attack)
                            self.enemy_health_update(self.enemy1.rect.x, self.enemy1.rect.y, self.enemy1.HP)

                        if self.enemy1.HP <= 0:
                            self.enemy1.kill()
                            self.tongue.kill()
                            self.tongue2.kill()
                            self.spawn_exploding_particles(100, self.enemy1)
                            self.swamping = False

                        if not self.body_group.sprites():
                            self.enemy_defeat = True

                        self.enemy_collisions(deltatime, player_action, self.body_group, self.attack_group, self.enemy1, 
                                            self.enemy1.tongue_damage, self.enemy1.body_damage, self.tongue, self.tongue2)
                        
                    if not self.swarming and not self.swamping:
                        self.confetti_time += deltatime
                        if self.confetti_time > 2:
                            self.victory = True
                    
                    if self.victory == True:
                        self.spawn_particles(200, deltatime)
                    
                    if player_action["pause"]:
                        new_state = self.pause
                        new_state.enter_state()
                        self.game.start = False
                
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
        display.blit(pygame.transform.scale(self.game.forest3, (1100,600)), (0,0))
        self.confection_display(display)
        if self.game.defeat:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
        self.camera.custom_draw(display)
        # Player stats
        self.health_render(display)
        self.moxie_render(display)
        self.particle_group.draw(display)

        
        for flies in self.fly_swarm.flylist.sprites():
            if not(flies.HP <= 0):
                self.fly_swarm.render(display)
                self.groupenemy_health_render(display,self.fly_swarm.flylist.sprites())
                
        if self.swamping == True:
            if not(self.enemy1.HP <= 0):
                if self.enemy1.current_anim_list == self.enemy1.attack_left:
                    self.tongue.render(display)
                elif self.enemy1.current_anim_list == self.enemy1.attack_right:
                    self.tongue2.render(display)
            if not(self.enemy1.HP <= 0):
                self.enemy_health_render(display, self.enemy1.rect.x, self.enemy1.rect.y)

        self.ultimate_display(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, "white", 500,150,200)

        self.sugarcube_list.draw(display)