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


class GameState(Enum):
    IS_WIN = 1
    IS_DRAW = -1
    STILL_PLAYING = 0


def initialize_game_state() -> np.ndarray:
    """
    Returns an ndarray, shape (6, 7) and data type (dtype) BoardPiece, initialized to 0 (NO_PLAYER).
    """
    row, column = 6, 7
    field = np.ndarray((row, column), BoardPiece())
    field.fill(NO_PLAYER)
    return field


def get_moves():
    return COUNTM


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


def apply_player_action(
        board: np.ndarray, action: PlayerAction, player: BoardPiece, copy: bool = False
) -> np.ndarray:
    """
    Sets board[i, action] = player, where i is the lowest open row. The modified
    board is returned. If copy is True, makes a copy of the board before modifying it.
    """

    if copy:
        cop = board

    for x in range(6):
        if board[x][action] == NO_PLAYER:
            board[x][action] = player

            break

    # For counting moves
    global COUNTM
    COUNTM = numpy.count_nonzero(board)

    return board


def connected_four(
        board: np.ndarray, player: BoardPiece, last_action: Optional[PlayerAction] = None,
) -> bool:
    """
    Returns True if there are four adjacent pieces equal to `player` arranged
    in either a horizontal, vertical, or diagonal line. Returns False otherwise.

    If desired, the last action taken (i.e. last column played) can be provided
    for potential speed optimisation.
    """
    rows, cols = board.shape
    rows_edge = rows - 3
    cols_edge = cols - 3

    # horizontal check
    for x in range(rows):
        for y in range(cols_edge):
            if np.all(board[x, y:y + 4] == player):
                return True

    # vertical check
    for y in range(cols):
        for x in range(rows_edge):
            if np.all(board[x:x + 4, y] == player):
                return True

    # diagonal left and right
    for x in range(rows_edge):
        for y in range(cols_edge):
            block = board[x:x + 4, y:y + 4]
            if np.all(np.diag(block) == player):
                return True
            if np.all(np.diag(block[::-1, :]) == player):
                return True
    return False


def check_end_state(
        board: np.ndarray, player: BoardPiece, last_action: Optional[PlayerAction] = None,
) -> GameState:
    """
    Returns the current game state for the current `player`, i.e. has their last
    action won (GameState.IS_WIN) or drawn (GameState.IS_DRAW) the game,
    or is play still on-going (GameState.STILL_PLAYING)?
    """
    con = connected_four(board, player, last_action)

    if con:
        return GameState.IS_WIN
    elif (False, True)[COUNTM < 42]:
        return GameState.STILL_PLAYING
    else:
        return GameState.IS_DRAW


class SavedState:
    pass


GenMove = Callable[
    [np.ndarray, BoardPiece, Optional[SavedState]],  # Arguments for the generate_move function
    Tuple[PlayerAction, Optional[SavedState]]  # Return type of the generate_move function
]
