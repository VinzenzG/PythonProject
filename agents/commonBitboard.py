import string
from enum import Enum
from typing import Optional, Callable, Tuple

import numpy
import numpy as np

BoardPiece = np.int8  # The data type (dtype) of the board
NO_PLAYER = BoardPiece(0)  # board[i, j] == NO_PLAYER where the position is empty
PLAYER1 = BoardPiece(1)  # board[i, j] == PLAYER1 where player 1 (player to move first) has a piece
PLAYER2 = BoardPiece(2)  # board[i, j] == PLAYER2 where player 2 (player to move second) has a piece
BoardPiecePrint = str  # dtype for string representation of BoardPiece
NO_PLAYER_PRINT = BoardPiecePrint(' ')
PLAYER1_PRINT = BoardPiecePrint('X')
PLAYER2_PRINT = BoardPiecePrint('O')
moves = np.int8
COUNTM = 0  # count moves
PlayerAction = np.int8  # The column to be played
WIDTH = 7
HEIGHT = 6


# class GameState(Enum):
#     IS_WIN = 1
#     IS_DRAW = -1
#     STILL_PLAYING = 0


# def initialize_game_state(seq: string) -> np.ndarray:
#     """
#     Returns an ndarray, shape (6, 7) and data type (dtype) BoardPiece, initialized to 0 (NO_PLAYER).
#     """
#
#     row, column = 6, 7
#     field = np.ndarray((row, column), BoardPiece())
#     field.fill(NO_PLAYER)
#     return field


def get_moves():
    return COUNTM

def count_moves(mask: int):
    return bin(mask).replace("0b", "").count('1')

def add_first_line():
    return "|==============|"


def add_last_line():
    return "\n|==============|\n|0 1 2 3 4 5 6 |"


def pretty_print_board(board: np.ndarray) -> str:
    """
    Should return `board` converted to a human readable string representation,
    to be used when playing or printing diagnostics to the console (stdout). The piece in
    board[0, 0] should appear in the lower-left. Here's an example output, note that we use
    PLAYER1_Print to represent PLAYER1 and PLAYER2_Print to represent PLAYER2):
    |==============|
    |              |
    |              |
    |    X X       |
    |    O X X     |
    |  O X O O     |
    |  O O X X     |
    |==============|
    |0 1 2 3 4 5 6 |
    """
    result = ""
    my_board = []

    for row in board:
        my_board.append(row)
    my_board = my_board[:: -1]

    result += add_first_line()
    #
    for row in my_board:
        result += "\n"
        result += "|"
        for x in row:
            if str(x) == "0":
                result += "  "
            if str(x) == "1":
                result += PLAYER1_PRINT + " "
            if str(x) == "2":
                result += PLAYER2_PRINT + " "
        result += "|"
    result += add_last_line()

    return result


def key(current: int, mask: int) -> int:
    return current + mask


def can_play(col: int, mask: int) -> bool:
    return (mask & top_mask(col)) == 0


def top_mask(col: int) -> int:
    top_mask = (int(1) << (HEIGHT - 1)) << col * (HEIGHT + 1)
    return top_mask


def bottom_mask(col: int) -> int:
    bottom_mask = int(1) << col * (HEIGHT + 1)
    return bottom_mask


def column_mask(col: int) -> int:
    columnone = (int(1) << HEIGHT) - 1
    column_mask = columnone << col * (HEIGHT + 1)
    return column_mask


def apply_player_action(col: int, current_pos: int, mask: int) -> Tuple[int, int]:
    current_pos ^= mask
    mask |= mask + bottom_mask(col)
    global COUNTM
    COUNTM = count_moves(mask)
    return current_pos, mask


# return current, mask, moves
def play_given_state(game: string) -> Tuple[int, int, int]:
    current = 0
    mask = 0
    for move in game:
        col = (int(move) - 1)
        if col < 0 or col >= WIDTH or not can_play(col, 0) or isWinningMove(col, current, mask): return 0, 0, 0
        current, mask = apply_player_action(col, current, mask)

    return current, mask, len(game)


def isWinningMove(col: int, current: int, mask: int) -> bool:
    pos = current
    pos |= (mask + bottom_mask(col)) & column_mask(col)
    return connected_four(pos)


def string_to_board(pp_board: str) -> np.ndarray:
    """
    Takes the output of pretty_print_board and turns it back into an ndarray.
    This is quite useful for debugging, when the agent crashed and you have the last
    board state as a string.
    """
    row, column = 6, 7
    field = np.ndarray((row, column), BoardPiece())
    lines = pp_board.split('\n')
    lines.pop(0)
    lines.pop(7)
    lines.pop(6)
    x = 0

    for line in lines:
        line = line[1: -1]
        line = line[0: 15: 2]
        y = 0
        for piece in line:

            if piece == " ":
                field[x][y] = NO_PLAYER
            if piece == "X":
                field[x][y] = PLAYER1
            if piece == "O":
                field[x][y] = PLAYER2
            y += 1
        x += 1
    field = field[:: -1]
    return field


# def apply_player_action(
#         board: np.ndarray, action: PlayerAction, player: BoardPiece, copy: bool = False
# ) -> np.ndarray:
#     """
#     Sets board[i, action] = player, where i is the lowest open row. The modified
#     board is returned. If copy is True, makes a copy of the board before modifying it.
#     """
#
#     if copy:
#         cop = board
#
#     for x in range(6):
#         if board[x][action] == NO_PLAYER:
#             board[x][action] = player
#
#             break
#
#     # For counting moves
#     global COUNTM
#     COUNTM = numpy.count_nonzero(board)
#
#     return board


def connected_four(pos: int
                   ) -> bool:
    """
    Returns True if there are four adjacent pieces equal to `player` arranged
    in either a horizontal, vertical, or diagonal line. Returns False otherwise.

    If desired, the last action taken (i.e. last column played) can be provided
    for potential speed optimisation.
    """

    # horizontal
    m = pos & (pos >> (HEIGHT + 1))
    if m & (m >> (2 * (HEIGHT + 1))):
        return True

    # diagonal
    m = pos & (pos >> HEIGHT)
    if m & (m >> (2 * HEIGHT)):
        return True

    # diagonal2
    m = pos & (pos >> HEIGHT + 2)
    if m & (m >> (2 * (HEIGHT + 2))):
        return True

    # vertical
    m = pos & (pos >> 1)
    if m & (m >> 2):
        return True

    return False
