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
from parent_classes.sugarcube import *



class Quad_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar, ParticleFunctions, SugarcubeSpawn):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.pause = Pause(self.game)
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.sugarcube_list = pygame.sprite.Group()
        self.enemy3 = Enemy3(self.game, self.camera)
        self.enemy_group = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()
        
        self.current_time, self.end_time = 0,0
        self.enemy_defeat = False
        self.snow_value = 1
        self.enemy3_heal = 0
        self.enemy_group.add(self.enemy3)

        self.end = False
        self.exit_game = False
        self.restart_game = False
        self.click = False
        self.state = "none"

        self.ultimates()
        self.characters()
        self.load_health_bar()
        self.load_moxie_bar()
        self.enemy_health_update(self.enemy3.rect.x, self.enemy3.rect.y, self.enemy3.HP)

        if self.game.current_level == 3:
            self.current_sugarcube_value = self.game.settings.first_sugarcube_value
        else:
            self.current_sugarcube_value = self.game.settings.sugarcube_value
            
        self.sugarcube_received = 0



    def update(self, deltatime, player_action):
        
        if player_action["reset_game"]:
            if not self.game.settings.first_win1:
                self.game.settings.first_win1 = True
                self.game.settings.reset_sugarcube_value()
                self.current_sugarcube_value = self.game.settings.sugarcube_value
            self.sugarcube_list.empty()
            self.snow_value = 1
            self.enemy3.enemy_reset()
            self.player.reset_player(200,200)
            self.ultimate_reset()
            self.enemy_health_update(self.enemy3.rect.x, self.enemy3.rect.y, self.enemy3.HP)
            self.load_health_bar()
            self.load_moxie_bar()
            if self.enemy_defeat:
                self.enemy3.add(self.enemy_group, self.camera)
                self.enemy_defeat = False
            self.game.start = False
            self.sugarcube_received, self.current_time = 0, 0
            self.end_time += deltatime
            if self.end_time > 0.5:
                player_action["reset_game"] = False
                self.end_time = 0

        if self.end:
            # self.game.current_level = 4
            self.button_go()

        if self.game.init_reset:
            if player_action["reset_game"] == False:
                self.exit_state(-1)

        self.game_over(player_action)
        self.game_restart(player_action)
        self.ending_options(deltatime, player_action, 4, 3)

        if self.game.start == True:
            if self.game.ult == False:

                # Update player 
                self.player.update(deltatime, player_action)
                self.update_ultimate(deltatime, player_action)
                self.health_update()
                self.moxie_update(player_action)
                self.cooldown_for_attacked(deltatime)
                

                if not(self.game.defeat):
                    if not(self.enemy3.HP <= 0):
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
                
               
                        for minions in self.enemy3.minionlist.sprites():
                            self.minion_collisions(deltatime, player_action, self.enemy3.minionlist, self.enemy3.minionlist, minions, minions.damage)

                    
                        for enemy in self.enemy_group.sprites():
                            if enemy.HP <= 0:
                                enemy.kill()
                                self.enemy3.minionlist.empty()
                                self.spawn_exploding_particles(300, enemy)
                                self.enemy_defeat = True

                   

                    self.snow_particles(self.snow_value)

                    if self.game.win:
                        self.snow_value = 0
                        self.spawn_particles(200, deltatime)

                    if not(self.end):
                        if player_action["pause"]:
                            new_state = self.pause
                            new_state.enter_state()
                            self.game.start = False 

            self.particle_group.update(deltatime)
            if self.game.ult and self.init_louie:
                self.louie_particles(4)

            self.add_ultimate(deltatime, player_action)
        else:
            self.game.start_timer()


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
        if self.game.start:
            self.boss_health_render(display)
            self.sugarcube_list.draw(display)

        if self.game.ult:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
        self.particle_group.draw(display)
        self.ultimate_display(display)
    
        if self.game.start == False:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
            if self.game.alpha == 0:
                self.game.draw_text(display, self.game.ct_display, True, "white", 500,150,200)


        if self.end:
            self.game.current_level = max(self.game.current_level, 4)
            self.ending_state(display)



