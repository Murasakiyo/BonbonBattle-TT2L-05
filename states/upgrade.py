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
        self.new_attack = 0
        self.new_health = 0
        self.new_speed = 0
        self.sugar_price = 0
        self.apply_upgrades = False


    def update(self, deltatime, player_action):
        player_action["up"], player_action["down"], player_action["right"], player_action["left"] = False, False, False, False
        player_action["ultimate"], player_action["attack"], player_action["defend"],= False, False, False
        self.player.update(deltatime,player_action)

        if self.attack_up_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.new_attack += 1
                self.sugar_price += 20
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False

        if self.attk_down_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click and not self.new_attack <= 0:
                self.new_attack -= 1
                self.sugar_price -= 20
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False



        if self.health_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.new_health += 1
                self.sugar_price += 20
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False

        if self.hdown_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click and not self.new_health <= 0:
                self.new_health -= 1
                self.sugar_price -= 20
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False




        if self.speed_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.new_speed += 1
                self.sugar_price += 20
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False

        if self.sdown_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click and not self.new_speed <= 0:
                self.new_speed -= 1
                self.sugar_price -= 20
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.click = False

        print(self.sugar_price)


        if self.upgrade_rect.collidepoint(self.game.mouse):
            if pygame.mouse.get_pressed()[0] and not self.click:
                self.apply_upgrades = True
                self.click = True
            if not pygame.mouse.get_pressed()[0]:
                self.apply_upgrades = False
                self.click = False            

        if self.apply_upgrades:
            self.player.attackpoints += self.new_attack
            self.player.healthpoints += self.new_health
            self.player.speed += self.new_speed
            self.current_currency -= self.sugar_price



        if player_action["pause"]:
            self.exit_state(-1)


    def render(self, display):
        display.blit(self.assets["menu"], (self.menu_rect))
        self.camera.custom_draw(display)
        display.blit(self.game.sugarcube_image, (10, 10))
        self.game.draw_text(display, f"{int(self.game.current_currency)}", False, "white", 40, 10, 35)
        self.game.draw_text(display, f"Attack: {int(self.player.attackpoints)}", False, (0,0,14), self.menu_rect.x + 30, self.menu_rect.y + 320, 25)
        self.game.draw_text(display, f"Health: {int(self.player.healthpoints)}", False, (0,0,14), self.menu_rect.x + 30, self.menu_rect.y + 350, 25)
        self.game.draw_text(display, f"Speed: {int(self.player.speed - 395)}", False, (0,0,14), self.menu_rect.x + 30, self.menu_rect.y + 380, 25)
        self.game.draw_text(display, f"Total: {int(self.sugar_price)}", False, (0, 0, 14), self.menu_rect.x + 200, self.menu_rect.y + 380, 25)
        self.game.draw_text(display, "Torres Ganache", True, (0,0,14), self.menu_rect.x + 30, self.menu_rect.y + 280, 30)
        self.hover_button(display, self.upgrade_rect, self.current_upgrade, self.assets["upgrade"], self.assets["upg_hover"])
        pygame.draw.rect(display, "white", self.attack_up_rect)
        pygame.draw.rect(display, "white", self.attk_down_rect)
        pygame.draw.rect(display, "white", self.health_rect)
        pygame.draw.rect(display, "white", self.hdown_rect)
        pygame.draw.rect(display, "white", self.speed_rect)
        pygame.draw.rect(display, "white", self.sdown_rect)
        


        # Displaying Attack upgrades
        display.blit(self.attack_up, (self.menu_rect.x + 300, self.menu_rect.y + 80))
        display.blit(self.attack_down, self.attk_down_rect)
        self.game.draw_text(display, f"{int(self.new_attack)}", True, (0,0,14), self.menu_rect.x + 405, self.menu_rect.y + 80, 40)
        self.game.draw_text(display, "ATTACK", True, (0,0,14), self.menu_rect.x + 370, self.menu_rect.y + 35, 30)

        # Displaying Health upgrades
        display.blit(self.health_up, self.health_rect)
        display.blit(self.health_down, self.hdown_rect)
        self.game.draw_text(display, f"{int(self.new_health)}", True, (0,0,14), self.menu_rect.x + 405, self.menu_rect.y + 180, 40)
        self.game.draw_text(display, "HEALTH", True, (0,0,14), self.menu_rect.x + 370, self.menu_rect.y + 140, 30)

        # Displaying Speed upgrades
        display.blit(self.speed_up, self.speed_rect)
        display.blit(self.speed_down, self.sdown_rect)
        self.game.draw_text(display, f"{int(self.new_speed)}", True, (0,0,14), self.menu_rect.x + 405, self.menu_rect.y + 280, 40)
        self.game.draw_text(display, "SPEED", True, (0,0,14), self.menu_rect.x + 375, self.menu_rect.y + 240, 30)

        self.game.draw_text(display, "[Back]", False, ("white"), 965, 60, 30)
        display.blit(self.game.backspace, (960, 10))

        