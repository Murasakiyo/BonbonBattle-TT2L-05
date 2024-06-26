import pygame
from parent_classes.state import *
from torres import *
from enemy1 import *
from states.pause_menu import *
from states.tutorial import *
from confection import *
from parent_classes.ultimate_action import *
from parent_classes.health import *
from parent_classes.collisions import *
from parent_classes.moxie import *
from parent_classes.enemyhealthbar import *
from parent_classes.particleeffect import *
from parent_classes.sugarcube import *



class First_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar, ParticleFunctions, SugarcubeSpawn):
    def __init__(self, game):
        super().__init__(game)
        # Sprite groups
        self.camera = CameraGroup(self.game)
        self.confection_ult = pygame.sprite.Group()
        self.support_dolls = pygame.sprite.Group()
        self.attack_group = pygame.sprite.Group()
        self.body_group = pygame.sprite.Group()
        self.particle_group = pygame.sprite.Group()
        self.sugarcube_list = pygame.sprite.Group()
        self.enemy1 = FrogEnemy(self.game)
        self.tongue = Tongue(self.game)
        self.tongue2 = Tongue2(self.game)
        self.pause = Pause(self.game)
        self.sounds = self.game.sounds

        self.ultimates()
        self.characters(200,200)
        self.load_health_bar()
        self.load_moxie_bar()
        self.enemy_health_update(self.enemy1.rect.x, self.enemy1.rect.y, self.enemy1.HP, self.enemy1.max_HP)

        self.camera.add(self.enemy1)
        self.attack_group.add(self.tongue, self.tongue2)
        self.body_group.add(self.enemy1)

        # Variables for ultimate
        self.current_time, self.end_time = 0,0
        self.gacha = 0
        self.accept_ult = False
        self.enemy_defeat = False

        # Variables for particles
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

        # Variables for tutorial
        self.tuto_time = 0
        self.tuto1_done = False
        self.tuto2_done = False
        self.tuto3_done = False
        self.tuto4_done = False
        self.tuto5_done = False
        self.tuto6_done = False
        self.show_moxie = False
        self.overlay = pygame.image.load("sprites/moxie_show.png").convert_alpha()
        self.end_prev = False


    # method overriding
    def enter_state(self):
        super().enter_state()  # Call parent class's method (to update the level)
        self.game.play_bg_music(self.game.sounds.lvl1_bgmusic)
        self.player.attribute_update()
        if self.game.current_level == 0:
            self.current_sugarcube_value = self.game.settings.first_sugarcube_value
        else:
            self.current_sugarcube_value = self.game.settings.sugarcube_value


    def update(self, deltatime, player_action):
        if player_action["reset_game"]:
            self.game.play_bg_music(self.game.sounds.lvl1_bgmusic)
            if self.game.settings.first_win1:
                self.current_sugarcube_value = self.game.settings.sugarcube_value
            self.enemy1.enemy_reset()
            self.player.reset_player(200,200)
            self.ultimate_reset()
            self.enemy_health_update(self.enemy1.rect.x, self.enemy1.rect.y, self.enemy1.HP, self.enemy1.max_HP)
            self.load_health_bar()
            self.load_moxie_bar()
            if self.enemy_defeat:
                self.attack_group.add(self.tongue, self.tongue2)
                self.body_group.add(self.enemy1)
                self.camera.add(self.enemy1)
                self.enemy_defeat = False
            self.sugarcube_list.empty()
            self.game.start = False
            self.current_time = 0
            self.sugarcube_received = 0
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
        self.ending_options(deltatime, player_action, 2, 1)

        if not(self.game.settings.tutorial):
            self.tuto4_done = True
        

        if self.game.start == True:
            if not(self.game.ult):
                # Update player
                self.player.update(deltatime, player_action)
                self.player_attacking(deltatime, self.body_group, self.enemy1)
                if self.tuto4_done:
                    self.update_ultimate(deltatime, player_action)
                self.cooldown_for_attacked(deltatime)
                self.health_update()
                self.moxie_update(player_action)
                self.game.frozen()

                self.tutorial_game(deltatime)

                # Update enemies
                if not(self.game.defeat):
                    if not(self.enemy1.HP <= 0):
                        if not(self.game.freeze):
                            self.enemy1.update(deltatime, player_action, self.player.rect.center[0], 
                                            self.player.rect.center[1], self.player.horiz_line, self.player.rect.x) 
                            self.tongue.update(deltatime, player_action, self.enemy1.rect.centerx - 190, self.enemy1.rect.centery - 5, self.enemy1.attack)
                            self.tongue2.update(deltatime, player_action, self.enemy1.rect.centerx -10, self.enemy1.rect.centery - 5, self.enemy1.attack)
                            # Check collision of enemies and players
                            self.enemy_collisions(player_action, self.body_group, self.attack_group, self.enemy1, 
                                            self.enemy1.tongue_damage, self.enemy1.body_damage, self.tongue, self.tongue2)
                        self.enemy_health_update(self.enemy1.rect.x, self.enemy1.rect.y, self.enemy1.HP, self.enemy1.max_HP)
                        
                    if self.louie.slow_down:
                        self.enemy1.speed = self.enemy1.speed * (50/100)
                        
                    if self.game.win:
                        self.spawn_particles(200, deltatime)

                    for enemy in self.body_group.sprites():
                        if enemy.HP <= 0:
                            self.sounds.enemies_death.play()
                            self.game.offset = self.game.screen_shake(3,5,20)
                            enemy.kill()
                            self.spawn_exploding_particles(100, enemy)
                            self.tongue.kill()
                            self.tongue2.kill()
                            self.enemy_defeat = True

                    if not(self.end):
                        if player_action["pause"]:
                            new_state = self.pause
                            new_state.enter_state()
                            self.game.start = False
                            
            else:
                self.add_ultimate(deltatime, player_action, self.body_group)

            self.particle_group.update(deltatime)
            self.ult_VFX(deltatime)
        else:
            self.game.start_timer()


    def render(self, display):

        display.blit(pygame.transform.scale(self.game.forest, (1100,600)), (0,0))
        # self.player.render(display)
        self.confection_display(display)
        if self.game.defeat:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
        self.camera.custom_draw(display)

        # If the enemy is not dead yet
        if not(self.enemy1.HP <= 0):
            if self.enemy1.current_anim_list == self.enemy1.attack_left:
                self.tongue.render(display)
            elif self.enemy1.current_anim_list == self.enemy1.attack_right:
                self.tongue2.render(display)

        if self.game.defeat or self.game.player_action["reset_game"]:
            self.tongue.image= self.tongue.idle[0]
            self.tongue2.image= self.tongue.idle[0]

        display.blit(pygame.transform.scale(self.game.trees, (1200,600)), (-60,0))
        
        self.health_render(display)
        self.moxie_render(display)
        if self.enemy1.HP <= 0:
            self.sugarcube_list.draw(display)


        if not(self.enemy1.HP <= 0):
            self.enemy_health_render(display, self.enemy1.rect.x, self.enemy1.rect.y)
        
        if self.game.freeze:
            for enemy in self.body_group:
                display.blit(self.game.ice, (enemy.rect.x + 5, enemy.rect.y + 20))

        if self.game.ult:
            display.blit(pygame.transform.scale(self.game.black, (1100,600)), (0,0))
        self.particle_group.draw(display)
        self.ultimate_display(display)

        if self.show_moxie:
            display.blit(self.overlay, (0,0))

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
                self.game.settings.first_win1 = True
                self.game.current_level = max(self.game.current_level, 1)
    
    def tutorial_game(self, deltatime):
        if self.game.tutorial_counter == 1:
            self.tuto1_done = True
        if self.game.tutorial_counter == 2:
            self.tuto2_done = True
        if self.game.tutorial_counter == 3:
            self.tuto3_done = True
        if self.game.tutorial_counter == 4:
            self.tuto4_done = True
            self.show_moxie = False
        if self.game.tutorial_counter == 5:
            self.tuto5_done = True
        if self.game.tutorial_counter == 6:
            self.tuto6_done = True

        if self.game.settings.tutorial:
            new_state = Tutorial(self.game, self.player.rect.centerx, self.player.rect.centery)
            if not self.tuto1_done:
                self.tuto_time += deltatime
                if self.tuto_time > 0.4:
                    new_state.enter_state()
                    self.tuto_time = 0
            if self.tuto1_done and not(self.tuto2_done):
                self.tuto_time += deltatime
                if self.tuto_time > 1:
                    new_state.enter_state()
                    self.tuto_time = 0
            if self.tuto2_done and not(self.tuto3_done):
                self.tuto_time += deltatime
                if self.tuto_time > 1:
                    new_state.enter_state()
                    self.tuto_time = 0
            if self.tuto3_done and not(self.tuto4_done):
                self.tuto_time += deltatime
                if self.tuto_time > 2.8:
                    self.show_moxie = True
                if self.tuto_time > 3:
                    new_state.enter_state()
                    self.tuto_time = 0
            if self.tuto4_done and not(self.tuto5_done):
                if self.confection_ult.sprites():
                    self.tuto_time += deltatime
                    if self.tuto_time > 1:
                        new_state.enter_state()
                        self.tuto_time = 0
            if self.tuto5_done and not(self.tuto6_done):
                if self.support_dolls.sprites():
                    self.tuto_time += deltatime
                    if self.tuto_time > 1:
                        new_state.enter_state()
                        self.tuto_time = 0
            if self.tuto6_done and not self.body_group.sprites():
                new_state.enter_state()
       
            



