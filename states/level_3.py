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
from parent_classes.particleeffect import *
from parent_classes.sugarcube import *


class Trio_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar, ParticleFunctions, SugarcubeSpawn):
    def __init__(self, game):
        super().__init__(game)
        self.camera = CameraGroup(self.game)
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.sugarcube_list = pygame.sprite.Group()
        self.fly_swarm = FlyEnemy(self.game)
        self.pause = Pause(self.game)
        self.sounds = self.game.sounds

        self.enemy1 = FrogEnemy(self.game)
        self.tongue = Tongue(self.game)
        self.tongue2 = Tongue2(self.game)
        self.attack_group = pygame.sprite.Group()
        self.body_group = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()

        self.ultimates()
        self.characters(200,200)
        self.load_health_bar()
        self.load_moxie_bar()
        self.enemy_health_update(self.enemy1.rect.x, self.enemy1.rect.y, self.enemy1.HP, self.enemy1.max_HP)

        self.attack_group.add(self.tongue, self.tongue2)
        self.body_group.add(self.enemy1)
        self.gacha = 0
        self.accept_ult = False

        self.current_time, self.end_time = 0,0
        self.swarming = True
        self.swamping = False
        self.enemy_defeat = False
        self.enemyfrog_defeat = False
        self.enemyflies_defeat = False
        self.current_enemy = self.fly_swarm.flylist

        self.allow_effect_for_krie = False
        self.allow_effect_for_stan = False
        self.effect_time = 0
        self.pos = ((550, 300))

        self.end = False
        self.exit_game = False
        self.restart_game = False
        self.click = False
        self.state = "none"
            
        self.sugarcube_received = 0

        self.end_prev = False

    def enter_state(self):
        super().enter_state()
        self.player.attribute_update()
        self.game.play_bg_music(self.game.sounds.lvl3_bgmusic)
        if self.game.current_level == 2:
            self.current_sugarcube_value = self.game.settings.first_sugarcube_value
        else:
            self.current_sugarcube_value = self.game.settings.sugarcube_value



    def update(self, deltatime, player_action):

        if player_action["reset_game"]:
            self.game.play_bg_music(self.game.sounds.lvl3_bgmusic)
            if self.game.settings.first_win3:
                self.current_sugarcube_value = self.game.settings.sugarcube_value
            self.sugarcube_list.empty()
            self.current_enemy = self.fly_swarm.flylist
            self.camera.remove(self.enemy1, self.tongue, self.tongue2)
            self.enemy1.enemy_reset()
            self.player.reset_player(200,200)
            self.ultimate_reset()
            self.enemy_health_update(self.enemy1.rect.x, self.enemy1.rect.y, self.enemy1.HP, self.enemy1.max_HP)
            self.load_health_bar()
            self.load_moxie_bar()
            for flies in self.fly_swarm.flylist.sprites():
                flies.kill()
                self.enemy_health_update(flies.rect.x,flies.rect.y, flies.HP, flies.max_HP)
            if self.enemy_defeat:
                self.attack_group.add(self.tongue, self.tongue2)
                self.body_group.add(self.enemy1)
                self.enemyfrog_defeat = False
                self.enemy_defeat = False
            self.swamping = False
            self.game.start = False
            self.sugarcube_received, self.current_time = 0, 0
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
        self.ending_options(deltatime, player_action, 4, 3)

        if self.game.start == True:
            if self.game.ult == False:
                # Update player
                self.player.update(deltatime, player_action)
                self.update_ultimate(deltatime, player_action)
                for flies in self.fly_swarm.flylist.sprites():
                    self.player_attacking(deltatime, self.fly_swarm.flylist, flies)
                if self.swamping:
                    self.player_attacking(deltatime, self.body_group, self.enemy1)
                self.health_update()
                self.moxie_update(player_action)
                self.cooldown_for_attacked(deltatime)
                self.game.frozen()


                if not(self.game.defeat):
                    # Check if flies are all still alive
                    if self.swarming:
                        if not(self.game.freeze):
                            self.fly_swarm.update(deltatime, player_action, self.player.rect.center[0], 
                                                self.player.rect.center[1], self.player.rect, self.player.rect.x, self.louie)
                    
                    for flies in self.fly_swarm.flylist.sprites():
                        if not(flies.HP <= 0):
                            self.flies_collisions(player_action, self.fly_swarm.flylist, self.fly_swarm.flylist, flies, flies.damage)
                        if flies.HP <= 0:
                            self.sounds.enemies_death.play()
                            self.game.offset = self.game.screen_shake(3,5,20)
                            flies.kill()
                            self.spawn_exploding_particles(100, flies)

                        if not self.fly_swarm.flylist.sprites():
                            self.swarming = False
                            self.swamping = True
                            self.enemyflies_defeat = True
                            self.current_enemy = self.body_group
                            self.camera.add(self.enemy1)

                    if not(self.swarming):
                        if self.swamping:
                            if not(self.enemy1.HP <= 0):
                                if not(self.game.freeze):
                                    self.enemy1.update(deltatime, player_action, self.player.rect.center[0], 
                                                    self.player.rect.center[1], self.player.horiz_line, self.player.rect.x) 
                                    self.tongue.update(deltatime, player_action, self.enemy1.rect.centerx - 190, self.enemy1.rect.centery - 5, self.enemy1.attack)
                                    self.tongue2.update(deltatime, player_action, self.enemy1.rect.centerx -10, self.enemy1.rect.centery - 5, self.enemy1.attack)
                                    self.enemy_collisions(player_action, self.body_group, self.attack_group, self.enemy1, 
                                                self.enemy1.tongue_damage, self.enemy1.body_damage, self.tongue, self.tongue2)
                                self.enemy_health_update(self.enemy1.rect.x, self.enemy1.rect.y, self.enemy1.HP, self.enemy1.max_HP)
                        
                        
                        for enemy in self.body_group.sprites():
                            if enemy.HP <= 0:
                                self.sounds.enemies_death.play()
                                self.game.offset = self.game.screen_shake(3,5,20)
                                enemy.kill()
                                self.spawn_exploding_particles(100, enemy)
                                self.tongue.kill()
                                self.tongue2.kill()
                                self.enemy_defeat = True
                                self.swamping = False

                        if not(self.body_group.sprites()) and not(self.attack_group.sprites()):
                            self.enemyfrog_defeat = True

                    if self.enemyfrog_defeat and self.enemyflies_defeat:
                        self.enemy_defeat = True

                    if self.game.win:
                        self.spawn_particles(200, deltatime)
                    
                    if not(self.end):
                        if player_action["pause"]:
                            new_state = self.pause
                            new_state.enter_state()
                            self.game.start = False
            else:
                self.add_ultimate(deltatime, player_action, self.current_enemy)

            self.particle_group.update(deltatime)
            self.ult_VFX(deltatime)

        else:
            self.game.start_timer()


    def render(self, display):
        display.blit(pygame.transform.scale(self.game.forest3, (1100,600)), (0,0))
        self.confection_display(display)
        if self.game.defeat:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
        self.camera.custom_draw(display)

        # Player stats
        self.health_render(display)
        self.moxie_render(display)

        
        for flies in self.fly_swarm.flylist.sprites():
            if not(flies.HP <= 0):
                self.fly_swarm.render(display)
                self.groupenemy_health_render(display,self.fly_swarm.flylist.sprites())

        if self.game.freeze:
            for flies in self.fly_swarm.flylist.sprites():
                display.blit(self.game.ice, (flies.rect.x, flies.rect.y + 15))
        
        if self.swamping == True:
            if self.game.freeze:
                for frogs in self.body_group.sprites():
                    display.blit(self.game.ice, (frogs.rect.x + 5, frogs.rect.y + 40))

        if self.swamping == True:
            if not(self.enemy1.HP <= 0):
                if self.enemy1.current_anim_list == self.enemy1.attack_left:
                    self.tongue.render(display)
                elif self.enemy1.current_anim_list == self.enemy1.attack_right:
                    self.tongue2.render(display)
            if not(self.enemy1.HP <= 0):
                self.enemy_health_render(display, self.enemy1.rect.x, self.enemy1.rect.y)
                
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
                self.game.settings.first_win3 = True
                self.game.current_level = max(self.game.current_level, 3)
        else:
            self.end_prev = False
