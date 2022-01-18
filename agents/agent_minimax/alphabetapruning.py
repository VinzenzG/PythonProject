import math
from typing import Optional, Tuple
import numpy as np
from agents.common import BoardPiece, SavedState, PlayerAction, PLAYER1, PLAYER2, GameState, check_end_state, \
    NO_PLAYER, apply_player_action

DEPTH = 4
Window = 4
score_dict = {
    4: 512,
    3: 64,
    2: 8

}


def generate_alpha_beta(
        board: np.ndarray, player: BoardPiece, save_state: Optional[SavedState] = None
) -> Tuple[PlayerAction, Optional[SavedState], int]:
    score, action, save_state = minimax(board, player, DEPTH, -math.inf, math.inf, save_state)
    return action, save_state


def calc_score(target_window: np.ndarray, player: BoardPiece) -> float:

    temp = 0
    if np.count_nonzero(target_window == player) == Window:
        temp += score_dict.get(Window)
    elif np.count_nonzero(target_window == player) == Window - 1 and np.count_nonzero(target_window == NO_PLAYER) == 1:
        temp += score_dict.get(Window - 1)
    elif np.count_nonzero(target_window == player) == Window - 2 and np.count_nonzero(target_window == NO_PLAYER) == 2:
        temp += score_dict.get(Window - 2)

    return temp


def score_heuristic(board: np.ndarray, player: BoardPiece) -> float:
    score = 0
    rows, cols = board.shape
    rows_edge = rows - Window + 1
    cols_edge = cols - Window + 1
    piece = np.int8

    score_board = np.ndarray((rows, cols), piece)
    score_board.fill(0)
    # horizontal
    for x in range(rows):
        for y in range(cols_edge):
            target = board[x, y:y + Window]
            tmp_score = calc_score(target, player)
            score_board[x][y] += tmp_score
            score += tmp_score

    # vertical
    for y in range(cols):
        for x in range(rows_edge):
            target = board[x: x + Window, y]
            tmp_score = calc_score(target, player)
            score_board[x][y] += tmp_score
            score += tmp_score

    # diagonal
    for x in range(rows_edge):
        for y in range(cols_edge):
            win_block = board[x:x + Window, y:y + Window]  # create a block of four pieces x four pieces
            target = np.diag(win_block)
            tmp_score = calc_score(target, player)
            score_board[x][y] += tmp_score
            score += tmp_score

            target = np.diag(win_block[::-1, :])
            tmp_score = calc_score(target, player)
            score_board[x][y] += tmp_score
            score += tmp_score
    return (score * (-1), score)[player == PLAYER1]


def minimax(
        board: np.ndarray,
        player: BoardPiece,
        depth: int,
        alpha: int,
        beta: int,
        save_state: Optional[SavedState] = None
) -> Tuple[float, int, Optional[SavedState]]:
    if check_end_state(board, player) == GameState.IS_DRAW:
        tmp = (math.inf, -math.inf)[player == PLAYER1]
        return tmp, -1, save_state

    if depth == 0:
        p1_score = score_heuristic(board, PLAYER1)
        p2_score = score_heuristic(board, PLAYER2)
        return p1_score + p2_score, -1, save_state

    best_sco = (math.inf, -math.inf)[player == PLAYER1]
    best_act = -1

    actions = np.where(board[-1] == 0)[0]

    for action in actions:
        copy = apply_player_action(board.copy(), action, player)
        next_player = (PLAYER1, PLAYER2)[player == PLAYER1]
        minimaxi = minimax(copy, next_player, depth - 1, alpha, beta, save_state)
        score = minimaxi[0]
        score_board = minimaxi[2]
        # print(score_board)
        if player == PLAYER1 and score > best_sco:
            best_sco = score
            best_act = action
            alpha = max(alpha, best_sco)
            if alpha >= beta:
                break
        elif player == PLAYER2 and score < best_sco:
            best_sco = score
            best_act = action
            beta = min(beta, best_sco)
            if alpha >= beta:
                break

    # print("best action {} for player{} with score {} in depth {}".format(best_act,player, best_sco, depth))
    return best_sco, best_act, save_state
