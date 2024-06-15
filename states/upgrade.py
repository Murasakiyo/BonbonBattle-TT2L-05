import pygame
from parent_classes.state import *
from parent_classes.dialogue import *
from torres import *
from krie import *

class Upgrade(State, Dialogue):
    def __init__(self, game):
        super().__init__(game)
        self.game = game
        self.player = Player(self.game, 290, 100)
        self.camera = CameraGroup(self.game)
        self.sounds = self.game.sounds
        self.camera.add(self.player)
        self.assets = {
            "menu": pygame.image.load("sprites/upgrade_menu.png").convert_alpha(),
            "up": pygame.image.load("sprites/buttons/up.png").convert_alpha(),
            "down": pygame.image.load("sprites/buttons/down.png").convert_alpha(),
            "upgrade": pygame.image.load("sprites/buttons/buy.png").convert_alpha(),
            "upg_hover": pygame.image.load("sprites/buttons/buy_hover.png").convert_alpha()
         }
        self.menu_rect = self.assets["menu"].get_rect(x = 250, y = 50)
        self.attack_up, self.health_up, self.speed_up = self.assets["up"], self.assets["up"], self.assets["up"]
        self.attack_down, self.health_down, self.speed_down = self.assets["down"], self.assets["down"], self.assets["down"]

        self.attack_up_rect = self.attack_up.get_rect(x= 550, y= 130)
        self.attk_down_rect = self.attack_down.get_rect(x = self.menu_rect.x + 480, y = self.menu_rect.y + 80 )
        self.health_rect = self.health_up.get_rect(x = self.menu_rect.x + 300, y= self.menu_rect.y + 180 )
        self.hdown_rect = self.health_down.get_rect(x = self.menu_rect.x + 480, y = self.menu_rect.y + 180)
        self.speed_rect = self.health_up.get_rect(x = self.menu_rect.x + 300, y = self.menu_rect.y + 280 )
        self.sdown_rect = self.health_down.get_rect(x = self.menu_rect.x + 480, y= self.menu_rect.y + 280)
        self.upgrade_rect = self.assets["upgrade"].get_rect(x = self.menu_rect.x + 330, y = self.menu_rect.y + 360)
        self.current_upgrade = self.assets["upgrade"]
        self.sugar_price = 0
        self.add_atk = 0
        self.add_HP = 0
        self.add_spd = 0
        self.atk_level = 0
        self.HP_level = 0
        self.spd_level = 0
        self.apply_upgrades = False


    def update(self, deltatime, player_action):

        # Only want Player's animation, not input
        player_action["up"], player_action["down"], player_action["right"], player_action["left"] = False, False, False, False
        player_action["ultimate"], player_action["attack"], player_action["defend"],= False, False, False

        self.player.update(deltatime,player_action)
        # self.player.upgrade()

        # Backspace key, leave room
        if self.attack_up_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click and self.game.current_currency >= 125:
                if self.game.settings.current_atk_level < 12 and self.atk_level < 12:
                    self.atk_level += 1 # Max is 12
                    self.add_atk += 1
                    self.sugar_price += 125
                    self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False

        if self.attk_down_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click and not self.game.settings.current_atk_level <= 0 and not self.add_atk <= 0:
                print("atk")
                self.sugar_price -= 125
                self.atk_level -= 1
                self.add_atk -= 1
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False


        if self.health_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click and self.game.current_currency >= 125:
                if self.game.settings.current_HP_level < 10 and self.HP_level < 10:
                    self.HP_level += 1 # Max is 10
                    self.add_HP += 50
                    self.sugar_price += 125
                    self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False

        if self.hdown_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click and not self.game.settings.current_HP_level <= 0 and not self.add_HP <= 0:
                print("hp")
                self.sugar_price -= 125
                self.HP_level -= 1
                self.add_HP -= 50
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False


        if self.speed_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click and self.game.current_currency >= 100:
                if self.game.settings.current_spd_level < 10 and self.spd_level < 10:
                    self.spd_level += 1 # Max is 10
                    self.add_spd += 10
                    self.sugar_price += 100
                    self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False

        if self.sdown_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click and not self.game.settings.current_spd_level <= 0 and not self.add_spd <= 0:
                print("spd")
                self.sugar_price -= 100
                self.spd_level -= 1
                self.add_spd -= 10
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False

        if self.upgrade_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.apply_upgrades = True
                self.click = True
                if self.sugar_price != 0 and self.game.current_currency >= self.sugar_price:
                    self.sounds.upgrade_clicked.play()
                else:
                    self.sounds.no_upgrade.play()

            if not pygame.mouse.get_pressed()[0]:
                self.apply_upgrades = False
                self.click = False            

        if self.apply_upgrades and self.game.current_currency >= self.sugar_price:
            self.game.settings.current_atk_level += self.atk_level
            self.game.settings.current_HP_level += self.HP_level
            self.game.settings.current_spd_level += self.spd_level
            self.game.settings.current_attackpoints += self.add_atk
            self.game.settings.current_healthpoints += self.add_HP
            self.game.settings.current_speed += self.add_spd
            self.game.current_currency -= self.sugar_price
            self.add_atk = 0
            self.add_HP = 0
            self.add_spd = 0
            self.sugar_price = 0

        if player_action["pause"]:
            self.exit_state(-1)
            self.add_atk = 0
            self.add_HP = 0
            self.add_spd = 0
            self.sugar_price = 0


    def render(self, display):
        display.blit(self.assets["menu"], (self.menu_rect))
        self.camera.custom_draw(display)
        display.blit(self.game.sugarcube_image, (285, 80))
        self.game.draw_text(display, f"{int(self.game.current_currency)}", False, "white", 315, 80, 35)
        self.game.draw_text(display, f"Attack: {int(self.game.settings.current_attackpoints)}", False, (0,0,14), self.menu_rect.x + 30, self.menu_rect.y + 320, 25)
        self.game.draw_text(display, f"Health: {int(self.game.settings.current_healthpoints)}", False, (0,0,14), self.menu_rect.x + 30, self.menu_rect.y + 350, 25)
        self.game.draw_text(display, f"Speed: {int(self.game.settings.current_speed)}", False, (0,0,14), self.menu_rect.x + 30, self.menu_rect.y + 380, 25)
        self.game.draw_text(display, f"Total:{int(self.sugar_price)}", False, (0, 0, 14), self.menu_rect.x + 185, self.menu_rect.y + 380, 25)
        self.game.draw_text(display, "Torres Ganache", True, (0,0,14), self.menu_rect.x + 30, self.menu_rect.y + 280, 30)
        self.hover_button(display, self.upgrade_rect, self.current_upgrade, self.assets["upgrade"], self.assets["upg_hover"])

        


        # Displaying Attack upgrades
        display.blit(self.attack_up, (self.menu_rect.x + 300, self.menu_rect.y + 80))
        display.blit(self.attack_down, self.attk_down_rect)
        if self.game.settings.current_atk_level < 12:
            self.game.draw_text(display, f"{int(self.add_atk)}", True, (0,0,14), self.menu_rect.x + 405, self.menu_rect.y + 80, 40)
        if self.game.settings.current_atk_level >= 12:
            self.game.draw_text(display, "MAX", True, (0,0,14), self.menu_rect.x + 385, self.menu_rect.y + 80, 40)
        self.game.draw_text(display, "ATTACK", True, (0,0,14), self.menu_rect.x + 370, self.menu_rect.y + 35, 30)

        # Displaying Health upgrades
        display.blit(self.health_up, self.health_rect)
        display.blit(self.health_down, self.hdown_rect)
        if self.game.settings.current_HP_level < 10:
            self.game.draw_text(display, f"{int(self.add_HP)}", True, (0,0,14), self.menu_rect.x + 405, self.menu_rect.y + 180, 40)
        if self.game.settings.current_HP_level >= 10:
            self.game.draw_text(display, "MAX", True, (0,0,14), self.menu_rect.x + 385, self.menu_rect.y + 180, 40)
        self.game.draw_text(display, "HEALTH", True, (0,0,14), self.menu_rect.x + 370, self.menu_rect.y + 140, 30)

        # Displaying Speed upgrades
        display.blit(self.speed_up, self.speed_rect)
        display.blit(self.speed_down, self.sdown_rect)
        if self.game.settings.current_spd_level < 10:
            self.game.draw_text(display, f"{int(self.add_spd)}", True, (0,0,14), self.menu_rect.x + 405, self.menu_rect.y + 280, 40)
        if self.game.settings.current_spd_level >= 10:
            self.game.draw_text(display, "MAX", True, (0,0,14), self.menu_rect.x + 385, self.menu_rect.y + 280, 40)
        self.game.draw_text(display, "SPEED", True, (0,0,14), self.menu_rect.x + 375, self.menu_rect.y + 240, 30)

        self.game.draw_text(display, "[Backspace]", False, ("white"), 920, 60, 30)
        display.blit(self.game.backspace, (960, 10))

        