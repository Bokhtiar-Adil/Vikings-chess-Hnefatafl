import os
import sys
import pygame as pg
import time


WINDOW_HEIGHT = 800
WINDOW_WIDTH = 1000
GAME_NAME = TITLE = "VIKINGS_CHESS"
GAME_ICON = pg.image.load("images/vh.jpg")
MAIN_MENU_TOP_BUTTON_x = 400
MAIN_MENU_TOP_BUTTON_y = 400
BOARD_TOP = 200
BOARD_LEFT = 125
CELL_WIDTH = 50
CELL_HEIGHT = 50
PIECE_RADIUS = 20
VALID_MOVE_INDICATOR_RADIUS = 10
SETTINGS_TEXT_GAP_VERTICAL = 50
SETTINGS_TEXT_GAP_HORIZONTAL = 100

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
win_snd_1 = os.path.join("sounds", "win_1.wav")
lose_snd_1 = os.path.join("sounds", "lose_1.wav")

clicked = False


def write_text(text, screen, position, color, font, new_window=True):
    '''
    This function writes the given text at the given position on given surface applying th e given color and font.

    Parameters
    ----------
    text : string
        This string will be #printed.
    screen : a pygame display or surface
        The text wiil be written on this suface.
    position : a pair of values e.g. (x,y)
        The text wiil be written at this position.
    color : rgb coolor code e.g. (255,255,255)
        The text wiil be written in this color.
    font : a pygame font (pg.font.SysFont)
        The text wiil be written in this font.
    new_window : a boolean value, optional
        This parameter wiil determine whether the text wil be #printed in a new window or current window. 
        If the former, all current text and graphics on this surface will be overwritten with background color.
        The default is True.

    Returns
    -------
    None.

    '''

    if new_window:
        screen.fill(bg2)
    txtobj = font.render(text, True, (255, 255, 255))
    txtrect = txtobj.get_rect()
    txtrect.topleft = position
    screen.blit(txtobj, txtrect)


class Custom_button:

    '''
    This class holds the ncessary part of a custom button operation.


    '''

    button_col = (26, 117, 255)
    hover_col = red
    click_col = (50, 150, 255)
    text_col = yellow

    def __init__(self, x, y, text, screen, font, width=200, height=70):
        self.x = x
        self.y = y
        self.text = text
        self.screen = screen
        self.font = font
        self.width = width
        self.height = height

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

        # add text to button
        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.screen.blit(text_img, (self.x + int(self.width / 2) -
                                    int(text_len / 2), self.y + 15))
        return action


