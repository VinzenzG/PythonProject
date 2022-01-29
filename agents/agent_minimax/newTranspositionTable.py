from typing import Tuple
import numpy as np
from numpy.lib import math

from agents import TranspositionTable
from agents.commonBitboard import isWinningMove, can_play, PlayerAction, get_moves, apply_player_action, key

WIDTH = 7
HEIGHT = 6
nodeCount = np.long
nodeCount = 0

transpositiontable = TranspositionTable()


def count_node():
    global nodeCount
    nodeCount = nodeCount + 1


def cancel_nodes():
    global nodeCount
    nodeCount = 0


def generate_new_Transpositiontable(current: int, mask: int) -> Tuple[PlayerAction, int, int]:
    score, action = negamax(current, mask, -math.inf, math.inf)
    explored_nodes = nodeCount
    cancel_nodes()
    return action, score, explored_nodes


def order_from_middle(lst):
    lst = list(lst)
    left = lst[len(lst) // 2 - 1::-1]
    right = lst[len(lst) // 2:]
    output = [right.pop(0)] if len(lst) % 2 else []
    for t in zip(left, right):
        output += sorted(t, reverse=True)
    return output


def negamax(
        current: int,
        mask: int,
        alpha: int,
        beta: int
) -> Tuple[float, int]:
    count_node()  # incrementor of explored nodes
    nodes = nodeCount
    # print(nodeCount, "expored nodes")
    # print(get_moves(), "moves")
    if get_moves() == 42:  # check draw game
        return 0, -1

    # (math.inf, -math.inf)[player == PLAYER1]
    best_act = -1
    actions = []

    for x in range(WIDTH):
        if can_play(x, mask):
            actions.append(x)
        if can_play(x, mask) and isWinningMove(x, current, mask):  # check if current can win
            return int((WIDTH * HEIGHT + 1 - get_moves()) / 2), -1

    maximal = int((WIDTH * HEIGHT - 1 - get_moves()) / 2)
    k = key(current, mask)
    val = transpositiontable[k]
    if val is not None:
        pass

    if beta > maximal:
        beta = maximal
        if alpha >= beta:
            return beta, -1

    actions = order_from_middle(actions)
    for action in actions:

        copycurr, copymask = apply_player_action(action, current, mask)
        negamax_score = -(negamax(copycurr, copymask, -beta, -alpha))[0]

        if negamax_score >= beta:
            best_sco = negamax_score
            best_act = action
            return negamax_score, best_act
        if negamax_score > alpha:
            alpha = negamax_score
            best_act = action

    return alpha, best_act
