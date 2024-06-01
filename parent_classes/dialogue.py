import pygame


class Dialogue():
    def __init__(self, game):
        self.game = game
        
    def variable(self, color, size, texts):
        self.color = color
        self.box = pygame.image.load("sprites/dialogue_box.png").convert_alpha()
        self.box_rect = self.box.get_rect(width = 700, height =200 )
        self.box_rect.x, self.box_rect.y = 210, 380
        # self.text_x, self.text_y = self.box_rect.x + 20, self.box_rect.y + 30
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


    def dialogue_update(self, player_action):
        if not(self.activetext >= len(self.text) - 1):
            self.message2 = self.text[self.activetext + 1]
        else:
            self.message2 = self.text[self.activetext]
        print(f"activetext:{self.activetext}")
        print(f"requirements:{len(self.text) - 1}")
        
        # print (self.pos)
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
        # print(list(self.message2))
        display.blit(self.box, (self.box_rect.x, self.box_rect.y))
    
        self.snip = self.font.render(self.message[0:self.counter//self.speed], True, self.color)
        self.space = self.font.render("[SPACE]", True, "Blue")

        if self.activetext != len(self.text) - 1:
            display.blit(self.snip, (self.pos[0]+30, self.pos[1]+30))
            if self.next:
                self.snip2 = self.font.render(self.message2[0:self.counter2//self.speed], True, self.color)
                display.blit(self.snip2, (self.pos[0]+30, self.pos[1] + 60))

        if self.doneall and self.activetext < len(self.text) - 1:
            display.blit(self.space, (self.pos[0]+580, self.pos[1] + 150))

        if self.activetext >= len(self.text) - 1:
            self.pos[1] += 10 * 1.2

    
    def dialogue(self, filename):
        text = list()
        self.open_file = open(f"texts/{filename}")
        text = self.open_file.readlines()

        for x in range(len(text)):
            text[x] = text[x].strip()
        text.append(" ")
        self.open_file.close()
        return text

            