class ChessBoard:
    '''
    This class contains all properties of a chess board.

    Properties:

        1. initial_pattern: this parameter holds the position of pieces at the start of the match.
        2. rows: n(rows) on board
        3. columns: n(columns) on board
        4. cell_width: width of each cell on surface
        5. cell_height: height of each cell on surface
        6. screen: where the board will be #printed
        7. restricted_cell: holds the (row, column) value of restricted cells

    Methods:

        1. draw_empty_board(): this method draws an empty board with no piece on given surface
        2. initiate_board_pieces(): this method initiates all the sprite instances of different types of pieces

    '''

    def __init__(self, screen, board_size="large"):

        # board size large means 11x11, small measn 9x9
        self.initial_pattern11 = ["x..aaaaa..x",
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

        self.initial_pattern9 = ["x..aaa..x",
                                 "....a....",
                                 ".........",
                                 "a..ddd..a",
                                 "aa.dcd.aa",
                                 "a..ddd..a",
                                 ".........",
                                 "....a....",
                                 "x..aaa..x"]

        if board_size == "large":
            self.initial_pattern = self.initial_pattern11
        else:
            self.initial_pattern = self.initial_pattern9

        self.rows = len(self.initial_pattern)
        self.columns = len(self.initial_pattern[0])
        self.cell_width = CELL_WIDTH
        self.cell_height = CELL_HEIGHT
        self.screen = screen
        self.restricted_cells = [(0, 0), (0, self.columns-1), (int(self.rows/2), int(
            self.columns/2)), (self.rows-1, 0), (self.rows-1, self.columns-1)]

    def draw_empty_board(self):
        '''
        This method draws an empty board with no piece on given surface

        Returns
        -------
        None.

        '''

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
            write_text(str(row), self.screen, (BOARD_LEFT - 30, BOARD_TOP + row*CELL_HEIGHT +
                       PIECE_RADIUS), (255, 255, 255), pg.font.SysFont("Arial", 15), False)
            write_text(str(row), self.screen, (BOARD_LEFT + row*CELL_WIDTH +
                       PIECE_RADIUS, BOARD_TOP - 30), (255, 255, 255), pg.font.SysFont("Arial", 15), False)
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
        '''
        This method initiates all the sprite instances of different types of pieces

        Returns
        -------
        None.

        '''
        att_cnt, def_cnt = 1, 1
        # for more effective use, this dict maps piece ids and pieces -> {pid : piece}
        global piece_pid_map
        piece_pid_map = {}

        for row in range(self.rows):
            for column in range(self.columns):
                if self.initial_pattern[row][column] == 'a':
                    pid = "a" + str(att_cnt)
                    AttackerPiece(pid, row, column)
                    att_cnt += 1
                elif self.initial_pattern[row][column] == 'd':
                    pid = "d" + str(def_cnt)
                    DefenderPiece(pid, row, column)
                    def_cnt += 1
                elif self.initial_pattern[row][column] == 'c':
                    pid = "k"
                    KingPiece(pid, row, column)
                else:
                    pass

        for piece in All_pieces:
            piece_pid_map[piece.pid] = piece


class ChessPiece(pg.sprite.Sprite):
    '''
    This class contains information about each piece.

    Properties:
        1. pid: holds a unique id for currnet piece instance
        2. row: holds the row index of current piece instance
        3. column: holds the column index of current piece instance
        4. center: center position of corresponding piece instance

    Methods:
        1. update_piece_position(row, column): if the corresponding piece instance is moved, this method updates row and column value of that piece.

    '''

    def __init__(self, pid, row, column):

        pg.sprite.Sprite.__init__(self, self.groups)
        self.pid = pid
        self.row, self.column = (row, column)
        self.center = (BOARD_LEFT + int(CELL_WIDTH / 2) + self.column*CELL_WIDTH,
                       BOARD_TOP + int(CELL_HEIGHT / 2) + self.row*CELL_HEIGHT)

    def draw_piece(self, screen):
        '''
        Draws a piece on board.

        Parameters
        ----------
        screen : surface

        Returns
        -------
        None.

        '''

        pg.draw.circle(screen, self.color, self.center, PIECE_RADIUS)

    def update_piece_position(self, row, column):
        '''
        This updates the position of all pieces on board.

        Parameters
        ----------
        row : row number
        column : column number

        Returns
        -------
        None.

        '''

        self.row, self.column = (row, column)
        self.center = (BOARD_LEFT + int(CELL_WIDTH / 2) + self.column*CELL_WIDTH,
                       BOARD_TOP + int(CELL_HEIGHT / 2) + self.row*CELL_HEIGHT)


class AttackerPiece(ChessPiece):
    '''
    This class holds information about attacker pieces. It's a child of ChessPiece class.

    Properties:
        1. color: a rgb color code. e.g. (255,255,255)
            color of the attacker piece that will be drawn on board.
        2. ptype: type of piece. values:
            i. "a" means attacker
            ii. "d" means defender
            ii. "k" means king.        
        here it's "a".
        3. permit_to_res_sp: a boolean value.
            tells whether the current piece is allowed on a restricted cell or not. here it's false.
    '''

    def __init__(self, pid, row, column):
        ChessPiece.__init__(self, pid, row, column)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.color = ATTACKER_PIECE_COLOR
        self.permit_to_res_sp = False
        self.ptype = "a"


class DefenderPiece(ChessPiece):
    '''
    This class holds information about defender pieces. It's a child of ChessPiece class.

    Properties:
        1. color: a rgb color code. e.g. (255,255,255)
            color of the attacker piece that will be drawn on board.
        2. ptype: type of piece. values:
            i. "a" means attacker
            ii. "d" means defender
            ii. "k" means king.        
        here it's "d".
        3. permit_to_res_sp: a boolean value.
            tells whether the current piece is allowed on a restricted cell or not. here it's false.
    '''

    def __init__(self, pid, row, column):
        ChessPiece.__init__(self, pid, row, column)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.color = DEFENDER_PIECE_COLOR
        self.permit_to_res_sp = False
        self.ptype = "d"


class KingPiece(DefenderPiece):
    '''
    This class holds information about attacker pieces. It's a child of DefenderPiece class.

    Properties:
        1. color: a rgb color code. e.g. (255,255,255)
            color of the attacker piece that will be drawn on board.
        2. ptype: type of piece. values:
            i. "a" means attacker
            ii. "d" means defender
            ii. "k" means king.        
        here it's "k".
        3. permit_to_res_sp: a boolean value.
            tells whether the current piece is allowed on a restricted cell or not. here it's true.
    '''

    def __init__(self, pid, row, column):
        DefenderPiece.__init__(self, pid, row, column)
        pg.sprite.Sprite.__init__(self, self.groups)
        self.color = KING_PIECE_COLOR
        self.permit_to_res_sp = True
        self.ptype = "k"


def match_specific_global_data():
    '''
    This function declares and initiates all sprite groups. 

    Global Properties:
        1. All_pieces: a srpite group containing all pieces.
        2. Attacker_pieces: a srpite group containing all attacker pieces.
        3. Defender_pieces: a srpite group containing all defender pieces.
        4. King_pieces: a srpite group containing all king piece.

    Returns
    -------
    None.

    '''

    global All_pieces, Attacker_pieces, Defender_pieces, King_pieces

    All_pieces = pg.sprite.Group()
    Attacker_pieces = pg.sprite.Group()
    Defender_pieces = pg.sprite.Group()
    King_pieces = pg.sprite.Group()

    ChessPiece.groups = All_pieces
    AttackerPiece.groups = All_pieces, Attacker_pieces
    DefenderPiece.groups = All_pieces, Defender_pieces
    KingPiece.groups = All_pieces, Defender_pieces, King_pieces


class Game_manager:
    '''
    This class handles all the events within the game.

    Properties:

        1. screen: a pygame display or surface.
            holds the current screen where the game is played on.
        2. board: a ChessBoard object.
            this board is used in current game.
        3. turn: a boolean value. default is True.
            this value decides whose turn it is - attackers' or defenders'.
        4. king_escape: a boolean value. dafult is false.
            this variable tells whether the king is captured or not.
        5. king_captured: a boolean value. default is false.
            this variable tells whether the king escaped or not.
        6. all_attackers_killed: a boolean value. default is false.
            this variable tells if all attackers are killed or not.
        7. finish: a boolean value. default is false.
            this variable tells whether a match finishing condition is reached or not.
        8. already_selected: a ChessPiece object, or any of it's child class object.
            this varaible holds currenlty selected piece.
        9. is_selected: a boolean value. default is false.
            this variable tells whether any piece is selected or not.
        10. valid_moves: a list of pair. 
            this list contains all the valid move indices- (row, column) of currently selected piece.
        11. valid_moves_positions: a list of pair. 
                this list contains all the valid move pixel positions- (x_pos, y_pos) of currently selected piece.
        12. current_board_status: a list of lists. 
                this holds current positions of all pieces i.e. current board pattern.
        13. current_board_status_with_border: a list of lists. 
                this holds current positions of all pieces i.e. current board pattern along with border index. 
                (this is redundent I know, but, it's needed for avoiding complexity)
        14. mode: 0 means p-vs-p, 1 means p-vs-ai
                this variable holds game mode.
        15. last_move: pair of pairs of indecies - ((prev_row, prev_col), (curr_row, curr_col))
                this variable holds the 'from' and 'to' of last move.
        16. board_size: "large" means 11x11, "small" means 9x9, default is "large"
                this variable holds board sizes.

    Methods:

        1. select_piece(selected_piece): 
            to select a piece.
        2. find_valid_moves(): 
            finds valid moves of selected piece.
        3. show_valid_moves(): 
            draws the indicator of valid moves on board.
        4. deselect(): 
            deselects currently selected piece.
        5. update_board_status(): 
            updates board status after each move.
        6. capture_check(): 
            contains capture related logics.
        7. king_capture_check(): 
            contains caturing-king related logics.
        8. escape_check(): 
            contains king-escape related logics.
        9. attackers_count_check(): 
            counts currently unkilled attacker pieces.
        10. match_finished(): 
                performs necessary tasks when match ends.
        11. mouse_click_analyzer(msx, msy): 
                analyzes current mouse click action and performs necessary functionalites.
        12. turn_msg(): 
                displays info about whose turn it is. 
        13. ai_move_manager(piece, row, column):
                handles ai moves

    '''

    def __init__(self, screen, board, mode, board_size="large"):
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
        self.mode = mode
        self.last_move = None
        self.board_size = board_size

        # initiating current_board_status and current_board_status_with_border.
        # initially board is in initial_pattern
        # appending top border row
        border = []
        for column in range(self.board.columns + 2):
            border.append("=")
        self.current_board_status_with_border.append(border)

        # appending according to initial_pattern
        for row in self.board.initial_pattern:
            bordered_row = ["="]  # to add a left border
            one_row = []
            for column in row:
                one_row.append(column)
                bordered_row.append(column)
            self.current_board_status.append(one_row)
            bordered_row.append("=")  # to add a right border
            self.current_board_status_with_border.append(bordered_row)

        # appending bottom border row
        self.current_board_status_with_border.append(border)

    def select_piece(self, selected_piece):
        '''
        This method selects a piece.

        Parameters
        ----------
        selected_piece : a ChessPiece or it's child class object.
            assigns this piece to already_selected variable.

        Returns
        -------
        None.

        '''

        self.is_selected = True
        self.already_selected = selected_piece
        self.find_valid_moves()

    def find_valid_moves(self):
        '''
        This method finds valid moves of selected piece.

        Returns
        -------
        None.

        '''

        
        self.valid_moves = []
        tempr = self.already_selected.row
        tempc = self.already_selected.column
        

        # finding valid moves in upwards direction
        tempr -= 1
        while tempr >= 0:

            # stores current row and column
            thispos = self.current_board_status[tempr][tempc]
            # if finds any piece, no move left in this direction anymore
            if thispos == "a" or thispos == "d" or thispos == "k" or (thispos == "x" and self.already_selected.ptype != "k"):
                break
            else:
                # if selected piece is king, only one move per direction is allowed
                if self.already_selected.ptype == "k":
                    if tempr < self.already_selected.row - 1 or tempr > self.already_selected.row + 1:
                        break
                    self.valid_moves.append((tempr, tempc))
                else:
                    # "." means empty cell
                    if thispos == ".":
                        self.valid_moves.append((tempr, tempc))

            tempr -= 1

        tempr = self.already_selected.row
        tempc = self.already_selected.column

        # finding valid moves in downwards direction
        tempr += 1
        while tempr < self.board.rows:

            # stores current row and column
            thispos = self.current_board_status[tempr][tempc]
            # if finds any piece, no move left in this direction anymore
            if thispos == "a" or thispos == "d" or thispos == "k" or (thispos == "x" and self.already_selected.ptype != "k"):
                break
            else:
                # if selected piece is king, only one move per direction is allowed
                if self.already_selected.ptype == "k":
                    if tempr < self.already_selected.row - 1 or tempr > self.already_selected.row + 1:
                        break
                    self.valid_moves.append((tempr, tempc))
                else:
                    # "." means empty cell
                    if thispos == ".":
                        self.valid_moves.append((tempr, tempc))

            tempr += 1

        tempr = self.already_selected.row
        tempc = self.already_selected.column

        # finding valid moves in left direction
        tempc -= 1
        while tempc >= 0:

            # stores current row and column
            thispos = self.current_board_status[tempr][tempc]
            # if finds any piece, no move left in this direction anymore
            if thispos == "a" or thispos == "d" or thispos == "k" or (thispos == "x" and self.already_selected.ptype != "k"):
                break
            else:
                # if selected piece is king, only one move per direction is allowed
                if self.already_selected.ptype == "k":
                    if tempc < self.already_selected.column - 1 or tempc > self.already_selected.column + 1:
                        break
                    self.valid_moves.append((tempr, tempc))
                else:
                    # "." means empty cell
                    if thispos == ".":
                        self.valid_moves.append((tempr, tempc))

            tempc -= 1

        tempr = self.already_selected.row
        tempc = self.already_selected.column

        # finding valid moves in right direction
        tempc += 1
        while tempc < self.board.columns:

            # stores current row and column
            thispos = self.current_board_status[tempr][tempc]
            # if finds any piece, no move left in this direction anymore
            if thispos == "a" or thispos == "d" or thispos == "k" or (thispos == "x" and self.already_selected.ptype != "k"):
                break
            else:
                # if selected piece is king, only one move per direction is allowed
                if self.already_selected.ptype == "k":
                    if tempc < self.already_selected.column - 1 or tempc > self.already_selected.column + 1:
                        break
                    self.valid_moves.append((tempr, tempc))
                else:
                    # "." means empty cell
                    if thispos == ".":
                        self.valid_moves.append((tempr, tempc))

            tempc += 1

        # for each (row, column) index of each valid move, corresponding pixel position is stored
        for position in self.valid_moves:
            self.valid_moves_positions.append((BOARD_LEFT + int(CELL_WIDTH / 2) + position[1]*CELL_WIDTH,
                                               BOARD_TOP + int(CELL_HEIGHT / 2) + position[0]*CELL_HEIGHT))

    def show_valid_moves(self):
        '''
        This method draws the indicator of valid moves on board.

        Returns
        -------
        None.

        '''

        # iterating over valid moves positions and drawing them on board
        for index in self.valid_moves_positions:

            pg.draw.circle(self.screen, VALID_MOVE_INDICATOR_COLOR,
                           index, VALID_MOVE_INDICATOR_RADIUS)

    def deselect(self):
        '''
        This method deselects currently selected piece.

        Returns
        -------
        None.

        '''

        self.is_selected = False
        self.already_selected = None
        self.valid_moves = []
        self.valid_moves_positions = []

    def update_board_status(self):
        '''
        This method updates board status after each move.

        Returns
        -------
        None.

        '''

        self.current_board_status = []
        self.current_board_status_with_border = []

        # adding top border row
        border = []
        for column in range(self.board.columns + 2):
            border.append("=")
        self.current_board_status_with_border.append(border)

        # first setting all cells as empty cells, then making changes where necessary
        for row in range(self.board.rows):
            bordered_row = ["="]  # left border
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
            bordered_row.append("=")  # right border
            self.current_board_status_with_border.append(bordered_row)

        # adding bottom border
        self.current_board_status_with_border.append(border)

        # according to each piece's positions, updating corresponding (row, column) value
        for piece in All_pieces:
            self.current_board_status[piece.row][piece.column] = piece.ptype
            # adding an extra 1 because 0th row and 0th column is border
            self.current_board_status_with_border[piece.row +
                                                  1][piece.column+1] = piece.ptype

        # initial pattern set middle cell as empty cell. but, if it is actually an restricted cell.
        # if it doesn't contain king, it's marked as "x'.
        if self.current_board_status[int(self.board.rows/2)][int(self.board.columns/2)] != "k":
            self.current_board_status[int(
                self.board.rows/2)][int(self.board.columns/2)] = "x"
            self.current_board_status_with_border[int(
                self.board.rows/2)+1][int(self.board.columns/2)+1] = "x"
        

    def capture_check(self):
        '''
        This method contains capture related logics.

        Returns
        -------
        None.

        '''
        # storing current piece's type and index
        ptype, prow, pcol = self.already_selected.ptype, self.already_selected.row + \
            1, self.already_selected.column+1

        # indices of sorrounding one hop cells and two hops cells.
        sorroundings = [(prow, pcol+1), (prow, pcol-1),
                        (prow-1, pcol), (prow+1, pcol)]
        two_hop_away = [(prow, pcol+2), (prow, pcol-2),
                        (prow-2, pcol), (prow+2, pcol)]

        # iterating over each neighbour cells and finding out if the piece of this cell is captured or not
        for pos, item in enumerate(sorroundings):

            # currently selected cell's piece, if any
            opp = self.current_board_status_with_border[item[0]][item[1]]
            # if index is 1, which means it's right beside border, which means there's no two-hop cell in thi direction
            # it may overflow the list index, so it will be set as empty cell instead to avoid error
            try:
                opp2 = self.current_board_status_with_border[two_hop_away[pos]
                                                             [0]][two_hop_away[pos][1]]
            except:
                opp2 = "."

            # if next cell is empty or has same type of piece or has border, no capturing is possible
            # if two hop cell is empty, then also no capturing is possible
            if ptype == opp or ptype == "x" or ptype == "=" or opp == "." or opp2 == ".":
                continue

            elif opp == "k":
                # king needs 4 enemies on 4 cardinal points to be captured. so, handled in another function.
                self.king_capture_check(item[0], item[1])
                # #print(self.king_captured)

            elif ptype != opp:
                # neghbour cell's piece is of different type
                if ptype == "a" and (ptype == opp2 or opp2 == "x"):
                    # a-d-a or a-d-res_cell situation
                    for piece in All_pieces:
                        if piece.ptype == opp and piece.row == sorroundings[pos][0]-1 and piece.column == sorroundings[pos][1]-1:
                            pg.mixer.Sound.play(pg.mixer.Sound(kill_snd_1))
                            piece.kill()
                            self.update_board_status()
                            break

                elif ptype != "a" and opp2 != "a" and opp2 != "=" and opp == "a":
                    # d-a-d or k-a-d or d-a-k or d-a-res_cell or k-a-res_cell situation
                    for piece in All_pieces:
                        if piece.ptype == opp and piece.row == sorroundings[pos][0]-1 and piece.column == sorroundings[pos][1]-1:
                            pg.mixer.Sound.play(pg.mixer.Sound(kill_snd_1))
                            piece.kill()
                            self.update_board_status()
                            break
        if self.king_captured:
            self.finish = True
            pg.mixer.Sound.play(pg.mixer.Sound(lose_snd_1))

    def king_capture_check(self, kingr, kingc):
        '''
        This method contains caturing-king related logics.

        Parameters
        ----------
        kingr : integer
            row index of king piece.
        kingc : integer 
            column index of king piece.

        Returns
        -------
        None.

        '''
        # store all four neighbor cells' pieces
        front = self.current_board_status_with_border[kingr][kingc+1]
        back = self.current_board_status_with_border[kingr][kingc-1]
        up = self.current_board_status_with_border[kingr-1][kingc]
        down = self.current_board_status_with_border[kingr+1][kingc]

        # if all four side has attackers or 3-attackers-one-bordercell situation occurs, king is captured
        # all other possible combos are discarded
        if front == "x" or back == "x" or up == "x" or down == "x":
            return

        elif front == "d" or back == "d" or up == "d" or down == "d":
            return

        elif front == "." or back == "." or up == "." or down == ".":
            return

        else:
            self.king_captured = True

    def escape_check(self):
        '''
        This method checks if the king has escaped or not.

        Returns
        -------
        None.

        '''

        # (0,0), (0,n-1), (n-1,0), (n-1,n-1) cells are escape points for king in a n*n board
        if self.current_board_status[0][0] == "k" or self.current_board_status[0][self.board.columns-1] == "k" or self.current_board_status[self.board.rows-1][0] == "k" or self.current_board_status[self.board.rows-1][self.board.columns-1] == "k":
            self.king_escaped = True
            self.finish = True
            pg.mixer.Sound.play(pg.mixer.Sound(win_snd_1))

        else:
            self.king_escaped = False

    def attackers_count_check(self):
        '''
        This method checks if all attackers are killed or not.

        Returns
        -------
        None.

        '''
        # only way attackers would win is by capturing king, so it's not necessary to check defenders' count
        # Attacker_pieces sprite group holds all attackers
        if len(Attacker_pieces) == 0:
            self.all_attackers_killed = True
            self.finish = True
            pg.mixer.Sound.play(pg.mixer.Sound(win_snd_1))


    def match_finished(self):
        '''
        This method displays necessary messages when the match finishes.

        Returns
        -------
        None.

        '''
        consolas = pg.font.SysFont("consolas", 22)
        if self.king_captured:
            if self.mode == 0:
                write_text(">>> KING CAPTURED !! ATTACKERS WIN !!", self.screen, (20, BOARD_TOP - 80), white,
                           consolas, False)
            else:
                write_text(">>> KING CAPTURED !! AI WINS !!", self.screen, (20, BOARD_TOP - 80), white,
                           consolas, False)

        elif self.king_escaped:
            write_text(">>> KING ESCAPED !! DEFENDERS WIN !!", self.screen, (20, BOARD_TOP - 80), white,
                       consolas, False)
            

        elif self.all_attackers_killed:
            write_text(">>> ALL ATTACKERS DEAD !! DEFENDERS WIN !!", self.screen, (20, BOARD_TOP - 80), white,
                       consolas, False)
            

        else:
            pass

    def mouse_click_analyzer(self, msx, msy):
        '''
        This method analyzes a mouse click event. This is the heart of Game_manager class.

        Parameters
        ----------
        msx : integer
            the row index of mouse clicked position.
        msy : integer
            the column index of mouse clicked position.

        Returns
        -------
        None.

        '''
        # if no piece is selected before and the player selects a piece, the valid moves of that piece is displayed
        if not self.is_selected:
            for piece in All_pieces:
                # collidepoint was not working (dunno why...). so, instead, made a custom logic
                # if mouse click position is within a distant of radius of piece from the center of so, it means it is clicked
                # iterates over all pieces to find out which piece satiefies such condition
                if (msx >= piece.center[0] - PIECE_RADIUS) and (msx < piece.center[0] + PIECE_RADIUS):
                    if (msy >= piece.center[1] - PIECE_RADIUS) and (msy < piece.center[1] + PIECE_RADIUS):
                        if (piece.ptype == "a" and self.turn) or (piece.ptype != "a" and not self.turn):
                            self.select_piece(piece)                            
                        break

        elif (self.already_selected.ptype != "a" and self.turn) or (self.already_selected.ptype == "a" and not self.turn):
            # opponent piece is selected, so previously selected piece will be deselected
            self.deselect()

        else:
            # some piece was selected previously
            # gonna check multiple scenerioes serially; if any meets requirement, 'done' flag will stop checking more
            done = False

            for piece in All_pieces:
                if (msx >= piece.center[0] - PIECE_RADIUS) and (msx < piece.center[0] + PIECE_RADIUS):
                    if (msy >= piece.center[1] - PIECE_RADIUS) and (msy < piece.center[1] + PIECE_RADIUS):
                        done = True
                        if piece == self.already_selected:
                            # previously selected piece is selected again, so it will be deselected
                            self.deselect()
                            break
                        else:
                            # some other piece of same side is selected
                            # so previous one will be deselected and current will be selected
                            self.deselect()
                            if (piece.ptype == "a" and self.turn) or (piece.ptype != "a" and not self.turn):
                                self.select_piece(piece)
                        break

            if not done:
                # a valid move was selected for previously selected piece, so it will move to that new cell position
                for ind, pos in enumerate(self.valid_moves_positions):
                    if (msx >= pos[0] - PIECE_RADIUS) and (msx < pos[0] + PIECE_RADIUS):
                        if (msy >= pos[1] - PIECE_RADIUS) and (msy < pos[1] + PIECE_RADIUS):
                            # updating piece's position
                            prev = (self.already_selected.row,
                                    self.already_selected.column)
                            self.already_selected.update_piece_position(
                                self.valid_moves[ind][0], self.valid_moves[ind][1])
                            curr = (self.already_selected.row,
                                    self.already_selected.column)
                            self.last_move = (prev, curr)
                            # updating board status
                            self.update_board_status()
                            # playing a sound effect
                            pg.mixer.Sound.play(pg.mixer.Sound(move_snd_1))
                            # checking if any opponent piece was captured or not
                            self.capture_check()
                            # checking if selected piece is king or not
                            # if it is, then checking if it's escaped or not
                            if self.already_selected.ptype == "k":
                                self.escape_check()
                            # if it was defender's turn, checking if all of the attackers are captured or not
                            if self.already_selected.ptype != "a":
                                self.attackers_count_check()
                            # altering turn; a to d or d to a
                            self.turn = not self.turn
                            done = True
                            break

                self.deselect()

    def ai_move_manager(self, piece, row, column):
        '''
        This function handles functionalities after AI chooses which piece to move

        Parameters
        ----------
        piece : AI's choosen piece
        row : row index
        column : column index

        Returns
        -------
        None.

        '''

        # updating piece's position
        self.already_selected = piece
        prev = (self.already_selected.row, self.already_selected.column)
        self.already_selected.update_piece_position(row-1, column-1)
        curr = (row-1, column-1)
        self.last_move = (prev, curr)
        # updating board status
        self.update_board_status()
        # playing a sound effect
        pg.mixer.Sound.play(pg.mixer.Sound(move_snd_1))
        # self.already_selected = self.ai_selected
        # checking if any opponent piece was captured or not
        self.capture_check()
        # checking if selected piece is king or not
        # if it is, then checking if it's escaped or not
        if self.already_selected.ptype == "k":
            self.escape_check()
        # if it was defender's turn, checking if all of the attackers are captured or not
        if self.already_selected.ptype != "a":
            self.attackers_count_check()
        # altering turn; a to d or d to a
        self.turn = not self.turn
        self.deselect()

    def turn_msg(self, game_started):
        '''
        This method shows message saying whose turn it is now.

        Returns
        -------
        None.

        '''
        consolas = pg.font.SysFont("consolas", 22)
        if not game_started:
            if self.mode == 0:
                write_text(">>> Click 'New Game' to start a new game.", self.screen,
                           (20, BOARD_TOP - 80), white, consolas, False)
            else:
                write_text(">>> Click 'New Game' to start a new game. AI is attacker and you are defender.", self.screen,
                           (20, BOARD_TOP - 80), white, consolas, False)

        elif self.mode == 0 and self.turn:
            write_text(">>> Attacker's Turn", self.screen, (20, BOARD_TOP - 80), white,
                       consolas, False)

        elif self.mode == 1 and self.turn:
            write_text(">>> AI is thinking...", self.screen, (20, BOARD_TOP - 80), white,
                       consolas, False)

        else:
            write_text(">>> Defender's Turn", self.screen, (20, BOARD_TOP - 80), white,
                       consolas, False)


class AI_manager:

    def __init__(self, manager, screen):

        self.manager = manager
        self.screen = screen

    def move(self):
        '''
        AI uses this function to move a piece.

        Returns
        -------
        None.

        '''

        current_board = []
        rows = self.manager.board.rows
        columns = self.manager.board.columns
        self.rows = rows
        self.columns = columns
        
        # creating pattern such as
        # [['x', '.', '.', 'a1', 'a2', 'a3', 'a4', 'a5', '.', '.', 'x'], 
        #  ['.', '.', '.', '.', '.', 'a6', '.', '.', '.', '.', '.'], 
        #  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
        #  ['a7', '.', '.', '.', '.', 'd1', '.', '.', '.', '.', 'a8'],
        #  ['a9', '.', '.', '.', 'd2', 'd3', 'd4', '.', '.', '.', 'a10'], 
        #  ['a11', 'a12', '.', 'd5', 'd6', 'k', 'd7', 'd8', '.', 'a13', 'a14'],
        #  ['a15', '.', '.', '.', 'd9', 'd10', 'd11', '.', '.', '.', 'a16'], 
        #  ['a17', '.', '.', '.', '.', 'd12', '.', '.', '.', '.', 'a18'],
        #  ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
        #  ['.', '.', '.', '.', '.', 'a19', '.', '.', '.', '.', '.'], 
        #  ['x', '.', '.', 'a20', 'a21', 'a22', 'a23', 'a24', '.', '.', 'x']]        

        current_board = []

        border_row = []
        for column in range(columns+2):
            border_row.append("=")
        current_board.append(border_row)

        for row in range(rows):
            one_row = ["="]
            for column in range(columns):
                one_row.append('.')
            one_row.append("=")
            current_board.append(one_row)

        current_board.append(border_row)

        for piece in All_pieces:
            current_board[piece.row+1][piece.column+1] = piece.pid

        current_board[1][1] = current_board[1][rows] = current_board[rows][1] = current_board[rows][columns] = 'x'
        if current_board[int((self.rows+1)/2)][int((self.columns+1)/2)] != 'k':
            current_board[int((self.rows+1)/2)][int((self.columns+1)/2)] = 'x'

        # find all possible valid move and return -> list[piece, (pair of indices)]
        piece, best_move = self.find_best_move(current_board)
        row, col = best_move

        # perform the move
        self.manager.ai_move_manager(piece, row, col)

    def find_all_possible_valid_moves(self, board_status_at_this_state, fake_turn):
        '''
        AI uses this fucntion to finds out all valid moves of all pieces of a type.

        Parameters
        ----------
        board_status_at_this_state : a 2d matrix
            at any state of evaluation, ai feeds that state's board status here to calculate moves
        fake_turn : boolean
            True - attackers' turn, False - defenders' turn

        Returns
        -------
        valid_moves : a list of pairs - [(str, (int, int))]
            (piece_pid, (row, column))

        '''

        valid_moves = []
        piece_pos_this_state = {}
        for row_ind, row in enumerate(board_status_at_this_state):
            for col_ind, column in enumerate(row):
                if column != "." and column != "x" and column != "=":
                    piece_pos_this_state[column] = (row_ind, col_ind)

        for each in piece_pos_this_state.keys():
            piece = each[0]

            # find moves for a side only if it's their turn
            if (fake_turn and not piece[0] == "a") or (not fake_turn and piece[0] == "a"):
                continue

            tempr = piece_pos_this_state[each][0]
            tempc = piece_pos_this_state[each][1]

            # finding valid moves in upwards direction
            tempr -= 1
            while tempr >= 0:
                # stores current row and column
                thispos = board_status_at_this_state[tempr][tempc][0]
                # if finds any piece, no move left in this direction anymore
                if thispos == "a" or thispos == "d" or thispos == "k" or thispos == "=" or (thispos == "x" and piece != "k"):
                    break
                else:
                    # this part is commented out because so far ai is only attacker and this part checks both 'a' or 'd'
                    # # if selected piece is king, only one move per direction is allowed
                    if piece == "k":
                        if tempr < piece_pos_this_state[each][0] - 1 or tempr > piece_pos_this_state[each][0] + 1:
                            break
                        valid_moves.append(
                            (piece_pid_map[each], (tempr, tempc)))
                    else:
                        # "." means empty cell
                        if thispos == ".":
                            valid_moves.append(
                                (piece_pid_map[each], (tempr, tempc)))

                tempr -= 1

            tempr = piece_pos_this_state[each][0]
            tempc = piece_pos_this_state[each][1]

            # finding valid moves in downwards direction
            tempr += 1
            while tempr < self.manager.board.rows+2:
                # stores current row and column
                thispos = board_status_at_this_state[tempr][tempc][0]
                # if finds any piece, no move left in this direction anymore
                if thispos == "a" or thispos == "d" or thispos == "k" or thispos == "=" or (thispos == "x" and piece != "k"):
                    break
                else:
                    # # if selected piece is king, only one move per direction is allowed
                    if piece == "k":
                        if tempr < piece_pos_this_state[each][0] - 1 or tempr > piece_pos_this_state[each][0] + 1:
                            break
                        valid_moves.append(
                            (piece_pid_map[each], (tempr, tempc)))
                    else:
                        # "." means empty cell
                        if thispos == ".":
                            valid_moves.append(
                                (piece_pid_map[each], (tempr, tempc)))

                tempr += 1

            tempr = piece_pos_this_state[each][0]
            tempc = piece_pos_this_state[each][1]

            # finding valid moves in left direction
            tempc -= 1
            while tempc >= 0:
                # stores current row and column
                thispos = board_status_at_this_state[tempr][tempc][0]
                # if finds any piece, no move left in this direction anymore
                if thispos == "a" or thispos == "d" or thispos == "k" or thispos == "=" or (thispos == "x" and piece != "k"):
                    break
                else:
                    # # if selected piece is king, only one move per direction is allowed
                    if piece == "k":
                        if tempc < piece_pos_this_state[each][1] - 1 or tempc > piece_pos_this_state[each][1] + 1:
                            break
                        valid_moves.append(
                            (piece_pid_map[each], (tempr, tempc)))
                    else:
                        # "." means empty cell
                        if thispos == ".":
                            valid_moves.append(
                                (piece_pid_map[each], (tempr, tempc)))

                tempc -= 1

            tempr = piece_pos_this_state[each][0]
            tempc = piece_pos_this_state[each][1]

            # finding valid moves in right direction
            tempc += 1
            while tempc < self.manager.board.columns+2:
                # stores current row and column
                thispos = board_status_at_this_state[tempr][tempc][0]
                # if finds any piece, no move left in this direction anymore
                if thispos == "a" or thispos == "d" or thispos == "k" or thispos == "=" or (thispos == "x" and piece != "k"):
                    break
                else:
                    # # if selected piece is king, only one move per direction is allowed
                    if piece == "k":
                        if tempc < piece_pos_this_state[each][1] - 1 or tempc > piece_pos_this_state[each][1] + 1:
                            break
                        valid_moves.append(
                            (piece_pid_map[each], (tempr, tempc)))
                    else:
                        # "." means empty cell
                        if thispos == ".":
                            valid_moves.append(
                                (piece_pid_map[each], (tempr, tempc)))

                tempc += 1

        return valid_moves

    def king_mobility(self, fake_board, r, c):
        '''
        THis function checks how many cells can king move at current state

        Parameters
        ----------
        fake_board : board status at that state            
        r : row of king            
        c : column of king            

        Returns
        -------
        score : number of cells king can move to            

        '''
        score = 0
        i = c-1
        while(i != '='):
            if fake_board[r][i] == '.' or fake_board[r][i] == 'x':
                score += 1
            else:
                break
            i -= 1

        i = c+1
        while(i != '='):
            if fake_board[r][i] == '.' or fake_board[r][i] == 'x':
                score += 1
            else:
                break

            i += 1

        i = r-1
        while(i != '='):
            if fake_board[i][c] == '.' or fake_board[i][c] == 'x':
                score += 1
            else:
                break

            i -= 1

        i = r+1
        while(i != '='):
            if fake_board[i][c] == '.' or fake_board[i][c] == 'x':
                score += 1
            else:
                break

            i += 1

        return score

    def king_sorrounded(self, fake_board, r, c):
        '''
        Finds out how many attacekrs are sorrounding king at current board state.

        Parameters
        ----------
        fake_board : board status at that state            
        r : row of king            
        c : column of king   

        Returns
        -------
        score : number of sorrounding attackers.

        '''
        score = 0
        if fake_board[r][c+1][0] == 'a':
            score += 1

        if fake_board[r][c-1][0] == 'a':
            score += 1

        if fake_board[r-1][c][0] == 'a':
            score += 1

        if fake_board[r+1][c][0] == 'a':
            score += 1

        return score

    def evaluate(self, fake_board):
        '''
        This function evaluates current board state using a predefined heuristic value. Heart of AI...

        Parameters
        ----------
        fake_board : current board state.

        Returns
        -------
        score : calculated cost/value of this state.

        '''
        # heuristic values
        weight_pos = 5
        # for 11x11 board
        weight_king_pos_11 = [[10000, 10000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 10000, 10000],
                              [10000, 500, 500, 500, 500, 500,
                              500, 500, 500, 500, 10000],
                              [1000, 500, 200, 200, 200, 200,
                              200, 200, 200, 500, 1000],
                              [1000, 500, 200, 50, 50, 50, 50, 50, 200, 500, 1000],
                              [1000, 500, 200, 50, 10, 10, 10, 50, 200, 500, 1000],
                              [1000, 500, 200, 50, 10, 0, 10, 50, 200, 500, 1000],
                              [1000, 500, 200, 50, 10, 10, 10, 50, 200, 500, 1000],
                              [1000, 500, 200, 50, 50, 50, 50, 50, 200, 500, 1000],
                              [1000, 500, 200, 200, 200, 200,
                              200, 200, 200, 500, 1000],
                              [10000, 500, 500, 500, 500, 500,
                              500, 500, 500, 500, 10000],
                              [10000, 10000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 10000, 10000]]

        # for 9x9 board
        weight_king_pos_9 = [[10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000],
                            [10000, 500, 500, 500, 500, 500, 500, 500, 10000],
                            [10000, 500, 150, 150, 150, 150, 150, 500, 10000],
                            [10000, 500, 150, 30, 30, 30, 150, 500, 10000],
                            [10000, 500, 150, 30, 0, 30, 150, 500, 10000],
                            [10000, 500, 150, 30, 30, 30, 150, 500, 10000],
                            [10000, 500, 150, 150, 150, 150, 150, 500, 10000],
                            [10000, 500, 500, 500, 500, 500, 500, 500, 10000],
                            [10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000, 10000]]

        if self.manager.board_size == "large":
            weight_king_pos = weight_king_pos_11
            weight_attacker = 12  # weight is given because inequal number of attacker and defender
            weight_defender = 24
        else:
            weight_king_pos = weight_king_pos_9
            weight_attacker = 8  # weight is given because inequal number of attacker and defender
            weight_defender = 12

        weight_king_sorrounded = 50000


        attacker = 0  # attacker count

        defender = 0  # defender count

        score = 0

        if self.fake_gameOver(fake_board) == 1:  # if 1 then winner is attacker
            print("c")
            score += 10000000
            return score

        elif self.fake_gameOver(fake_board) == 2:  # if 1 then winner is defender
            score -= 10000000
            return score

        # finding number of attackers and defenders currently on board
        # searching king position
        for row_index, row in enumerate(fake_board):
            for col_index, col in enumerate(row):
                if(col == 'k'):
                    r = row_index
                    c = col_index
                elif(col[0] == 'a'):
                    attacker += 1
                elif(col[0] == 'd'):
                    defender += 1

        # making dynamic heuristic evaluation to prioritize on restricting movement of king when he is close to escaping cells
        if r-3 <= 1 and c-3 <= 1:
            if fake_board[1][2][0] == 'a':
                score += 50000
            if fake_board[2][1][0] == 'a':
                score += 50000
        elif r-3 <= 1 and c+3 >=(self.columns):
            if fake_board[1][self.columns-1][0] == 'a':
                score += 50000
            if fake_board[2][self.columns][0] == 'a':
                score += 50000

        elif r+3 >= (self.rows) and c-3 <= 1:
            if fake_board[self.rows-1][1][0] == 'a':
                score += 50000
            if fake_board[self.rows][2][0] == 'a':
                score += 50000

        elif r+3 >=(self.rows) and c+3 >=(self.columns):
            if fake_board[self.rows][self.columns-1][0] == 'a':
                score += 50000
            if fake_board[self.rows-1][self.columns][0] == 'a':
                score += 50000

        score += (attacker*weight_attacker)
        score -= (defender*weight_defender)
        score -= (weight_pos*weight_king_pos[r-1][c-1])
        score += (weight_king_sorrounded *
                  self.king_sorrounded(fake_board, r, c))

        return score

    def fake_move(self, fake_board, commited_move):
        '''
        This function performs a fake move - AI's imaginative move in alpha-beta pruning

        Parameters
        ----------
        fake_board : this state's board status
        commited_move : which and where to move - (piece.pid, (row, column))

        Returns
        -------
        current_board : board status after commiting that move
        diff : difference of number of uncaptured pieces on both sides        

        '''
        # fake board = current state fake board, commited move=the move to be executed
        # (piece, (where to))
        current_board = []
        for row in range(len(fake_board)):
            one_row = []
            for column in range(len(fake_board[0])):
                one_row.append(".")
            current_board.append(one_row)

        for row_index, row in enumerate(fake_board):
            for col_index, column in enumerate(row):
                current_board[row_index][col_index] = column

        for row_index, row in enumerate(current_board):
            f = True
            for column_index, col in enumerate(row):
                if(commited_move[0].pid == col):
                    current_board[row_index][column_index] = "."
                    f = False
                    break

            if not f:
                break

        # r=int((self.rows+1)/2)
        # c=int((self.columns+1)/2)
        if current_board[int((self.rows+1)/2)][int((self.columns+1)/2)] == ".":
            current_board[int((self.rows+1)/2)][int((self.columns+1)/2)] = 'x'
        current_board[commited_move[1][0]][commited_move[1]
                                           [1]] = commited_move[0].pid

        current_board, king_captured = self.fake_capture_check(
            current_board, commited_move)

        attacker = 0
        defender = 0
        for row_index, row in enumerate(current_board):
            for col_index, col in enumerate(row):
                if(col[0] == 'a'):
                    attacker += 1
                elif(col[0] == 'd'):
                    defender += 1

        if current_board[int((self.rows+1)/2)][int((self.columns+1)/2)] == ".":
            current_board[int((self.rows+1)/2)][int((self.columns+1)/2)] = 'x'

        return current_board, attacker-defender

    def minimax(self, fake_board, alpha, beta, max_depth, turn):
        '''
        Implementation of minimax algorithm.

        Parameters
        ----------
        fake_board : current fake state's board
        alpha : integer
        beta : integer
        max_depth : number of step to dive into the tree
        turn : True for attackers, False for defenders

        Returns
        -------
        bestvalue: the best value evaluated

        '''

        bestvalue = -10000000000
        moves = self.find_all_possible_valid_moves(
            fake_board, turn)  # True attacker ,False Defender

        if max_depth <= 0 or self.fake_gameOver(fake_board) == 1 or self.fake_gameOver(fake_board) == 2:
            return self.evaluate(fake_board)

        # fake board is copied into current board
        current_board = []
        for row in range(len(fake_board)):
            one_row = []
            for column in range(len(fake_board[0])):
                one_row.append(".")
            current_board.append(one_row)

        for row_index, row in enumerate(fake_board):
            for col_index, column in enumerate(row):
                current_board[row_index][col_index] = column

        # commit a move form valid moves list -> evaluate -> pick bestvalue -> alpha-beta computing
        if(turn == True):  # attacker maximizer
            bestvalue = -1000000000000000000
            for i in moves:
                tmp_fake_board, diff = self.fake_move(current_board, i)
                value = self.minimax(tmp_fake_board, alpha,
                                     beta, max_depth-1, False)
                bestvalue = max(value, bestvalue)
                alpha = max(alpha, bestvalue)
                if(beta <= alpha):
                    break

        else:  # defender minimizer
            bestvalue = 1000000000000000000
            for i in moves:
                tmp_fake_board, diff = self.fake_move(current_board, i)
                value = self.minimax(tmp_fake_board, alpha,
                                     beta, max_depth-1, True)
                bestvalue = min(value, bestvalue)
                beta = min(beta, bestvalue)
                if(beta <= alpha):
                    break

        return bestvalue

    def strategy(self, current_board):
        '''
        Brain of AI...

        Parameters
        ----------
        current_board : current state's board

        Returns
        -------
        bestmove : best move for this state to be committed by AI

        '''
        # value to calcaute the move with best minimax value
        bestvalue = -1000000000000000000
        max_depth = 3
        # True attacker,False Defender  
        #moves =(piece_object,(row,col))
        moves = self.find_all_possible_valid_moves(current_board, True)
        c = 0
        diffs = {}
        for i in moves:   # iterate all possible valid moves and their corersponding min max value
            c += 1
            fake_board, diff = self.fake_move(current_board, i)
            value = self.minimax(fake_board, -1000000000000000000,
                                 1000000000000000000, max_depth-1, False)
            print(value, i[1], diff)
            if(value > bestvalue):
                bestmove = i
                bestvalue = value
                diffs[value] = diff

            elif(value == bestvalue and diff > diffs[value]):
                bestmove = i
                bestvalue = value
                diffs[value] = diff

            if(value == bestvalue and (i[1] == (1, 2) or i[1] == (2, 1) or i[1] == (1, self.columns-1) or i[1] == (2, self.columns) or i[1] == (self.rows-1, 1) or i[1] == (self.rows, 2) or i[1] == (self.rows-1, self.columns) or i[1] == (self.rows, self.columns-1))):
                bestmove = i

        return bestmove

    def find_best_move(self, current_board):
        '''
        Calls algoritm.

        Parameters
        ----------
        current_board : current state's board

        Returns
        -------
        best_move : best move for this state to be committed by AI
        
        '''

        best_move = self.strategy(current_board)

        return best_move

    def fake_gameOver(self, fake_board):
        '''
        Check AI's minimax tree traversing has reached game over condition or not.

        Parameters
        ----------
        fake_board : current fake state's board

        Returns
        -------
        int
            1 attacker win, 2 defender win, 3 none win

        '''
        # 1 attacker win,2 defender win,3 none win        
        if self.fake_king_capture_check(fake_board):
            return 1
        elif self.fake_king_escape(fake_board) or self.fake_attacker_cnt(fake_board):
            return 2
        else:
            return 3

    def fake_capture_check(self, fake_board_with_border, move):
        '''
        This method contains capture related logics at any fake state.

        Parameters
        ----------
        fake_board_with_border : current fake state's board
        move : for which move the capture event might happen

        Returns
        -------
        fake_board_with_border : current fake state's board
        king_captured : whether the king is captured or not - True or False

        '''
        # storing current piece's type and index
        ptype, prow, pcol = move[0].pid[0], move[1][0], move[1][1]

        # indices of sorrounding one hop cells and two hops cells.
        sorroundings = [(prow, pcol+1), (prow, pcol-1),
                        (prow-1, pcol), (prow+1, pcol)]
        two_hop_away = [(prow, pcol+2), (prow, pcol-2),
                        (prow-2, pcol), (prow+2, pcol)]
        
        # iterating over each neighbour cells and finding out if the piece of this cell is captured or not
        for pos, item in enumerate(sorroundings):

            king_captured = False
            # currently selected cell's piece, if any
            opp = fake_board_with_border[item[0]][item[1]][0]            
            # if index is 1, which means it's right beside border, which means there's no two-hop cell in thi direction
            # it may overflow the list index, so it will be set as empty cell instead to avoid error
            try:
                opp2 = fake_board_with_border[two_hop_away[pos]
                                              [0]][two_hop_away[pos][1]][0]
            except:
                opp2 = "."

            # if next cell is empty or has same type of piece or has border, no capturing is possible
            # if two hop cell is empty, then also no capturing is possible
            if ptype == opp or ptype == "x" or ptype == "=" or opp == "." or opp2 == ".":
                continue

            elif opp == "k":
                # king needs 4 enemies on 4 cardinal points to be captured. so, handled in another function.
                king_captured = self.fake_king_capture_check(
                    fake_board_with_border)                

            elif ptype != opp:
                # neghbour cell's piece is of different type
                if ptype == "a" and (ptype == opp2 or opp2 == "x"):
                    # a-d-a or a-d-res_cell situation
                    fake_board_with_border[item[0]][item[1]] = '.'                    

                elif ptype != "a" and opp2 != "a" and opp2 != "=" and opp == "a":
                    # d-a-d or k-a-d or d-a-k or d-a-res_cell or k-a-res_cell situation
                    fake_board_with_border[item[0]][item[1]] = '.'                    

        return fake_board_with_border, king_captured
        

    def fake_king_capture_check(self, fake_board_with_border):
        '''
        This method contains caturing-king related logics.

        Parameters
        ----------
        fake_board_with_border : current fake state's board

        Returns
        -------
        bool
            True if captured, False if not.

        '''
        # store all four neighbor cells' pieces             
        for row_index, row in enumerate(fake_board_with_border):
            for col_index, col in enumerate(row):
                if col == "k":                    
                    kingr = row_index
                    kingc = col_index
                    break
        
        front = fake_board_with_border[kingr][kingc+1][0]
        back = fake_board_with_border[kingr][kingc-1][0]
        up = fake_board_with_border[kingr-1][kingc][0]
        down = fake_board_with_border[kingr+1][kingc][0]

        # if all four sides has attackers or a 3-attackers-one-bordercell situation occurs, king is captured
        # all other possible combos are discarded
        if front == "x" or back == "x" or up == "x" or down == "x":
            return False

        elif front == "d" or back == "d" or up == "d" or down == "d":
            return False

        elif front == "." or back == "." or up == "." or down == ".":
            return False

        else:
            return True

    def fake_king_escape(self, fake_board):
        '''
        Checks whether king has escaped in this fake state or not.

        Parameters
        ----------
        fake_board : current fake state's board

        Returns
        -------
        bool
            True if escaped, False if not.

        '''
        r = self.manager.board.rows
        c = self.manager.board.columns
        if fake_board[1][1] == 'k' or fake_board[1][c] == 'k' or fake_board[r][1] == 'k' or fake_board[r][c] == 'k':
            return True

    def fake_attacker_cnt(self, fake_board):
        '''
        Checks whether all attacekrs are captured in this fake state or not.

        Parameters
        ----------
        fake_board : current fake state's board

        Returns
        -------
        bool
            True if all are captured, False if not.

        '''

        for row_index, row in enumerate(fake_board):
            for col_ind, col in enumerate(row):
                if col[0] == "a":
                    return False
        return True


def game_window(screen, mode):
    '''
    This handles game.

    Parameters
    ----------
    screen : surface
        on which surface the game will be played.
    mode : integer
        0 means p vs p, 1 means p vs ai.

    Returns
    -------
    None.

    '''

    # intializing some needed instances
    match_specific_global_data()
    chessboard = ChessBoard(screen)
    chessboard.draw_empty_board()
    chessboard.initiate_board_pieces()
    manager = Game_manager(screen, chessboard, mode)
    if mode == 1:
        bot = AI_manager(manager, screen)

    tafle = True
    game_started = False
    while tafle:
        write_text("Play Vikings Chess", screen, (20, 20), (255, 255, 255),
                   pg.font.SysFont("Arial", 40))
        backbtn = Custom_button(750, 20, "Back", screen,
                                pg.font.SysFont("Arial", 30))

        write_text("Game Settings", screen, (WINDOW_WIDTH - 250, BOARD_TOP), (255, 255, 255),
                   pg.font.SysFont("Arial", 25), False)

        write_text("Board Size:", screen, (WINDOW_WIDTH - 300, BOARD_TOP + SETTINGS_TEXT_GAP_VERTICAL + 10), (255, 255, 255),
                   pg.font.SysFont("Arial", 20), False)

        size9by9btn = Custom_button(WINDOW_WIDTH - 300 + SETTINGS_TEXT_GAP_HORIZONTAL, BOARD_TOP + SETTINGS_TEXT_GAP_VERTICAL, "9x9", screen,
                                    pg.font.SysFont("Arial", 20), width=50, height=50)

        size11by11btn = Custom_button(WINDOW_WIDTH - 300 + SETTINGS_TEXT_GAP_HORIZONTAL*1.7, BOARD_TOP + SETTINGS_TEXT_GAP_VERTICAL, "11x11", screen,
                                      pg.font.SysFont("Arial", 20), width=50, height=50)

        backbtn = Custom_button(750, 20, "Back", screen,
                                pg.font.SysFont("Arial", 30))

        if game_started:
            txt = "Restart Game"
        else:
            txt = 'New Game'

        newgamebtn = Custom_button(
            525, 20, txt, screen, pg.font.SysFont("Arial", 30))

        if backbtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            main()

        if size9by9btn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            game_started = False
            match_specific_global_data()
            chessboard = ChessBoard(screen, "small")
            chessboard.draw_empty_board()
            chessboard.initiate_board_pieces()
            manager = Game_manager(screen, chessboard, mode, "small")
            if mode == 1:
                bot = AI_manager(manager, screen)

        if size11by11btn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            game_started = False
            match_specific_global_data()
            chessboard = ChessBoard(screen, "large")
            chessboard.draw_empty_board()
            chessboard.initiate_board_pieces()
            manager = Game_manager(screen, chessboard, mode, "large")
            if mode == 1:
                bot = AI_manager(manager, screen)

        if newgamebtn.draw_button():
            last_board = manager.board_size
            game_started = True
            match_specific_global_data()
            chessboard = ChessBoard(screen, last_board)
            chessboard.draw_empty_board()
            chessboard.initiate_board_pieces()
            manager = Game_manager(screen, chessboard, mode, last_board)
            if mode == 1:
                bot = AI_manager(manager, screen)

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
                    if mode == 0:
                        manager.mouse_click_analyzer(msx, msy)
                    else:
                        if manager.turn == False:
                            manager.mouse_click_analyzer(msx, msy)
                            chessboard.draw_empty_board()
                            for piece in All_pieces:
                                piece.draw_piece(screen)
                            if manager.finish:
                                manager.match_finished()
                            else:
                                manager.turn_msg(game_started)
                            if manager.last_move is not None:
                                pg.draw.circle(screen, red, (BOARD_LEFT+(manager.last_move[0][1]*CELL_WIDTH)+(
                                    CELL_WIDTH/2), BOARD_TOP+(manager.last_move[0][0]*CELL_HEIGHT)+(CELL_HEIGHT/2)), 5)
                                pg.draw.circle(screen, white, (BOARD_LEFT+(manager.last_move[1][1]*CELL_WIDTH)+(
                                    CELL_WIDTH/2), BOARD_TOP+(manager.last_move[1][0]*CELL_HEIGHT)+(CELL_HEIGHT/2)), 5)
                            pg.display.update()

        if game_started and mode == 1 and manager.turn and not manager.finish:
            
            chessboard.draw_empty_board()
            for piece in All_pieces:
                piece.draw_piece(screen)
            if manager.finish:
                manager.match_finished()
            else:
                manager.turn_msg(game_started)
            if manager.last_move is not None:
                pg.draw.circle(screen, red, (BOARD_LEFT+(manager.last_move[0][1]*CELL_WIDTH)+(CELL_WIDTH/2), BOARD_TOP+(
                    manager.last_move[0][0]*CELL_HEIGHT)+(CELL_HEIGHT/2)), 5)
                pg.draw.circle(screen, white, (BOARD_LEFT+(manager.last_move[1][1]*CELL_WIDTH)+(CELL_WIDTH/2), BOARD_TOP+(
                    manager.last_move[1][0]*CELL_HEIGHT)+(CELL_HEIGHT/2)), 5)
            pg.display.update()
            print("c")
            bot.move()
        for piece in All_pieces:
            piece.draw_piece(screen)        

        manager.show_valid_moves()
        if manager.finish:
            manager.match_finished()
        else:
            manager.turn_msg(game_started)
       
        if manager.last_move is not None:
            pg.draw.circle(screen, red, (BOARD_LEFT+(manager.last_move[0][1]*CELL_WIDTH)+(CELL_WIDTH/2), BOARD_TOP+(
                manager.last_move[0][0]*CELL_HEIGHT)+(CELL_HEIGHT/2)), 5)
            pg.draw.circle(screen, white, (BOARD_LEFT+(manager.last_move[1][1]*CELL_WIDTH)+(CELL_WIDTH/2), BOARD_TOP+(
                manager.last_move[1][0]*CELL_HEIGHT)+(CELL_HEIGHT/2)), 5)
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
        
        msgs = []
        msgs.append("> Turn based game.")
        msgs.append("> Two board sizes: 'large' - 11x11 and 'small' - 9x9.")
        msgs.append("> Center cell and four corner cells are called restricted cells.")
        msgs.append("> Excluding king, a-d count is 24-12 on large board and 16-8 on small board.")
        msgs.append("> All pieces except king can move any number of cells horizontally or vertically.")
        msgs.append("> King can move only one cell at a time.")
        msgs.append("> Only king can move to any of the restricted cells.")
        msgs.append("> Pieces, except king, can be captured by sandwitching them from both sides.")
        msgs.append("> Restricted cells can be used to sandwitch opponent.")
        msgs.append("> Only one opponent piece can be captured in single line with single move.")
        msgs.append("> Multiple pieces can be captured with a single move on cardinal points.")
        msgs.append("> To capture king, attackers need to sorround him on all four cardinal points.")
        msgs.append("> If king is captured, attackers win.")
        msgs.append("> If king escapes to any of the four corner cells, defenders win.")
        msgs.append("> If all attackers are captured, defenders win.")
        
        consolas = pg.font.SysFont("consolas", 20)
        cnt = 0
        for msg in msgs:
            write_text(msg, screen, (20, BOARD_TOP - 80 + 40*cnt), white, consolas, False)
            cnt += 1        

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
            
        msgs = []
        msgs.append("> Originated in Scandinavia.")
        msgs.append("> Developed from a Roman game called Ludus Latrunculorum.")
        msgs.append("> This game flourished until the arrival of chess.")
        msgs.append("> This game was revived back in nineteenth century.")
        
        
        consolas = pg.font.SysFont("consolas", 20)
        cnt = 0
        for msg in msgs:
            write_text(msg, screen, (20, BOARD_TOP - 80 + 40*cnt), white, consolas, False)
            cnt += 1        

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
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_on = False
                pg.quit()

        screen.fill(bg2)
        write_text("Welcome To Vikings Chess!", screen, (250, 20),
                   (255, 255, 255), pg.font.SysFont("Arial", 50))

        btn_font = pg.font.SysFont("Arial", 28)
        gamebtn_1 = Custom_button(
            MAIN_MENU_TOP_BUTTON_x - 110, MAIN_MENU_TOP_BUTTON_y, "Play vs Human", screen, btn_font)
        gamebtn_2 = Custom_button(
            MAIN_MENU_TOP_BUTTON_x + 110, MAIN_MENU_TOP_BUTTON_y, "Play vs AI", screen, btn_font)
        rulesbtn = Custom_button(
            MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y + 100, "Rules", screen, btn_font)
        historybtn = Custom_button(
            MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y + 200, "History", screen, btn_font)
        exitbtn = Custom_button(
            MAIN_MENU_TOP_BUTTON_x, MAIN_MENU_TOP_BUTTON_y + 300, "Exit", screen, btn_font)

        if gamebtn_1.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            game_window(screen, mode=0)

        if gamebtn_2.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            game_window(screen, mode=1)

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

        screen.blit(GAME_ICON_resized, (icon_rect))
        pg.display.update()


if __name__ == "__main__":
    main()