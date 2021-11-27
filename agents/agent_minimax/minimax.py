import math
from typing import Optional, Tuple

import numpy as np

from agents.common import BoardPiece, SavedState, PlayerAction, PLAYER1, PLAYER2, GameState, check_end_state, NO_PLAYER, \
    apply_player_action

DEPTH = 3
Window = 4
score_dict = {
    1: 0,
    2: 1,
    3: 10,
    4: 100
}

def generate_minimax(
        board: np.ndarray, player: BoardPiece, save_state: Optional[SavedState] = None
) -> Tuple[PlayerAction, Optional[SavedState]]:
    score, action, save_state2 = minimax(board, player, DEPTH, save_state)
    return action, save_state2


def det_score(target_window: np.ndarray, player: BoardPiece) -> float:
    temp = 0
    if np.count_nonzero(target_window == player) == Window:
        temp += score_dict.get(Window)
    elif np.count_nonzero(target_window == player) == Window - 1 and np.count_nonzero(target_window == NO_PLAYER) == 1:
        temp += score_dict.get(Window - 1)
    elif np.count_nonzero(target_window == player) == Window - 2 and np.count_nonzero(target_window == NO_PLAYER) == 2:
        temp += score_dict.get(Window - 1)

    return temp


def score_heuristic(board: np.ndarray, player: BoardPiece) -> float:
    score = 0
    rows, cols = board.shape
    rows_edge = rows - Window + 1
    cols_edge = cols - Window + 1
    score_board = np.ndarray

    # horizontal
    for x in range(rows):
        for y in range(cols_edge):
            target = board[x, y:y + Window]
            score += det_score(target, player)

    # vertical
    for y in range(cols):
        for x in range(rows_edge):
            target = board[x: x + Window, y]
            score += det_score(target, player)

    # diagonal
    for x in range(rows_edge):
        for y in range(cols_edge):
            win_block = board[x:x + Window, y:y + Window] # create a block of four pieces x four pieces
            target = np.diag(win_block)
            score += det_score(target, player)
            target = np.diag(win_block[::-1, :])
            score += det_score(target, player)

    return (score, score * -1)[player == PLAYER1]


def minimax(
        board: np.ndarray,
        player: BoardPiece, depth: int,
        save_state: Optional[SavedState] = None
) -> Tuple[float, int, Optional[SavedState]]:

    if check_end_state(board, player) == GameState.IS_DRAW:
        tmp = (-math.inf, math.inf)[player == PLAYER1]
        return tmp, -1, save_state

    if depth == 0:
        p1_score = score_heuristic(board, PLAYER1)
        p2_score = score_heuristic(board, PLAYER2)
        return p1_score + p2_score, -1, save_state

    best_sco = (math.inf, -math.inf)[player == PLAYER1]
    best_act = -1

    actions = np.where(board[-1] == 0)[0]

    for action in actions:
        copy = apply_player_action(board, action, player, True)
        next_player = (PLAYER1, PLAYER2)[player == PLAYER1]
        score = minimax(copy, next_player, depth-1, save_state)[0]
        if player == PLAYER1 and score > best_sco:
            best_sco = score
            best_act = action
        elif player == PLAYER2 and score < best_sco:
            best_sco = score
            best_act = action

    return best_sco, best_act, save_state
