import pygame
from parent_classes.state import *
from states.pause_menu import *
from torres import *
from enemy3 import *
from confection import *
from parent_classes.ultimate_action import *
from parent_classes.health import *
from parent_classes.collisions import *
from parent_classes.moxie import *
from parent_classes.enemyhealthbar import *
from currency import Sugarcube
from parent_classes.particleeffect import *



class Quad_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar, ParticleFunctions):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.pause = Pause(self.game)
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.enemy3 = Enemy3(self.game, self.camera)
        self.enemy_group = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()
        
        self.current_time, self.end_time = 0,0
        self.confetti = False
        self.victory = False
        self.enemy_defeat = False
        self.cause_effect = True
        self.confetti_time = 0
        self.snow_value = 2

        self.enemy3_heal = 0

        self.end = False
        self.exit_game = False
        self.restart_game = False
        self.click = False
        self.state = "none"


        self.ultimates()
        self.characters()
        self.load_health_bar()
        self.load_moxie_bar()
        self.enemy_group.add(self.enemy3)
        self.enemy_health_update(self.enemy3.rect.x, self.enemy3.rect.y, self.enemy3.HP)


        self.current_sugarcube_value = 50
        self.sugarcube_list = pygame.sprite.Group()
        self.spawn_sugarcubes(5)


    def spawn_sugarcubes(self, num_sugarcubes):
        for _ in range(num_sugarcubes):
            sugarcube = Sugarcube(self.game, self.current_sugarcube_value)
            self.sugarcube_list.add(sugarcube)

    def reset_sugarcubes(self):
        self.current_sugarcube_value = 10  
        self.sugarcube_list.empty()  
        self.spawn_sugarcubes(5) 


    def update(self, deltatime, player_action):
        
        if player_action["reset_game"]:
            self.enemy3.enemy_reset()
            self.player.reset_player(200,200)
            self.ultimate_reset()
            self.enemy_health_update(self.enemy3.rect.x, self.enemy3.rect.y, self.enemy3.HP)
            self.load_health_bar()
            self.load_moxie_bar()
            self.reset_sugarcubes()
            self.end_time += deltatime
            if self.end_time > 0.5:
                self.swarming = True
                player_action["reset_game"] = False
                self.end_time = 0

        if self.end:
            self.button_go()

        if self.game.init_reset:
            if player_action["reset_game"] == False:
                self.exit_state(-1)

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
                self.cooldown_for_attacked(deltatime)
                

                if not(self.game.defeat) and not(self.enemy3.HP <= 0):
                    self.enemy3.update(deltatime, player_action, self.player.rect.center[0], self.player.rect.center[1], self.player.rect.x)
                    self.snake_attacked(deltatime, player_action, self.enemy_group, self.enemy3, self.enemy3.body_damage)
                    self.enemy_health_update(self.enemy3.rect.x, self.enemy3.rect.y, self.enemy3.HP)

                    # self.snow_particles(2)
                    
                    if self.enemy3.HP < 300:
                        if self.enemy3.leech == True:
                            self.old_health = self.player.healthpoints
                            self.player.healthpoints -= (self.player.healthpoints * 20/100)
                            self.enemy3_heal = (self.old_health * 20/100)
                            self.enemy3.HP += self.enemy3_heal

                    if self.enemy3.HP > 300:
                        self.enemy3.HP = 300
                
                if not(self.game.defeat):
                    for minions in self.enemy3.minionlist.sprites():
                        self.minion_collisions(deltatime, player_action, self.enemy3.minionlist, self.enemy3.minionlist, minions, minions.damage)

                self.particle_group.update(deltatime)

                if self.enemy3.HP <= 0:
                    self.enemy3.kill()
                    self.enemy3.minionlist.remove(self.enemy3.minions)
                    self.enemy_defeat = True
                    self.confetti = True

                if self.cause_effect and self.enemy_defeat:
                    self.spawn_exploding_particles(300, self.enemy3)
                    self.cause_effect = False

                self.snow_particles(self.snow_value)

                if self.confetti:
                    self.snow_value = 0
                    self.confetti_time += deltatime
                    if self.confetti_time > 2:
                        self.victory = True

                if self.victory == True:
                    self.spawn_particles(200, deltatime)

                if not(self.end):
                    if player_action["pause"]:
                        new_state = self.pause
                        new_state.enter_state()
                        self.game.start = False 

            self.add_ultimate(deltatime, player_action)
        else:
            self.game.start_timer()

        self.sugarcube_list.update()
        for sugarcube in self.sugarcube_list:
            if sugarcube.rect.colliderect(self.player.rect):
                print("collide")
                sugarcube.collect(self.player)
                print(f"Remaining sugarcubes: {len(self.sugarcube_list)}")


    def render(self, display):
        display.blit(pygame.transform.scale(self.game.mountain, (1100,600)), (0,0))
        self.confection_display(display)
        if self.game.defeat:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
        self.camera.custom_draw(display)
        self.enemy3.render(display)
        display.blit(pygame.transform.scale(self.game.mount_asset, (1200,600)), (-60,0))

        self.health_render(display)
        self.moxie_render(display)
        self.boss_health_render(display)
        self.particle_group.draw(display)
        
        self.ultimate_display(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, "white", 500,150,200)

        self.sugarcube_list.draw(display)

        if self.end:
            self.ending_state(display)



