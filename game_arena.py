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
    '''
    This function writes the given text at the given position on given surface applying th e given color and font.

    Parameters
    ----------
    text : string
        This string will be printed.
    screen : a pygame display or surface
        The text wiil be written on this suface.
    position : a pair of values e.g. (x,y)
        The text wiil be written at this position.
    color : rgb coolor code e.g. (255,255,255)
        The text wiil be written in this color.
    font : a pygame font (pg.font.SysFont)
        The text wiil be written in this font.
    new_window : a boolean value, optional
        This parameter wiil determine whether the text wil be printed in a new window or current window. 
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
    
    def __init__(self, x, y, text, screen, font, width = 200, height = 70):
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
    '''
    This class contains all properties of a chess board.

    Properties:

        1. initial_pattern: this parameter holds the position of pieces at the start of the match.
        2. rows: n(rows) on board
        3. columns: n(columns) on board
        4. cell_width: width of each cell on surface
        5. cell_height: height of each cell on surface
        6. screen: where the board will be printed
        7. restricted_cell: holds the (row, column) value of restricted cells

    Methods:

        1. draw_empty_board(): this method draws an empty board with no piece on given surface
        2. initiate_board_pieces(): this method initiates all the sprite instances of different types of pieces

    '''

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

        pg.draw.circle(screen, self.color, self.center, PIECE_RADIUS)

    def update_piece_position(self, row, column):

        self.row_prev, self.column_prev = self.row, self.column
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
        14. ai_selected: a ChessPiece object, or any of it's child class object.
                this varaible holds currenlty selected piece by ai bot.

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
        border = []
        for column in range(self.board.columns + 2):
            border.append("=")
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

        # print("here 3")
        self.valid_moves = []
        tempr = self.already_selected.row
        tempc = self.already_selected.column
        # print(tempr, tempc)

        # finding valid moves in upwards direction
        tempr -= 1
        while tempr >= 0:

            # stores current row and column
            thispos = self.current_board_status[tempr][tempc]
            # if finds any piece, no move left in this direction anymore
            if thispos == "a" or thispos == "d" or thispos == "k":
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
            if thispos == "a" or thispos == "d" or thispos == "k":
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
            if thispos == "a" or thispos == "d" or thispos == "k":
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
            if thispos == "a" or thispos == "d" or thispos == "k":
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

        # first setting all cells as empty cells, then making change where necessary
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
        border = []
        for column in range(self.board.columns + 2):
            border.append("=")
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

        # print(self.current_board_status)

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
                # print(self.king_captured)

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

    def blockade_check(self):

        pass

    def match_finished(self):
        '''
        This method displays necessary messages when the match finishes.

        Returns
        -------
        None.

        '''

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
                            # manager.show_valid_moves()
                            # print("Added")
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
                                # manager.show_valid_moves()
                                # print("Added")
                        break

            if not done:
                # a valid move was selected for previously selected piece, so it will move to that new cell position
                for ind, pos in enumerate(self.valid_moves_positions):
                    if (msx >= pos[0] - PIECE_RADIUS) and (msx < pos[0] + PIECE_RADIUS):
                        if (msy >= pos[1] - PIECE_RADIUS) and (msy < pos[1] + PIECE_RADIUS):
                            # updating piece's position
                            self.already_selected.update_piece_position(
                                self.valid_moves[ind][0], self.valid_moves[ind][1])
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

        # updating piece's position
        self.already_selected = piece
        self.already_selected.update_piece_position(row, column)
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


    def turn_msg(self):
        '''
        This method shows message saying whose turn it is now.

        Returns
        -------
        None.

        '''

        if self.turn:
            write_text("Attacker's Turn", self.screen, (400, BOARD_TOP + self.board.rows*CELL_HEIGHT + 50), white,
                       pg.font.SysFont("Arial", 30), False)
        else:
            write_text("Defender's Turn", self.screen, (400, BOARD_TOP + self.board.rows*CELL_HEIGHT + 50), white,
                       pg.font.SysFont("Arial", 30), False)


class AI_manager:

    def __init__(self, manager, screen):

        self.manager = manager
        self.screen = screen

    def move(self):

        current_board = []
        rows = self.manager.board.rows
        columns = self.manager.board.columns

        '''
        creating patten such as
        [['x', '.', '.', 'a1', 'a2', 'a3', 'a4', 'a5', '.', '.', 'x'], 
         ['.', '.', '.', '.', '.', 'a6', '.', '.', '.', '.', '.'], 
         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
         ['a7', '.', '.', '.', '.', 'd1', '.', '.', '.', '.', 'a8'],
         ['a9', '.', '.', '.', 'd2', 'd3', 'd4', '.', '.', '.', 'a10'], 
         ['a11', 'a12', '.', 'd5', 'd6', 'k', 'd7', 'd8', '.', 'a13', 'a14'],
         ['a15', '.', '.', '.', 'd9', 'd10', 'd11', '.', '.', '.', 'a16'], 
         ['a17', '.', '.', '.', '.', 'd12', '.', '.', '.', '.', 'a18'],
         ['.', '.', '.', '.', '.', '.', '.', '.', '.', '.', '.'], 
         ['.', '.', '.', '.', '.', 'a19', '.', '.', '.', '.', '.'], 
         ['x', '.', '.', 'a20', 'a21', 'a22', 'a23', 'a24', '.', '.', 'x']]
        '''

        for row in range(rows):
            one_row = []
            for column in range(columns):
                if (row == 0 and column == 0) or (row == 0 and column == columns-1) or (row == rows-1 and column == 0) or (row == rows-1 and column == columns-1):
                    # restricted cells (0,0),(0,n-1),(n-1,0),(n-1,n-1) for a n by n board
                    one_row.append("x")
                else:
                    one_row.append(".")
            current_board.append(one_row)

        for piece in All_pieces:
            current_board[piece.row][piece.column] = piece.pid

        # find all possible valid move and return -> list[piece, (pair of indices)]
        moves = self.find_all_possible_valid_moves(current_board, True)
        # select the best move. implement algorithm here
        piece, best_move = self.find_best_move(current_board, moves)
        # print(best_move)
        row, col = best_move  # change

        # perform the move
        self.manager.ai_move_manager(piece, row, col)

    def find_all_possible_valid_moves(self, board_status_at_this_state, fake_turn):

        valid_moves = []
        # needs a list of pair containing the fake pos of pieces at current fake state
        piece_pos_this_state = []
        for row_ind, row in enumerate(board_status_at_this_state):
            for col_ind, column in enumerate(row):
                if column != "." or column != "x":
                    piece_pos_this_state.append((column, (row_ind, col_ind)))

        for each in piece_pos_this_state:
            piece = each[0]
            if (fake_turn and not piece[0] == "a") or (not fake_turn and piece[0] == "a"):
                continue
            # print("here 3")
            tempr = each[1][0]
            tempc = each[1][1]
            # print(tempr, tempc)

            # finding valid moves in upwards direction
            tempr -= 1
            while tempr >= 0:

                # stores current row and column
                thispos = board_status_at_this_state[tempr][tempc][0]
                # if finds any piece, no move left in this direction anymore
                if thispos == "a" or thispos == "d" or thispos == "k":
                    break
                else:
                    # this part is commented out because so far ai is only attacker and this part checks both 'a' or 'd'
                    # # if selected piece is king, only one move per direction is allowed
                    if piece == "k":
                        if tempr < each[1][0] - 1 or tempr > each[1][0] + 1:
                            break
                        # valid_moves.append((piece, (tempr, tempc)))
                        valid_moves.append(
                            (piece_pid_map[piece], (tempr, tempc)))
                    else:
                        # "." means empty cell
                        if thispos == ".":
                            # valid_moves.append((piece, (tempr, tempc)))
                            valid_moves.append(
                                (piece_pid_map[piece], (tempr, tempc)))

                tempr -= 1

            tempr = each[1][0]
            tempc = each[1][1]

            # finding valid moves in downwards direction
            tempr += 1
            while tempr < self.manager.board.rows:

                # stores current row and column
                thispos = board_status_at_this_state[tempr][tempc][0]
                # if finds any piece, no move left in this direction anymore
                if thispos == "a" or thispos == "d" or thispos == "k":
                    break
                else:
                    # # if selected piece is king, only one move per direction is allowed
                    if piece == "k":
                        if tempr < each[1][0] - 1 or tempr > each[1][0] + 1:
                            break
                        # valid_moves.append((piece, (tempr, tempc)))
                        valid_moves.append(
                            (piece_pid_map[piece], (tempr, tempc)))
                    else:
                        # "." means empty cell
                        if thispos == ".":
                            # valid_moves.append((piece, (tempr, tempc)))
                            valid_moves.append(
                                (piece_pid_map[piece], (tempr, tempc)))

                tempr += 1

            tempr = each[1][0]
            tempc = each[1][1]

            # finding valid moves in left direction
            tempc -= 1
            while tempc >= 0:

                # stores current row and column
                thispos = board_status_at_this_state[tempr][tempc][0]
                # if finds any piece, no move left in this direction anymore
                if thispos == "a" or thispos == "d" or thispos == "k":
                    break
                else:
                    # # if selected piece is king, only one move per direction is allowed
                    if piece == "k":
                        if tempc < each[1][1] - 1 or tempc > each[1][1] + 1:
                            break
                        # valid_moves.append((piece, (tempr, tempc)))
                        valid_moves.append(
                            (piece_pid_map[piece], (tempr, tempc)))
                    else:
                        # "." means empty cell
                        if thispos == ".":
                            # valid_moves.append((piece, (tempr, tempc)))
                            valid_moves.append(
                                (piece_pid_map[piece], (tempr, tempc)))

                tempc -= 1

            tempr = each[1][0]
            tempc = each[1][1]

            # finding valid moves in right direction
            tempc += 1
            while tempc < self.manager.board.columns:

                # stores current row and column
                thispos = board_status_at_this_state[tempr][tempc][0]
                # if finds any piece, no move left in this direction anymore
                if thispos == "a" or thispos == "d" or thispos == "k":
                    break
                else:
                    # # if selected piece is king, only one move per direction is allowed
                    if piece == "k":
                        if tempc < each[1][1] - 1 or tempc > each[1][1] + 1:
                            break
                        # valid_moves.append((piece, (tempr, tempc)))
                        valid_moves.append(
                            (piece_pid_map[piece], (tempr, tempc)))
                    else:
                        # "." means empty cell
                        if thispos == ".":
                            # valid_moves.append((piece, (tempr, tempc)))
                            valid_moves.append(
                                (piece_pid_map[piece], (tempr, tempc)))

                tempc += 1

        return valid_moves

    def king_mobility():
        pass

    def king_sorrounded():
        pass

    def evaluate(turn):
        #     weight_king_pos=[[200 ,1   ,20  ,20  ,20  ,20  ,20  ,1   ,200 ],
        # 	[1   ,1   ,8   ,8   ,8   ,8   ,8   ,1   ,1   ],
        # 	[20  ,8   ,4   ,4   ,4   ,4   ,4   ,8   ,20  ],
        # 	[20  ,8   ,4   ,2   ,2   ,2   ,4   ,8   ,20  ],
        # 	[20  ,8   ,4   ,2   ,0   ,2   ,4   ,8   ,20  ],
        # 	[20  ,8   ,4   ,2   ,2   ,2   ,4   ,8   ,20  ],
        # 	[20  ,8   ,4   ,4   ,4   ,4   ,4   ,8   ,20  ],
        # 	[1   ,1   ,8   ,8   ,8   ,8   ,8   ,1   ,1   ],
        # 	[200 ,1   ,20  ,20  ,20  ,20  ,20  ,1   ,200 ] ]

        #     weight_king_mobility=5

        #     weight_king_sorrounded=50

        #     score=0

        #     if boardstate.getwinner()==player:
        #         score+=10000
        #         return score

        #     elif boardstate.getwinner()==opponet:
        #         score-=10000
        #         return score

        #     for row_index,row in enumerate (fake_board):
        #          for column_index,col in enumerate(row):
        #              if(col=='k'):
        #                  r=row,c=col
        #                  break

        #     if turn==True:
        #         score+=attacker
        #         score-=defender
        #         score+=weight_king_pos[r][c]

        #     else:
        #         score+=defender
        #         score-=attacker
        #         score-=weight_king_pos[r][c]
        return 50

    def fake_move(self, fake_board, commited_move):
        # fake board=current state fake board, commited move=the move to be executed
        for row_index, row in enumerate(fake_board):
            f = True
            for column_index, col in enumerate(row):
                if(commited_move[0].pid == col):
                    col = '.'
                    f = False
                    break

            if not f:
                break

        fake_board[commited_move[1][0]][commited_move[1]
                                        [0]] = commited_move[0].pid

        fake_board_with_border = []

        one_row = []
        for column in range(len(fake_board[0])+2):
            one_row.append("=")
        fake_board_with_border.append(one_row)

        for row in fake_board:
            one_row = ["="]
            for column in row:
                one_row.append(column)
            one_row.append("=")
            fake_board_with_border.append(one_row)

        one_row = []
        for column in range(len(fake_board[0])+2):
            one_row.append("=")
        fake_board_with_border.append(one_row)

        self.fake_capture_check(fake_board_with_border, commited_move)

        return fake_board_with_border

    def minimax(self, fake_board, alpha, beta, max_depth, turn):

        bestvalue = -10000000
        moves = self.find_all_possible_valid_moves(
            fake_board, True)  # True attacker ,False Defender
        if(max_depth == 0):  # or boardstate.gameOver()
            # return self.evaluate(fake_board)
            return 50

        # list of all pieces corresponding at this state fake board
        '''fake board is copied into current board'''

        current_board = []
        for row in range(len(fake_board)):
            one_row = []
            for column in range(len(fake_board[0])):
                one_row.append(".")
            current_board.append(one_row)

        for row_index, row in enumerate(fake_board):
            for col_index, column in enumerate(fake_board):
                current_board[row_index][col_index] = column

        if(turn == True):  # attacker  maximizer
            bestvalue = -10000000
            for i in moves:
                tmp_fake_board = self.fake_move(current_board, i)
                value = self.minimax(tmp_fake_board, alpha,
                                     beta, max_depth-1, False)
                bestvalue = max(value, bestvalue)
                alpha = max(alpha, value)
                if(beta <= alpha):
                    break

        else:  # defender minimizer
            bestvalue = 10000000
            for i in moves:
                tmp_fake_board = self.fake_move(current_board, i)
                value = self.minimax(tmp_fake_board, alpha,
                                     beta, max_depth-1, True)
                bestvalue = min(value, bestvalue)
                beta = min(beta, value)
                if(beta <= alpha):
                    break

        return bestvalue

    def strategy(self, current_board, moves):

        bestvalue = -1000000  # value to calcaute the move with best minimax value
        max_depth = 3
        # True attacker ,False Defender  #moves =(piece_object,(row,col))
        moves = self.find_all_possible_valid_moves(current_board, True)

        for i in moves:   # iterate all possible valid moves and their corersponding min max value
            fake_board = self.fake_move(current_board, i)
            # print(fake_board)
            value = self.minimax(fake_board, -10000000,
                                 10000000, max_depth-1, True)
            if(value > bestvalue):
                bestmove = i
                bestvalue = value

        return bestmove

    def find_best_move(self, current_board, moves):

        best_move = self.strategy(current_board, moves)

        return best_move

    def fake_capture_check(self, fake_board_with_border, move):
        '''
        This method contains capture related logics.

        Returns
        -------
        None.

        '''
        # storing current piece's type and index
        ptype, prow, pcol = move[0].pid[0], move[1][0], move[1][1]

        # indices of sorrounding one hop cells and two hops cells.
        sorroundings = [(prow, pcol+1), (prow, pcol-1),
                        (prow-1, pcol), (prow+1, pcol)]
        two_hop_away = [(prow, pcol+2), (prow, pcol-2),
                        (prow-2, pcol), (prow+2, pcol)]

        captured_pieces = []
        # iterating over each neighbour cells and finding out if the piece of this cell is captured or not
        for pos, item in enumerate(sorroundings):

            captured = False
            # currently selected cell's piece, if any
            opp = fake_board_with_border[item[0]][item[1]][0]
            oppid = fake_board_with_border[item[0]][item[1]]
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
                # self.king_capture_check(item[0], item[1])
                # print(self.king_captured)
                pass

            elif ptype != opp:
                # neghbour cell's piece is of different type
                if ptype == "a" and (ptype == opp2 or opp2 == "x"):
                    # a-d-a or a-d-res_cell situation
                    for piece in All_pieces:
                        if piece.pid == oppid:
                            captured = True
                            captured_pieces.append(piece)
                            break

                elif ptype != "a" and opp2 != "a" and opp2 != "=" and opp == "a":
                    # d-a-d or k-a-d or d-a-k or d-a-res_cell or k-a-res_cell situation
                    for piece in All_pieces:
                        if piece.pid == oppid:
                            captured = True
                            captured_pieces.append(piece)
                            break
        # if self.king_captured:
        #     self.finish = True

        # need to return captured pieces to caller function
        # then must remove them from updated fake board status
        # could be done here too
        # needs to check king capture event
        # should I flag it or not??
        # is captured flag useless??

    def fake_king_capture_check(self, fake_board_with_border, kingr, kingc):
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
        front = fake_board_with_border[kingr][kingc+1][0]
        back = fake_board_with_border[kingr][kingc-1][0]
        up = fake_board_with_border[kingr-1][kingc][0]
        down = fake_board_with_border[kingr+1][kingc][0]

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

    # intializing some needed intances
    match_specific_global_data()
    chessboard = ChessBoard(screen)
    chessboard.draw_empty_board()
    chessboard.initiate_board_pieces()
    manager = Game_manager(screen, chessboard)
    if mode == 1:
        bot = AI_manager(manager, screen)

    tafle = True
    game_started = False
    while tafle:
        write_text("Play Vikings Chess", screen, (20, 20), (255, 255, 255),
                   pg.font.SysFont("Arial", 40))
        backbtn = Custom_button(750, 20, "Back", screen,
                                pg.font.SysFont("Arial", 30))
        newgamebtn = Custom_button(
            525, 20, "New Game", screen, pg.font.SysFont("Arial", 30))


        if backbtn.draw_button():
            pg.mixer.Sound.play(pg.mixer.Sound(click_snd))
            main()

        if newgamebtn.draw_button():
            game_started = True
            match_specific_global_data()
            chessboard = ChessBoard(screen)
            chessboard.draw_empty_board()
            chessboard.initiate_board_pieces()
            manager = Game_manager(screen, chessboard)
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

        if game_started and mode == 1 and manager.turn:
            # time.sleep(1)
            bot.move()
        for piece in All_pieces:
            piece.draw_piece(screen)

        # print(manager.valid_moves)

        manager.show_valid_moves()
        if manager.finish:
            manager.match_finished()
        else:
            manager.turn_msg()
        pg.display.update()
        # if manager.turn:
        #     time.sleep(1)


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

        # click = False

        screen.blit(GAME_ICON_resized, (icon_rect))
        pg.display.update()


if __name__ == "__main__":
    main()
