import pygame
from parent_classes.state import *
from states.pause_menu import *
from torres import *
from enemy4 import *
from confection import *
from parent_classes.ultimate_action import *
from parent_classes.health import *
from parent_classes.collisions import *
from parent_classes.moxie import *
from parent_classes.enemyhealthbar import *
from parent_classes.particleeffect import *
from parent_classes.sugarcube import *
from music import Sounds



class Penta_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar, ParticleFunctions, SugarcubeSpawn):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.pause = Pause(self.game)
        self.ultimate = False
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.sugarcube_list = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()
        self.sounds = Sounds(self.game)

        self.ultimates()
        self.characters(450, 200)
        self.enemy4 = Enemy4(self.game, self.player.rect.centerx, self.player.rect.centery)
        self.load_health_bar()
        self.load_moxie_bar()
        self.enemy_health_update(self.enemy4.aira.rect.x, self.enemy4.aira.rect.y, self.enemy4.HP, self.enemy4.max_HP)
        self.enemy_moxie_update(self.enemy4.moxie, self.enemy4.max_moxie)




        self.body_group = pygame.sprite.Group()
        self.attack_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.body_group.add(self.enemy4.aira, self.enemy4.lyra)
        self.attack_group.add(self.enemy4.horiz_string, self.enemy4.vert_string, self.enemy4.twin_ult)
        


        self.deal_damage = True
        self.attack_cooldown = 0
        self.countdown = 0
        self.gacha = 0
        self.accept_ult = False

        self.sugarcube_received = 0
        self.current_time, self.end_time = 0,0
        self.gacha = 0
        self.accept_ult = False
        self.enemy_defeat = False

        self.allow_effect_for_krie = False
        self.allow_effect_for_stan = False
        self.effect_time = 0
        self.pos = ((550, 300))

        # Variables for game reset
        self.end = False
        self.exit_game = False
        self.restart_game = False
        self.click = False
        self.state = "none"
                    
        self.sugarcube_received = 0


    def update(self, deltatime, player_action):

        if player_action["reset_game"]:
            # if self.game.settings.first_win1:
            #     self.current_sugarcube_value = self.game.settings.sugarcube_value
            self.player.reset_player(200,200)
            self.enemy4.enemy_reset()
            self.ultimate_reset()
            self.enemy_health_update(self.enemy4.aira.rect.x, self.enemy4.aira.rect.y, self.enemy4.HP, self.enemy4.max_HP)
            self.enemy_moxie_update(self.enemy4.moxie, self.enemy4.max_moxie)
            self.load_health_bar()
            self.load_moxie_bar()
            if self.enemy_defeat:
                self.body_group.add(self.enemy4.aira, self.enemy4.lyra)
                self.attack_group.add(self.enemy4.horiz_string, self.enemy4.vert_string, self.enemy4.twin_ult)
                self.enemy_defeat = False
            self.sugarcube_list.empty()
            self.game.start = False
            self.current_time = 0
            self.sugarcube_received = 0
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
        # self.ending_options(deltatime, player_action, 4, 3)

        if self.game.start == True:
            if not(self.game.ult):

                # Update player and enemies
                self.player.update(deltatime, player_action)
                self.player_attacking_airalyra(deltatime, self.body_group, self.enemy4, self.enemy4.aira, self.enemy4.lyra)
                self.health_update()
                self.moxie_update(player_action)
                self.cooldown_for_attacked(deltatime)
                self.update_ultimate(deltatime, player_action)
                self.game.frozen()

                # for enemy in self.body_group.sprites():
                if self.enemy4.HP <= 0 and not(self.enemy_defeat):
                    self.sounds.enemies_death.play()
                    self.enemy_defeat = True
                    
                # if self.enemy4.aira.rect.centerx == 550 and self.enemy_defeat:
                #     self.body_group.remove(self.enemy4.lyra)

                if not self.enemy4.aira.rect.centerx <= 540 and not self.enemy4.aira.rect.centerx >= 560 and self.enemy_defeat:
                    self.body_group.remove(self.enemy4.lyra)

                if not(self.game.defeat):
                    if not(self.enemy4.HP <= 0):
                        if not(self.game.freeze):
                            self.enemy4.update(deltatime, player_action, self.player.rect.centerx, self.player.rect.centery)
                            self.AiraLyra_collisions(player_action, self.body_group, self.attack_group, self.enemy4.vert_string, self.enemy4.horiz_string, self.enemy4.string_damage,
                                                    self.enemy4.body_damage, self.enemy4.ult_damage, self.enemy4.twin_ult, self.enemy4, self.enemy4.aira, self.enemy4.lyra)

                    
                        # for enemy in self.body_group.sprites():
                        # if self.enemy4.HP <= 0 and not(self.enemy_defeat):
                        #     self.sounds.enemies_death.play()
                        #     self.body_group.remove(self.enemy4.lyra)
                        #     self.enemy_defeat = True

                    self.enemy_health_update(self.enemy4.aira.rect.x, self.enemy4.aira.rect.y, self.enemy4.HP, self.enemy4.max_HP)
                    self.enemy_moxie_update(self.enemy4.moxie, self.enemy4.max_moxie)
                       
 

                    if self.game.win:
                        self.snow_value = 0
                        self.spawn_particles(200, deltatime)


                if self.enemy4.HP <= 0:
                    self.enemy4.update(deltatime, player_action, self.player.rect.centerx, self.player.rect.centery)


                if not(self.end):
                    if player_action["pause"]:
                        new_state = self.pause
                        new_state.enter_state()
                        self.game.start = False 

                    if self.init_stan:
                        if self.stan.attack:
                            if not(self.enemy4.ult_attack):
                                self.enemy4.moxie -= 1
            else:
                # if self.game.ult:
                #     if self.init_stan:
                #         if not(self.enemy3.leech):
                #             self.enemy3.ult = False
                #             self.enemy3.moxie = 0
                self.add_ultimate(deltatime, player_action, self.enemy_group)

            self.particle_group.update(deltatime)

            # Character Ultimate VFX
            if self.game.ult and self.init_louie:
                self.louie_particles(4)


            if self.game.ult and self.init_krie:
                self.allow_effect_for_krie = True

            if self.allow_effect_for_krie and not self.init_krie:
                self.heal_particles(75)
                self.allow_effect_for_krie = False


            if self.game.ult and self.init_stan:
                self.allow_effect_for_stan = True

            if self.allow_effect_for_stan and not self.init_stan:
                self.effect_time += deltatime
                self.confetti_fireworks(50, self.effect_time)
                if self.effect_time > 0.4:
                    self.effect_time = 0
                    self.allow_effect_for_stan = False  
        else:
            self.game.start_timer()


    def render(self, display):
        display.blit(pygame.transform.scale(self.game.circus_tent, (1100,600)), (0,0))
        self.confection_display(display)
        if self.game.defeat:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
        self.camera.custom_draw(display)

        if not self.enemy4.HP <= 0:
            self.enemy4.render(display)

        if not(self.enemy4.start_ult_atk):
            for enemies in self.body_group:
                if self.body_group.sprites():
                    enemies.render(display)

        display.blit(pygame.transform.scale(self.game.circus_asset, (1200,600)), (0,0))

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
            self.ending_state(display)
            if self.game.win:
                self.game.settings.first_win4 = True
                self.game.current_level = max(self.game.current_level, 5)



