import sys
import pygame as pg


WINDOW_HEIGHT = 700
WINDOW_WIDTH = 1000
GAME_NAME = TITLE = "VIKINGS_CHESS"
GAME_ICON = pg.image.load("images/vh.jpg")
MAIN_MENU_TOP_BUTTON_x = 400
MAIN_MENU_TOP_BUTTON_y = 150



bg = (204, 102, 0)
bg2 = (40,40,40)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255,255,1)
white = (255, 255, 255)

clicked = False


def write_text(text, screen, position, color, font):
    screen.fill(bg2)
    txtobj = font.render(text, True, (255, 255, 255))
    txtrect = txtobj.get_rect()
    txtrect.topleft = position
    screen.blit(txtobj, txtrect)


class custom_button():

    # colours for button and text
    button_col = (26, 117, 255)
    hover_col = red
    click_col = (50, 150, 255)
    text_col = yellow
    width = 180
    height = 70

    def __init__(self, x, y, text, screen, font):
        self.x = x
        self.y = y
        self.text = text
        self.screen = screen
        self.font = font

    def draw_button(self):

        global clicked
        action = False

        # get mouse position
        pos = pg.mouse.get_pos()

        # create pg Rect object for the button
        button_rect = pg.Rect(self.x, self.y, self.width, self.height)

        # check mouseover and clicked conditions
        if button_rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] == 1:
                clicked = True
                pg.draw.rect(self.screen, self.click_col, button_rect)
            elif pg.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pg.draw.rect(self.screen, self.hover_col, button_rect)
        else:
            pg.draw.rect(self.screen, self.button_col, button_rect)

        # add shading to button
        # pg.draw.line(self.screen, white, (self.x, self.y),
        #              (self.x + self.width, self.y), 2)
        # pg.draw.line(self.screen, white, (self.x, self.y),
        #              (self.x, self.y + self.height), 2)
        # pg.draw.line(self.screen, black, (self.x, self.y + self.height),
        #              (self.x + self.width, self.y + self.height), 2)
        # pg.draw.line(self.screen, black, (self.x + self.width, self.y),
        #              (self.x + self.width, self.y + self.height), 2)

        # add text to button
        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.screen.blit(text_img, (self.x + int(self.width / 2) -
                    int(text_len / 2), self.y + 15))
        return action


def game(screen):
    tafle = True
    while tafle:
        write_text("Game", screen, (20, 20), (255, 255, 255),
                   pg.font.SysFont("Arial", 20))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    tafle = False
        pg.display.update()


def rules(screen):
    tafle = True
    while tafle:
        write_text("Rules", screen, (20, 20), (255, 255, 255),
                   pg.font.SysFont("Arial", 20))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    tafle = False
        pg.display.update()


def history(screen):
    tafle = True
    while tafle:
        write_text("History", screen, (20, 20), (255, 255, 255),
                   pg.font.SysFont("Arial", 20))
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    tafle = False
        pg.display.update()


def main():
    pg.init()
    screen = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pg.display.set_caption(GAME_NAME)
    pg.display.set_icon(GAME_ICON)    
    

    game_on = True

    while game_on:
        # screen.fill(bg)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_on = False
                pg.quit()
                
        screen.fill(bg2)
        write_text("Welcome To Vikings Chess!", screen, (250, 20),
                   (255, 255, 255), pg.font.SysFont("Arial", 50))
        
        btn_font = pg.font.SysFont("Arial", 30)
        gamebtn = custom_button(MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y, "Play", screen, btn_font)
        rulesbtn = custom_button(MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y + 100, "Rules", screen, btn_font)
        historybtn = custom_button(MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y + 200, "History", screen, btn_font)
        exitbtn = custom_button(MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y + 300, "Exit", screen, btn_font)
        
        if gamebtn.draw_button():
            game(screen)
        
        if rulesbtn.draw_button():
            rules(screen)
        
        if historybtn.draw_button():
            history(screen)
        
        if exitbtn.draw_button():
            game_on = False
            pg.quit()

        # click = False      

               
        pg.display.update()


if __name__ == "__main__":
    main()
