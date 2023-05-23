import sys
import pygame as pg


WINDOW_HEIGHT = 700
WINDOW_WIDTH = 1000
GAME_NAME = TITLE = "VIKINGS_CHESS"
GAME_ICON = pg.image.load("images/vh.jpg")
MAIN_MENU_TOP_BUTTON_x = 400
MAIN_MENU_TOP_BUTTON_y = 150
BOARD_TOP = 120
BOARD_LEFT = 225
CELL_WIDTH = 50
CELL_HEIGHT = 50


bg = (204, 102, 0)
bg2 = (40, 40, 40)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255, 255, 1)
golden = (255, 215, 0)
white = (255, 255, 255)

clicked = False


def write_text(text, screen, position, color, font):
    screen.fill(bg2)
    txtobj = font.render(text, True, (255, 255, 255))
    txtrect = txtobj.get_rect()
    txtrect.topleft = position
    screen.blit(txtobj, txtrect)


class Custom_button:

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


class ChessBoard:

    def __init__(self, screen, board_size="large"):

        if board_size == "large":

            self.initial_pattern = [['x', '.', '.', 'a', 'a', 'a', 'a', 'a', '.', '.', 'x'],
                                    ['.', '.', '.', '.', '.', 'a',
                                        '.', '.', '.', '.', '.'],
                                    ['.', '.', '.', '.', '.', '.',
                                        '.', '.', '.', '.', '.'],
                                    ['a', '.', '.', '.', '.', 'd',
                                        '.', '.', '.', '.', 'a'],
                                    ['a', '.', '.', '.', 'd', 'd',
                                        'd', '.', '.', '.', 'a'],
                                    ['a', 'a', '.', 'd', 'd', 'c',
                                        'd', 'd', '.', 'a', 'a'],
                                    ['a', '.', '.', '.', 'd', 'd',
                                        'd', '.', '.', '.', 'a'],
                                    ['a', '.', '.', '.', '.', 'd',
                                        '.', '.', '.', '.', 'a'],
                                    ['.', '.', '.', '.', '.', '.',
                                        '.', '.', '.', '.', '.'],
                                    ['.', '.', '.', '.', '.', 'a',
                                        '.', '.', '.', '.', '.'],
                                    ['x', '.', '.', 'a', 'a', 'a', 'a', 'a', '.', '.', 'x']]

        self.rows = len(self.initial_pattern)
        self.columns = len(self.initial_pattern[0])
        self.cell_width = CELL_WIDTH
        self.cell_height = CELL_HEIGHT
        self.screen = screen

    def draw_empty_board(self):

        color_flag = True
        for row in range(self.rows):
            for column in range(self.columns):
                cell_rect = pg.Rect(BOARD_LEFT + column * self.cell_width, BOARD_TOP +
                                    row * self.cell_height, self.cell_width, self.cell_height)
                
                if (row == 0 or row == self.rows-1) and (column == 0 or column == self.columns-1):
                    pg.draw.rect(self.screen, red, cell_rect)
                elif row == int(self.rows / 2) and column == int(self.columns / 2):
                    pg.draw.rect(self.screen, golden, cell_rect)                    
                elif color_flag:
                    pg.draw.rect(self.screen, white, cell_rect)                    
                else:
                    pg.draw.rect(self.screen, black, cell_rect)
                    
                color_flag = not color_flag

def game(screen):
    tafle = True
    while tafle:
        write_text("Play Vikings Chess", screen, (20, 20), (255, 255, 255),
                   pg.font.SysFont("Arial", 40))
        backbtn = Custom_button(800, 20, "Back", screen,
                                pg.font.SysFont("Arial", 30))
        restartbtn = Custom_button(
            600, 20, "Restart", screen, pg.font.SysFont("Arial", 30))

        if backbtn.draw_button():
            main()

        if restartbtn.draw_button():
            pass

        chessboard = ChessBoard(screen)
        chessboard.draw_empty_board()
        
        
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
        gamebtn = Custom_button(
            MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y, "Play", screen, btn_font)
        rulesbtn = Custom_button(
            MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y + 100, "Rules", screen, btn_font)
        historybtn = Custom_button(
            MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y + 200, "History", screen, btn_font)
        exitbtn = Custom_button(
            MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y + 300, "Exit", screen, btn_font)

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
