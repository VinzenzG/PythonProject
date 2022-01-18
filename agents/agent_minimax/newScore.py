
from typing import Tuple
import numpy as np
from numpy.lib import math

from agents.common import BoardPiece, SavedState, PlayerAction, PLAYER1, PLAYER2, GameState, check_end_state, \
    NO_PLAYER, apply_player_action, get_moves, connected_four

DEPTH = 4
Window = 4
nodeCount = np.long
nodeCount = 0


def count_node():
    global nodeCount
    nodeCount = nodeCount + 1


def cancel_nodes():
    global nodeCount
    nodeCount = 0


def generate_new_score(
        board: np.ndarray, player: BoardPiece) -> Tuple[PlayerAction, int, int]:
    score, action = negamax(board, player, -math.inf, math.inf)
    explored_nodes = nodeCount
    cancel_nodes()
    return action, score, explored_nodes

def negamax(
        board: np.ndarray,
        player: BoardPiece,
        alpha: int,
        beta: int
) -> Tuple[float, int]:

    count_node()  # incrementor of explored nodes
    # print(nodeCount, "expored nodes")
    # print(get_moves(), "moves")

    if get_moves() == 42:  # check draw game
        return 0, -1

    # (math.inf, -math.inf)[player == PLAYER1]
    best_act = -1

    actions = np.where(board[-1] == 0)[0]
    played_moves = get_moves()
    for action in actions:  # check if next is a winning move

        copy = apply_player_action(board.copy(), action, player)
        if connected_four(copy, player):
            return int((43 - (played_moves + 1)) / 2), action

    best_sco = -42
    max = int((41 - played_moves)/2)
    if beta > max:
        beta = max
        if alpha >= beta:
            return beta, -1

    for action in actions:

        copy = apply_player_action(board.copy(), action, player)
        next_player = (PLAYER1, PLAYER2)[player == PLAYER1]
        negamax_score = -(negamax(copy, next_player, -beta, -alpha))[0]

        if negamax_score >= beta:
            best_sco = negamax_score
            best_act = action
            return negamax_score, best_act
        if negamax_score > alpha:
            alpha = negamax_score
            best_act = action

    return alpha, best_act
