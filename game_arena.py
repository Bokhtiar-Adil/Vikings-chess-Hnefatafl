import sys
import pygame as pg


WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000
GAME_NAME = TITLE = "VIKINGS_CHESS"
GAME_ICON = pg.image.load("images/vh.jpg")
MAIN_MENU_TOP_BUTTON_x = 400
MAIN_MENU_TOP_BUTTON_y = 250
BOARD_TOP = 120
BOARD_LEFT = 225
CELL_WIDTH = 50
CELL_HEIGHT = 50
PIECE_RADIUS = 20
VALID_MOVE_INDICATOR_RADIUS = 10


bg = (204, 102, 0)
bg2 = (40, 40, 40)
red = (255, 0, 0)
black = (0, 0, 0)
yellow = (255, 255, 1)
golden = (255, 215, 0)
white = (255, 255, 255)
pink_fuchsia = (255, 0, 255)
green_neon = (15, 255, 80)
green_dark = (2, 48, 32)
green_teal = (0, 128, 128)
blue_indigo = (63, 0, 255)

ATTACKER_PIECE_COLOR = pink_fuchsia
DEFENDER_PIECE_COLOR = green_teal
KING_PIECE_COLOR = blue_indigo
VALID_MOVE_INDICATOR_COLOR = green_neon

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

        # if board_size == "large":

        #     self.initial_pattern = ["x..aaaaa..x",
        #                             ".....a.....",
        #                             "...........",
        #                             "a....d....a",
        #                             "a...ddd...a",
        #                             "aa.ddcdd.aa",
        #                             "a...ddd...a",
        #                             "a....d....a",
        #                             "...........",
        #                             ".....a.....",
        #                             "x..aaaaa..x"]
        self.initial_pattern = ["x..aaaaa..x",
                                ".....a.....",
                                "...........",
                                "a....d....a",
                                "a...ddd...a",
                                "aa.ddcdd.aa",
                                "a...ddd...a",
                                "a....d....a",
                                "...........",
                                ".....a.....",
                                "x..aaaaa..x"]

        self.rows = len(self.initial_pattern)
        self.columns = len(self.initial_pattern[0])
        self.cell_width = CELL_WIDTH
        self.cell_height = CELL_HEIGHT
        self.screen = screen
        self.current_board_status = self.initial_pattern
        self.restricted_cells = [(0, 0), (0, self.columns-1), (int(self.rows/2), int(
            self.columns/2)), (self.rows-1, 0), (self.rows-1, self.columns-1)]

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

    def initiate_board_pieces(self):

        for row in range(self.rows):
            for column in range(self.columns):
                if self.initial_pattern[row][column] == 'a':
                    AttackerPiece(row, column)
                elif self.initial_pattern[row][column] == 'd':
                    DefenderPiece(row, column)
                elif self.initial_pattern[row][column] == 'c':
                    KingPiece(row, column)
                else:
                    pass


class ChessPiece(pg.sprite.Sprite):

    def __init__(self, row, column):

        pg.sprite.Sprite.__init__(self, self.groups)
        self.row, self.column = (row, column)
        self.center = (BOARD_LEFT + int(CELL_WIDTH / 2) + self.column*CELL_WIDTH,
                       BOARD_TOP + int(CELL_HEIGHT / 2) + self.row*CELL_HEIGHT)

    def draw_piece(self, screen):

        pg.draw.circle(screen, self.color, self.center, PIECE_RADIUS)


class AttackerPiece(ChessPiece):

    def __init__(self, row, column):
        ChessPiece.__init__(self, row, column)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.color = ATTACKER_PIECE_COLOR
        self.permit_to_res_sp = False


class DefenderPiece(ChessPiece):

    def __init__(self, row, column):
        ChessPiece.__init__(self, row, column)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.color = DEFENDER_PIECE_COLOR
        self.permit_to_res_sp = False


class KingPiece(DefenderPiece):

    def __init__(self, row, column):
        DefenderPiece.__init__(self, row, column)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.color = KING_PIECE_COLOR
        self.permit_to_res_sp = True


