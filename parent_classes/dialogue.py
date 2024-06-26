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
        self.text = texts
        self.message = self.text[self.activetext]
        self.done = False
        self.doneall = False
        self.next = False
        self.pos = self.box_rect
        self.finish_convo = False

    def reset_dialogue(self):
        self.counter = 0
        self.counter2 = 0
        self.activetext = 0
        self.done = False
        self.doneall = False
        self.next = False
        self.finish_convo = False
        self.message = self.text[self.activetext]
        self.box_rect.x, self.box_rect.y = 210, 380
        self.pos = self.box_rect


    def dialogue_update(self, player_action):
        if not(self.activetext >= len(self.text) - 1):
            self.message2 = self.text[self.activetext + 1]
        else:
            self.message2 = self.text[self.activetext]
        
        
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
    def __init__(self, game, ans1, ans2, ans3, ans4, three_ans, four_ans):
        self.game = game
        self.choice1 = ans1
        self.choice2 = ans2
        self.choice3 = ans3
        self.choice4 = ans4
        self.three_ans = three_ans
        self.four_ans = four_ans
        self.box = pygame.image.load("sprites/dialogue_box.png").convert_alpha()
        self.font = pygame.font.Font("Fonts/retro-pixel-cute-prop.ttf", 24)
        self.box_rect = self.box.get_rect(width = 700, height =200 )
        self.box_rect.x, self.box_rect.y = 210, 380
        self.color_hover = (0,0,14)
        self.color = (156, 145, 145)
        self.choicelist = self.check_choicelist()
        # self.init_answer()

        self.index= 0
        self.enter = self.font.render("[ENTER]", True, "Blue")
        self.current_time = 0
        self.answer = 0

        self.option1_hover = self.font.render(f">{self.choice1}", True, self.color_hover)
        self.option1 = self.font.render(f">{self.choice1}", True, self.color)
        self.option2_hover = self.font.render(f">{self.choice2}", True, self.color_hover)
        self.option2 = self.font.render(f">{self.choice2}", True, self.color)
        self.option3_hover = self.font.render(f">{self.choice3}", True, self.color_hover)
        self.option3 = self.font.render(f">{self.choice3}", True, self.color)
        self.option4_hover = self.font.render(f">{self.choice4}", True, self.color_hover)
        self.option4 = self.font.render(f">{self.choice4}", True, self.color)

        self.current_option1 = self.option1
        self.current_option2 = self.option2
        self.current_option3 = self.option3
        self.current_option4 = self.option4

    def check_choicelist(self):
        if self.three_ans:
            choicelist = {0: "answer1", 1: "answer2", 2: "answer3"}
        elif self.four_ans:
            choicelist = {0: "answer1", 1: "answer2", 2:"answer3", 3:"answer4"}
        else:
            choicelist = {0: "answer1", 1: "answer2"}
        return choicelist
    

    def update(self, deltatime, player_action):
        self.update_keys(deltatime)


    def pick_choice(self, player_action):
        
        if self.choicelist[self.index] == "answer1":
            self.current_option1 = self.option1_hover
            if player_action["go"]:
                self.answer = 1
                return self.answer
        else:
            self.current_option1 = self.option1

        if self.choicelist[self.index] == "answer2":
            self.current_option2 = self.option2_hover
            if player_action["go"]:
                self.answer = 2
                return self.answer
        else:
            self.current_option2 = self.option2

        if self.three_ans or self.four_ans:
            if self.choicelist[self.index] == "answer3":
                self.current_option3 = self.option3_hover
                if player_action["go"]:
                    self.answer = 3
                    return self.answer
            else:
                self.current_option3 = self.option3


        if self.four_ans:
            if self.choicelist[self.index] == "answer4":
                self.current_option4 = self.option4_hover
                if player_action["go"]:
                    self.answer = 4
                    return self.answer
            else:
                self.current_option4 = self.option4
    
    def reset_options(self):
        self.index = 0
        self.answer = 0
         

    def render(self,display):
        x, y= 250, 410
        display.blit(self.box, (self.box_rect.x, self.box_rect.y))

        display.blit(self.current_option1, (x,y))
        display.blit(self.current_option2, (x,y+30))
        if self.three_ans or self.four_ans:
            display.blit(self.current_option3, (x,y+60))
        if self.four_ans:
            display.blit(self.current_option4, (x,y+90))
        display.blit(self.enter, (790, 530))
    

    def update_keys(self, deltatime):
        self.current_time += deltatime
        if self.current_time > 0.12:
            if self.game.convo_keys["down"]:  
                self.index = (self.index + 1) % len(self.choicelist)
            elif self.game.convo_keys["up"]:
                self.index = (self.index - 1) % len(self.choicelist)
            self.current_time = 0
    
