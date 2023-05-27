import os
import sys
import pygame as pg


WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000
GAME_NAME = TITLE = "VIKINGS_CHESS"
GAME_ICON = pg.image.load("images/vh.jpg")
MAIN_MENU_TOP_BUTTON_x = 400
MAIN_MENU_TOP_BUTTON_y = 400
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
blue_zaffre = (8, 24, 168)

ATTACKER_PIECE_COLOR = pink_fuchsia
DEFENDER_PIECE_COLOR = green_teal
KING_PIECE_COLOR = golden
VALID_MOVE_INDICATOR_COLOR = green_neon
BORDER_COLOR = blue_zaffre

GAME_ICON_resized = pg.image.load("images/vh_resized.jpg")

click_snd = os.path.join("sounds", "click_1.wav")
move_snd_1 = os.path.join("sounds", "move_1.mp3")
kill_snd_1 = os.path.join("sounds", "kill_1.mp3")

clicked = False


def write_text(text, screen, position, color, font, new_window=True):
    if new_window:
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
    width = 200
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
        self.restricted_cells = [(0, 0), (0, self.columns-1), (int(self.rows/2), int(
            self.columns/2)), (self.rows-1, 0), (self.rows-1, self.columns-1)]

    def draw_empty_board(self):

        border_top = pg.Rect(BOARD_LEFT - 10, BOARD_TOP -
                             10, self.columns*CELL_WIDTH + 20, 10)
        pg.draw.rect(self.screen, BORDER_COLOR, border_top)
        border_down = pg.Rect(BOARD_LEFT - 10, BOARD_TOP +
                              self.rows*CELL_HEIGHT, self.columns*CELL_WIDTH + 20, 10)
        pg.draw.rect(self.screen, BORDER_COLOR, border_down)
        border_left = pg.Rect(BOARD_LEFT - 10, BOARD_TOP -
                              10, 10, self.rows*CELL_HEIGHT + 10)
        pg.draw.rect(self.screen, BORDER_COLOR, border_left)
        border_right = pg.Rect(BOARD_LEFT+self.columns*CELL_WIDTH,
                               BOARD_TOP - 10, 10, self.rows*CELL_HEIGHT + 10)
        pg.draw.rect(self.screen, BORDER_COLOR, border_right)

        color_flag = True
        for row in range(self.rows):
            for column in range(self.columns):
                cell_rect = pg.Rect(BOARD_LEFT + column * self.cell_width, BOARD_TOP +
                                    row * self.cell_height, self.cell_width, self.cell_height)

                if (row == 0 or row == self.rows-1) and (column == 0 or column == self.columns-1):
                    pg.draw.rect(self.screen, red, cell_rect)
                elif row == int(self.rows / 2) and column == int(self.columns / 2):
                    pg.draw.rect(self.screen, blue_indigo, cell_rect)
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

    def update_piece_position(self, row, column):

        self.row, self.column = (row, column)
        self.center = (BOARD_LEFT + int(CELL_WIDTH / 2) + self.column*CELL_WIDTH,
                       BOARD_TOP + int(CELL_HEIGHT / 2) + self.row*CELL_HEIGHT)


class AttackerPiece(ChessPiece):

    def __init__(self, row, column):
        ChessPiece.__init__(self, row, column)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.color = ATTACKER_PIECE_COLOR
        self.permit_to_res_sp = False
        self.ptype = "a"


class DefenderPiece(ChessPiece):

    def __init__(self, row, column):
        ChessPiece.__init__(self, row, column)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.color = DEFENDER_PIECE_COLOR
        self.permit_to_res_sp = False
        self.ptype = "d"


