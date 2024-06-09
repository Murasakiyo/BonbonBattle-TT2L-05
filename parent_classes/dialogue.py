import pygame


class Dialogue():
    def __init__(self, game, color, size, texts):
        self.game = game
        self.variable(color, size, texts)
        
    def variable(self, color, size, texts):
        self.color = color
        self.box = pygame.image.load("sprites/dialogue_box.png").convert_alpha()
        self.box_rect = self.box.get_rect(width = 700, height =200 )
        self.box_rect.x, self.box_rect.y = 210, 380
        self.font = pygame.font.Font("Fonts/retro-pixel-cute-prop.ttf", size)
        self.snip = self.font.render(" ", True, self.color)
        self.counter = 0
        self.counter2 = 0
        self.speed = 1
        self.activetext = 0
        self.num =0
        self.text = texts
        self.message = self.text[self.activetext]
        self.done = False
        self.doneall = False
        self.next = False
        self.pos = self.box_rect
        self.finish_convo = False


    def dialogue_update(self, player_action):
        if not(self.activetext >= len(self.text) - 1):
            self.message2 = self.text[self.activetext + 1]
        else:
            self.message2 = self.text[self.activetext]
        # print(f"activetext:{self.activetext}")
        # print(f"requirements:{len(self.text) - 1}")
        
        if self.counter < self.speed * len(self.message):
            self.counter = self.counter + 1
        elif self.counter >= self.speed*len(self.message):
            self.done = True

        if self.next:
            if self.counter2 < self.speed * len(self.message2):
                self.counter2 = self.counter2 + 1
            elif self.counter2 >= self.speed*len(self.message2):
                self.doneall = True
        
        if self.done:
            self.next = True

        if player_action["next"] and self.doneall and self.activetext < len(self.text) - 1:
            if not(self.activetext >= len(self.text) - 2):
                self.activetext += 2
            else:
                self.activetext += 1
            self.done = False
            self.next = False
            self.doneall = False
            self.message = self.text[self.activetext]
            self.counter = 0
            self.counter2 = 0
            player_action["next"] = False


    def draw_text(self,display):
        display.blit(self.box, (self.box_rect.x, self.box_rect.y))
    
        self.snip = self.font.render(self.message[0:self.counter//self.speed], True, self.color)
        self.space = self.font.render("[SPACE]", True, "Blue")

        if self.activetext != len(self.text) - 1:
            display.blit(self.snip, (240, 410))
            if self.next:
                self.snip2 = self.font.render(self.message2[0:self.counter2//self.speed], True, self.color)
                display.blit(self.snip2, (240, 440))

        if self.doneall and self.activetext < len(self.text) - 1:
            display.blit(self.space, (790, 530))

    def finish(self):
         if self.activetext >= len(self.text) - 1:
            self.finish_convo = True
    
    def transtion_end(self):
        if self.activetext >= len(self.text) - 1:
            if self.pos[1] <= 800:
                self.pos[1] += 10 * 1.2
            else:
                self.pos[1] = self.pos[1]
                self.finish_convo = True
    
class Answer():
    def __init__(self, game, ans1, ans2, ans3):
        self.game = game
        self.choice1 = ans1
        self.choice2 = ans2
        self.choice3 = ans3
        self.box = pygame.image.load("sprites/dialogue_box.png").convert_alpha()
        self.font = pygame.font.Font("Fonts/retro-pixel-cute-prop.ttf", 24)
        self.box_rect = self.box.get_rect(width = 700, height =200 )
        self.box_rect.x, self.box_rect.y = 210, 380
        self.color_hover = (0,0,14)
        self.color = (156, 145, 145)
        self.choicelist = {0: "answer1", 1: "answer2", 2: "answer3"}
        self.index = 0
        self.enter = self.font.render("[ENTER]", True, "Blue")
        self.current_time = 0

        self.option1_hover = self.font.render(f">{self.choice1}", True, self.color_hover)
        self.option1 = self.font.render(f">{self.choice1}", True, self.color)
        self.option2_hover = self.font.render(f">{self.choice2}", True, self.color_hover)
        self.option2 = self.font.render(f">{self.choice2}", True, self.color)
        self.option3_hover = self.font.render(f">{self.choice3}", True, self.color_hover)
        self.option3 = self.font.render(f">{self.choice3}", True, self.color)

        self.current_option1 = self.option1
        self.current_option2 = self.option2
        self.current_option3 = self.option3


    def update(self, deltatime, player_action):
        self.update_keys(deltatime)

    def pick_choice(self, player_action):
        if self.choicelist[self.index] == "answer1":
            self.current_option1 = self.option1_hover
            if player_action["go"]:
                answer = 1
                return answer
        else:
            self.current_option1 = self.option1
        if self.choicelist[self.index] == "answer2":
            self.current_option2 = self.option2_hover
            if player_action["go"]:
                answer = 2
                return answer
        else:
            self.current_option2 = self.option2
        if self.choicelist[self.index] == "answer3":
            self.current_option3 = self.option3_hover
            if player_action["go"]:
                answer = 3
                return answer
        else:
            self.current_option3 = self.option3
         

    def render(self,display):
        x, y= 250, 410
        display.blit(self.box, (self.box_rect.x, self.box_rect.y))

        display.blit(self.current_option1, (x,y))
        display.blit(self.current_option2, (x,y+30))
        display.blit(self.current_option3, (x,y+60))
        display.blit(self.enter, (790, 530))
            

    def update_keys(self, deltatime):
        # print("updating..")
        self.current_time += deltatime
        if self.current_time > 0.13:
            if self.game.convo_keys["down"]:  
                self.index = (self.index + 1) % len(self.choicelist)
            elif self.game.convo_keys["up"]:
                self.index = (self.index - 1) % len(self.choicelist)
            self.current_time = 0
