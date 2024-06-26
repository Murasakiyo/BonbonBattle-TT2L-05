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
        self.sounds = self.game.sounds
        
        self.current_time, self.end_time, self.leech_timer = 0,0,0
        self.enemy_defeat = False
        self.snow_value = 1
        self.enemy3_heal = 0
        self.gacha = 0
        self.accept_ult = False
        self.enemy_group.add(self.enemy3)

        self.allow_effect_for_krie = False
        self.allow_effect_for_stan = False
        self.effect_time = 0
        self.pos = ((550, 300))

        self.end = False
        self.exit_game = False
        self.restart_game = False
        self.click = False
        self.state = "none"

        self.ultimates()
        self.characters(200,200)
        self.load_health_bar()
        self.load_moxie_bar()
        self.enemy_health_update(self.enemy3.rect.x, self.enemy3.rect.y, self.enemy3.HP, self.enemy3.max_HP)
        self.enemy_moxie_update(self.enemy3.moxie, self.enemy3.max_moxie)

        self.sugarcube_received = 0

        self.end_prev = False

    def enter_state(self):
        super().enter_state()
        self.player.attribute_update()
        self.game.play_bg_music(self.game.sounds.lvl4_bgmusic)
        if self.game.current_level == 3:
            self.current_sugarcube_value = self.game.settings.first_sugarcube_value
        else:
            self.current_sugarcube_value = self.game.settings.sugarcube_value



    def update(self, deltatime, player_action):
        
        if player_action["reset_game"]:
            self.game.play_bg_music(self.game.sounds.lvl4_bgmusic)
            if self.game.settings.first_win4:
                self.current_sugarcube_value = self.game.settings.sugarcube_value
            self.sugarcube_list.empty()
            self.snow_value = 1
            self.enemy3.enemy_reset()
            self.player.reset_player(200,200)
            self.ultimate_reset()
            self.enemy_health_update(self.enemy3.rect.x, self.enemy3.rect.y, self.enemy3.HP, self.enemy3.max_HP)
            self.enemy_moxie_update(self.enemy3.moxie, self.enemy3.max_moxie)
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
            self.button_go()

        if self.game.init_reset:
            if player_action["reset_game"] == False:
                self.exit_state(-1)

        self.game_over(player_action)
        self.game_restart(player_action)
        self.ending_options(deltatime, player_action, 5, 4)

        if self.game.start == True:
            if self.game.ult == False:
                # Update player 
                self.player.update(deltatime, player_action)
                self.player_attacking(deltatime, self.enemy_group, self.enemy3)
                self.update_ultimate(deltatime, player_action)
                self.health_update()
                self.moxie_update(player_action)
                self.cooldown_for_attacked(deltatime)
                self.game.frozen()
                
                for enemy in self.enemy_group.sprites():
                    if enemy.HP <= 0:
                        enemy.kill()
                        self.sounds.enemies_death.play()
                        self.enemy3.minionlist.empty()
                        self.spawn_exploding_particles(300, enemy)
                        self.enemy_defeat = True

                if not(self.game.defeat):
                    if not(self.enemy3.HP <= 0):
                        if not(self.game.freeze):
                            self.enemy3.update(deltatime, player_action, self.player.rect.center[0], self.player.rect.center[1], self.player.rect.x)
                            self.snake_attacked(deltatime, player_action, self.enemy_group, self.enemy3, self.enemy3.body_damage)
                            for minions in self.enemy3.minionlist.sprites():
                                self.minion_collisions(deltatime, player_action, self.enemy3.minionlist, self.enemy3.minionlist, minions, minions.damage)
                            
                            if self.enemy3.HP < 300:
                                if self.enemy3.leech == True:
                                    self.old_health = self.player.healthpoints
                                    self.leech_timer += deltatime
                                    if not(self.leech_timer > 0.15):
                                        self.player.healthpoints -= (self.player.healthpoints * 0.05)
                                        self.enemy3_heal = (self.old_health * 0.05)
                                        self.enemy3.HP += self.enemy3_heal
                                else:
                                    self.leech_timer = 0

                        if self.louie.slow_down:
                            self.enemy3.speed = self.enemy3.speed * (50/100)
                            
                        if self.enemy3.HP > 300:
                            self.enemy3.HP = 300
                    

                    self.enemy_health_update(self.enemy3.rect.x, self.enemy3.rect.y, self.enemy3.HP, self.enemy3.max_HP)
                    self.enemy_moxie_update(self.enemy3.moxie, self.enemy3.max_moxie)
                       
                    self.snow_particles(self.snow_value)

                    if self.game.win:
                        self.snow_value = 0
                        self.spawn_particles(200, deltatime)

                    if not(self.end):
                        if player_action["pause"]:
                            new_state = self.pause
                            new_state.enter_state()
                            self.game.start = False 

                    if self.init_stan:
                        if self.stan.attack:
                            if not(self.enemy3.ult):
                                self.enemy3.moxie -= 1
                    else:
                        self.player.attackpoints = self.game.settings.current_attackpoints

            else:
                if self.game.ult:
                    if self.init_stan:
                        if not(self.enemy3.leech):
                            self.enemy3.ult = False
                            self.enemy3.moxie = 0
                    if self.init_louie:
                        if self.enemy3.leech == True:
                            self.enemy3.leech = False
                            self.leech_timer = 0


                self.add_ultimate(deltatime, player_action, self.enemy_group)

            self.particle_group.update(deltatime)
            self.ult_VFX(deltatime)  

        else:
            self.game.start_timer()


    def render(self, display):
        display.blit(pygame.transform.scale(self.game.mountain, (1100,600)), (0,0))
        if self.enemy3.leech == True:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
        self.confection_display(display)
        if self.game.defeat:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
        self.camera.custom_draw(display)
        self.enemy3.render(display)
        if self.game.freeze:
            for enemy in self.enemy_group.sprites():
                display.blit(self.game.ice, (enemy.rect.x + 15, enemy.rect.y + 25))
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
            if self.end_prev == False:
                self.game.stop_bg_music()
                self.end_prev = True
            self.ending_state(display)
            if self.game.win:
                self.game.settings.first_win4 = True
                self.game.current_level = max(self.game.current_level, 4)
        else:
            self.end_prev = False    

       