class KingPiece(DefenderPiece):

    def __init__(self, row, column):
        DefenderPiece.__init__(self, row, column)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.color = KING_PIECE_COLOR
        self.permit_to_res_sp = True
        self.ptype = "k"


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
        self.turn = True
        self.king_escaped = False
        self.king_captured = False
        self.all_attackers_killed = False
        self.finish = False
        self.already_selected = None
        self.is_selected = False
        self.valid_moves = []
        self.valid_moves_positions = []
        self.current_board_status = []
        self.current_board_status_with_border = []

        border = []
        for column in range(self.board.columns + 2):
            border.append("=")
        self.current_board_status_with_border.append(border)

        for row in self.board.initial_pattern:
            bordered_row = ["="]
            one_row = []
            for column in row:
                one_row.append(column)
                bordered_row.append(column)
            self.current_board_status.append(one_row)
            bordered_row.append("=")
            self.current_board_status_with_border.append(bordered_row)

        border = []
        for column in range(self.board.columns + 2):
            border.append("=")
        self.current_board_status_with_border.append(border)

    def select_piece(self, selected_piece):

        self.is_selected = True
        self.already_selected = selected_piece
        self.find_valid_moves()

    def find_valid_moves(self):

        # print("here 3")
        self.valid_moves = []
        tempr = self.already_selected.row
        tempc = self.already_selected.column
        # print(tempr, tempc)
        
        tempr -= 1
        while tempr >= 0:
            
            thispos = self.current_board_status[tempr][tempc]
            if thispos == "a" or thispos == "d" or thispos == "k":
                break
            else:
                if self.already_selected.ptype == "k":
                    if tempr < self.already_selected.row - 1 or tempr > self.already_selected.row + 1:
                        break
                    self.valid_moves.append((tempr, tempc))
                else:
                    if thispos == ".":
                        self.valid_moves.append((tempr, tempc))

            tempr -= 1

        tempr = self.already_selected.row
        tempc = self.already_selected.column

        tempr += 1
        while tempr < self.board.rows:
            
            thispos = self.current_board_status[tempr][tempc]
            if thispos == "a" or thispos == "d" or thispos == "k":
                break
            else:
                if self.already_selected.ptype == "k":
                    if tempr < self.already_selected.row - 1 or tempr > self.already_selected.row + 1:
                        break
                    self.valid_moves.append((tempr, tempc))
                else:
                    if thispos == ".":
                        self.valid_moves.append((tempr, tempc))

            tempr += 1

        tempr = self.already_selected.row
        tempc = self.already_selected.column

        tempc -= 1
        while tempc >= 0:
            
            thispos = self.current_board_status[tempr][tempc]
            if thispos == "a" or thispos == "d" or thispos == "k":
                break
            else:
                if self.already_selected.ptype == "k":
                    if tempc < self.already_selected.column - 1 or tempc > self.already_selected.column + 1:
                        break
                    self.valid_moves.append((tempr, tempc))
                else:
                    if thispos == ".":
                        self.valid_moves.append((tempr, tempc))

            tempc -= 1

        tempr = self.already_selected.row
        tempc = self.already_selected.column

        tempc += 1
        while tempc < self.board.columns:
            
            thispos = self.current_board_status[tempr][tempc]
            if thispos == "a" or thispos == "d" or thispos == "k":
                break
            else:
                if self.already_selected.ptype == "k":
                    if tempc < self.already_selected.column - 1 or tempc > self.already_selected.column + 1:
                        break
                    self.valid_moves.append((tempr, tempc))
                else:
                    if thispos == ".":
                        self.valid_moves.append((tempr, tempc))

            tempc += 1

        for position in self.valid_moves:
            self.valid_moves_positions.append((BOARD_LEFT + int(CELL_WIDTH / 2) + position[1]*CELL_WIDTH,
                                               BOARD_TOP + int(CELL_HEIGHT / 2) + position[0]*CELL_HEIGHT))

    def show_valid_moves(self):

        # print("here 4")
        for index in self.valid_moves:

            # print("here 5")
            indicator_pos = (BOARD_LEFT + int(CELL_WIDTH / 2) + index[1]*CELL_WIDTH,
                             BOARD_TOP + int(CELL_HEIGHT / 2) + index[0]*CELL_HEIGHT)
            pg.draw.circle(self.screen, VALID_MOVE_INDICATOR_COLOR,
                           indicator_pos, VALID_MOVE_INDICATOR_RADIUS)

    def deselect(self):

        self.is_selected = False
        self.already_selected = None
        self.valid_moves = []
        self.valid_moves_positions = []
        Current_piece.empty()

    def update_board_status(self):

        self.current_board_status = []
        self.current_board_status_with_border = []

        border = []
        for column in range(self.board.columns + 2):
            border.append("=")
        self.current_board_status_with_border.append(border)

        for row in range(self.board.rows):
            bordered_row = ["="]
            one_row = []
            for column in range(self.board.columns):
                one_row.append(".")
                bordered_row.append(".")

            if row == 0 or row == self.board.rows - 1:
                one_row[0] = "x"
                one_row[self.board.columns-1] = "x"
                bordered_row[1] = "x"
                bordered_row[self.board.columns] = "x"
            self.current_board_status.append(one_row)
            bordered_row.append("=")
            self.current_board_status_with_border.append(bordered_row)

        border = []
        for column in range(self.board.columns + 2):
            border.append("=")
        self.current_board_status_with_border.append(border)

        for piece in All_pieces:
            self.current_board_status[piece.row][piece.column] = piece.ptype
            self.current_board_status_with_border[piece.row +
                                                  1][piece.column+1] = piece.ptype

        if self.current_board_status[int(self.board.rows/2)][int(self.board.columns/2)] != "k":
            self.current_board_status[int(
                self.board.rows/2)][int(self.board.columns/2)] = "x"
            self.current_board_status_with_border[int(
                self.board.rows/2)+1][int(self.board.columns/2)+1] = "x"

        # print(self.current_board_status)

    def capture_check(self):

        ptype, prow, pcol = self.already_selected.ptype, self.already_selected.row + \
            1, self.already_selected.column+1

        sorroundings = [(prow, pcol+1), (prow, pcol-1),
                        (prow-1, pcol), (prow+1, pcol)]
        two_hop_away = [(prow, pcol+2), (prow, pcol-2),
                        (prow-2, pcol), (prow+2, pcol)]

        # out = False
        for pos, item in enumerate(sorroundings):

            # if self.king_captured:
            #     break
            # print(prow,pcol,item)
            opp = self.current_board_status_with_border[item[0]][item[1]]
            try:
                opp2 = self.current_board_status_with_border[two_hop_away[pos]
                                                             [0]][two_hop_away[pos][1]]
            except:
                opp2 = "."

            if ptype == opp or ptype == "x" or ptype == "=" or opp == "." or opp2 == ".":
                continue

            elif opp == "k":
                self.king_capture_check(item[0], item[1])
                print(self.king_captured)
                # if self.king_captured:
                #     out = True

            elif ptype != opp:
                if ptype == "a" and ptype == opp2:
                    for piece in All_pieces:
                        if piece.ptype == opp and piece.row == sorroundings[pos][0]-1 and piece.column == sorroundings[pos][1]-1:
                            pg.mixer.Sound.play(pg.mixer.Sound(kill_snd_1))
                            piece.kill()
                            self.update_board_status()
                            break

                elif ptype != "a" and opp2 != "a" and opp2 != "=" and opp == "a":
                    for piece in All_pieces:
                        if piece.ptype == opp and piece.row == sorroundings[pos][0]-1 and piece.column == sorroundings[pos][1]-1:
                            pg.mixer.Sound.play(pg.mixer.Sound(kill_snd_1))
                            piece.kill()
                            self.update_board_status()
                            break
        if self.king_captured:
            self.finish = True

    def king_capture_check(self, kingr, kingc):

        front = self.current_board_status_with_border[kingr][kingc+1]
        back = self.current_board_status_with_border[kingr][kingc-1]
        up = self.current_board_status_with_border[kingr-1][kingc]
        down = self.current_board_status_with_border[kingr+1][kingc]

        print(front, back, up, down)

        if front == "x" or back == "x" or up == "x" or down == "x":
            return

        elif front == "d" or back == "d" or up == "d" or down == "d":
            return

        elif front == "." or back == "." or up == "." or down == ".":
            return

        else:
            self.king_captured = True

    def escape_check(self):

        if self.current_board_status[0][0] == "k" or self.current_board_status[0][self.board.columns-1] == "k" or self.current_board_status[self.board.rows-1][0] == "k" or self.current_board_status[self.board.rows-1][self.board.columns-1] == "k":
            self.king_escaped = True
            self.finish = True

        else:
            self.king_escaped = False

    def attackers_count_check(self):

        if len(Attacker_pieces) == 0:
            self.all_attackers_killed = True
            self.finish = True

    def blockade_check(self):

        pass

    def match_finished(self):

        if self.king_captured:
            write_text("KING CAPTURED !! ATTACKERS WIN !!", self.screen, (300, BOARD_TOP + self.board.rows*CELL_HEIGHT + 50), pink_fuchsia,
                       pg.font.SysFont("Arial", 40), False)

        elif self.king_escaped:
            write_text("KING ESCAPED !! DEFENDERS WIN !!", self.screen, (300, BOARD_TOP + self.board.rows*CELL_HEIGHT + 50), green_neon,
                       pg.font.SysFont("Arial", 40), False)

        elif self.all_attackers_dead:
            write_text("ALL ATTACKERS DEAD !! DEFENDERS WIN !!", self.screen, (300, BOARD_TOP + self.board.rows*CELL_HEIGHT + 50), green_neon,
                       pg.font.SysFont("Arial", 40), False)

        else:
            pass

    def mouse_pos_analyzer(self, msx, msy):

        if not self.is_selected:
            for piece in All_pieces:
                if (msx >= piece.center[0] - PIECE_RADIUS) and (msx < piece.center[0] + PIECE_RADIUS):
                    if (msy >= piece.center[1] - PIECE_RADIUS) and (msy < piece.center[1] + PIECE_RADIUS):
                        if (piece.ptype == "a" and self.turn) or (piece.ptype != "a" and not self.turn):
                            self.select_piece(piece)
                            # manager.show_valid_moves()
                            Current_piece.add(piece)
                            # print("Added")
                        break

        elif (self.already_selected.ptype != "a" and self.turn) or (self.already_selected.ptype == "a" and not self.turn):
            self.deselect()

        else:
            done = False
            for piece in All_pieces:
                if (msx >= piece.center[0] - PIECE_RADIUS) and (msx < piece.center[0] + PIECE_RADIUS):
                    if (msy >= piece.center[1] - PIECE_RADIUS) and (msy < piece.center[1] + PIECE_RADIUS):
                        done = True
                        if piece == self.already_selected:
                            self.deselect()
                            break
                        else:
                            self.deselect()
                            if (piece.ptype == "a" and self.turn) or (piece.ptype != "a" and not self.turn):
                                self.select_piece(piece)
                                # manager.show_valid_moves()
                                Current_piece.add(piece)
                                # print("Added")
                        break

            if not done:

                for ind, pos in enumerate(self.valid_moves_positions):
                    if (msx >= pos[0] - PIECE_RADIUS) and (msx < pos[0] + PIECE_RADIUS):
                        if (msy >= pos[1] - PIECE_RADIUS) and (msy < pos[1] + PIECE_RADIUS):
                            self.already_selected.update_piece_position(
                                self.valid_moves[ind][0], self.valid_moves[ind][1])
                            self.update_board_status()
                            pg.mixer.Sound.play(pg.mixer.Sound(move_snd_1))
                            self.capture_check()
                            if self.already_selected.ptype == "k":
                                self.escape_check()
                            if self.already_selected != "a":
                                self.attackers_count_check()
                            self.turn = not self.turn
                            done = True
                            break

                self.deselect()

    def turn_msg(self):

        if self.turn:
            write_text("Attacker's Turn", self.screen, (400, BOARD_TOP + self.board.rows*CELL_HEIGHT + 50), white,
                       pg.font.SysFont("Arial", 30), False)
        else:
            write_text("Defender's Turn", self.screen, (400, BOARD_TOP + self.board.rows*CELL_HEIGHT + 50), white,
                       pg.font.SysFont("Arial", 30), False)


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
        backbtn = Custom_button(750, 20, "Back", screen,
                                pg.font.SysFont("Arial", 30))
        restartbtn = Custom_button(
            525, 20, "Restart", screen, pg.font.SysFont("Arial", 30))

        if backbtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            main()

        if restartbtn.draw_button():
            match_specific_global_data()
            chessboard = ChessBoard(screen)
            chessboard.draw_empty_board()
            chessboard.initiate_board_pieces()
            manager = Game_manager(screen, chessboard)

        chessboard.draw_empty_board()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    tafle = False
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                msx, msy = pg.mouse.get_pos()
                if not manager.finish:
                    manager.mouse_pos_analyzer(msx, msy)

        for piece in All_pieces:
            piece.draw_piece(screen)

        # print(manager.valid_moves)

        manager.show_valid_moves()
        if manager.finish:
            manager.match_finished()
        else:
            manager.turn_msg()
        pg.display.update()


def rules(screen):
    tafle = True
    while tafle:
        write_text("Rules of Viking Chess", screen, (20, 20), (255, 255, 255),
                   pg.font.SysFont("Arial", 40))
        backbtn = Custom_button(750, 20, "Back", screen,
                                pg.font.SysFont("Arial", 30))

        if backbtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            main()

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
                   pg.font.SysFont("Arial", 40))
        backbtn = Custom_button(750, 20, "Back", screen,
                                pg.font.SysFont("Arial", 30))

        if backbtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            main()

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

    icon_rect = GAME_ICON_resized.get_rect(
        center=(500, MAIN_MENU_TOP_BUTTON_y-150))

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
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            game_window(screen)

        if rulesbtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            rules(screen)

        if historybtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            history(screen)

        if exitbtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            game_on = False
            pg.quit()

        # click = False

        screen.blit(GAME_ICON_resized, (icon_rect))
        pg.display.update()


if __name__ == "__main__":
    main()
