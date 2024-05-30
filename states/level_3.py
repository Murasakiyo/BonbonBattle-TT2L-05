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


class Trio_Stage(State, Ults, Collisions, Health, Moxie, EnemyHealthBar):
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

        self.ultimates()
        self.characters()
        self.load_health_bar()
        self.load_moxie_bar()
        self.enemy_health_update(self.enemy1.rect.x, self.enemy1.rect.y, self.enemy1.HP)

        self.attack_group.add(self.tongue, self.tongue2)
        self.body_group.add(self.enemy1)

        self.current_time, self.end_time = 0,0
        self.moxie_points = 0
        self.swarming = True
        self.swamping = False
        self.enemy_defeat = False
        self.enemyfrog_defeat = False
        self.enemyflies_defeat = False

        self.end = False
        self.exit_game = False
        self.restart_game = False
        self.click = False
        self.state = "none"

    def update(self, deltatime, player_action):

        if player_action["reset_game"]:
            self.enemy1.remove(self.camera)
            self.tongue.remove(self.camera)
            self.tongue2.remove(self.camera)
            self.enemy1.enemy_reset()
            self.player.reset_player(200,200)
            self.ultimate_reset()
            self.enemy_health_update(self.enemy1.rect.x, self.enemy1.rect.y, self.enemy1.HP)
            self.load_health_bar()
            self.load_moxie_bar()
            for flies in self.fly_swarm.flylist.sprites():
                flies.kill()
                self.enemy_health_update(flies.rect.x,flies.rect.y, flies.HP)
            if self.enemyflies_defeat:
                # self.fly_swarm.flies_spawn()
                self.enemyflies_defeat = False
            if self.enemy_defeat:
                self.attack_group.add(self.tongue, self.tongue2)
                self.body_group.add(self.enemy1)
                self.enemyfrog_defeat = False
                self.enemy_defeat = False
            self.swamping = False
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

                if not(self.game.defeat):
                    print(self.game.win)
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
                            self.swamping = False

                        if not(self.body_group.sprites()) and not(self.attack_group.sprites()):
                            self.enemyfrog_defeat = True

                        self.enemy_collisions(deltatime, player_action, self.body_group, self.attack_group, self.enemy1, 
                                            self.enemy1.tongue_damage, self.enemy1.body_damage, self.tongue, self.tongue2)
                    
                    if not(self.end):
                        if player_action["pause"]:
                            new_state = self.pause
                            new_state.enter_state()
                            self.game.start = False

                    if self.enemyfrog_defeat and self.enemyflies_defeat:
                        self.enemy_defeat = True

            self.add_ultimate(deltatime, player_action)
        else:
            self.game.start_timer()
        # print(self.attack_time)

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

        if self.end:
            self.ending_state(display)