def match_specific_global_data():

    global All_pieces, Attacker_pieces, Defender_pieces, King_pieces, Current_piece

    All_pieces = pg.sprite.Group()
    Attacker_pieces = pg.sprite.Group()
    Defender_pieces = pg.sprite.Group()
    King_pieces = pg.sprite.Group()
    Current_piece = pg.sprite.Group()

    ChessPiece.groups = All_pieces
    AttackerPiece.groups = All_pieces, Attacker_pieces
    DefenderPiece.groups = All_pieces, Defender_pieces
    KingPiece.groups = All_pieces, Defender_pieces, King_pieces


class Game_manager:

    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.attacker_turn = True
        self.defender_turn = False
        self.king_escaped = False
        self.king_captured = False
        self.already_selected = None
        self.is_selected = False
        self.valid_moves = []

    def select_piece(self, selected_piece):

        # print("here 1")
        # print(self.board.current_board_status)
        if not self.is_selected and selected_piece != self.already_selected:
            # print("here 2")
            self.is_selected = True
            self.already_selected = selected_piece
            self.find_valid_moves()
            # self.show_valid_moves()
            # print(self.valid_moves)
            
        elif self.is_selected and selected_piece != self.already_selected:
            self.is_selected = True
            self.already_selected = selected_piece
            self.find_valid_moves()
            # self.show_valid_moves()
            # print(self.valid_moves)
        
        elif self.is_selected:
            self.is_selected = False
            self.already_selected = None
            self.valid_moves = []
        
        # print(self.valid_moves)
            
    def find_valid_moves(self):

        # print("here 3")
        self.valid_moves = []
        tempr = self.already_selected.row
        tempc = self.already_selected.column
        # print(tempr, tempc)

        tempr -= 1
        while tempr >= 0:

            if self.board.current_board_status[tempr][tempc] != ".":
                break
            else:
                if (tempr, tempc) not in self.board.restricted_cells:
                    self.valid_moves.append((tempr, tempc))

            tempr -= 1

        tempr = self.already_selected.row
        tempc = self.already_selected.column

        tempr += 1
        while tempr < self.board.rows:

            if self.board.current_board_status[tempr][tempc] != ".":
                break
            else:
                if (tempr, tempc) not in self.board.restricted_cells:
                    self.valid_moves.append((tempr, tempc))

            tempr += 1

        tempr = self.already_selected.row
        tempc = self.already_selected.column

        tempc -= 1
        while tempc >= 0:

            if self.board.current_board_status[tempr][tempc] != ".":
                break
            else:
                if (tempr, tempc) not in self.board.restricted_cells:
                    self.valid_moves.append((tempr, tempc))

            tempc -= 1

        tempr = self.already_selected.row
        tempc = self.already_selected.column

        tempc += 1
        while tempc < self.board.columns:

            if self.board.current_board_status[tempr][tempc] != ".":
                break
            else:
                if (tempr, tempc) not in self.board.restricted_cells:
                    self.valid_moves.append((tempr, tempc))

            tempc += 1

    def show_valid_moves(self):
        
        # print("here 4")
        for index in self.valid_moves:
            
            # print("here 5")
            indicator_pos = (BOARD_LEFT + int(CELL_WIDTH / 2) + index[1]*CELL_WIDTH,
                           BOARD_TOP + int(CELL_HEIGHT / 2) + index[0]*CELL_HEIGHT)
            pg.draw.circle(self.screen, VALID_MOVE_INDICATOR_COLOR, indicator_pos, VALID_MOVE_INDICATOR_RADIUS)


def game_window(screen):
    
    match_specific_global_data()
    chessboard = ChessBoard(screen)
    chessboard.draw_empty_board()
    chessboard.initiate_board_pieces()
    manager = Game_manager(screen, chessboard)
    
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

        chessboard.draw_empty_board()
        # selected_piece = None

        for event in pg.event.get():            
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    tafle = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                msx, msy = pg.mouse.get_pos()
                for piece in All_pieces:
                    if (msx >= piece.center[0] - PIECE_RADIUS) and (msx <= piece.center[0] + PIECE_RADIUS):
                        if (msy >= piece.center[1] - PIECE_RADIUS) and (msy <= piece.center[1] + PIECE_RADIUS):
                            manager.select_piece(piece)
                            # manager.show_valid_moves()
                            Current_piece.add(piece)
                            # print("Added")
                            break

        for piece in All_pieces:
            piece.draw_piece(screen)
        
        
        manager.show_valid_moves()
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
            game_window(screen)

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
