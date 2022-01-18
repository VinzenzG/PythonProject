import timeit

import numpy as np
from typing import Optional, Callable, List
from agents.agent_minimax.alphabetapruning import generate_alpha_beta

from agents.agent_minimax.minimax import generate_minimax
from agents.agent_minimax.newNegamax import generate_new_negamax
from agents.agent_minimax.newOrder import generate_new_order
from agents.agent_minimax.newScore import generate_new_score
from agents.common import PlayerAction, BoardPiece, SavedState, GenMove
from agents.agent_random import generate_move
import time
from agents.common import PLAYER1, PLAYER2, PLAYER1_PRINT, PLAYER2_PRINT, GameState
from agents.common import initialize_game_state, pretty_print_board, apply_player_action, check_end_state

# t0 = time.time()
# print(pretty_print_board(board))
# print(
#     f'{player_name} you are playing with {PLAYER1_PRINT if player == PLAYER1 else PLAYER2_PRINT}'
# )
#
# print(f"Move time: {time.time() - t0:.3f}s")


if __name__ == "__main__":
    with open("./Benchmark data sets/Test_L3_R1") as f:
        data = f.readlines()[9]
        data = data.split(" ")
        board = initialize_game_state()
        playerOne = True
        PlayerAction = np.int8  # The column to be played

        for move in data[0]:
            apply_player_action(board, int(move) - 1, (PLAYER2, PLAYER1)[playerOne])
            if playerOne:
                playerOne = False
            else:
                playerOne = True

    t0 = time.time()

    action, score, nodes = generate_new_order(board, (PLAYER2, PLAYER1)[playerOne])

    t1 = time.time()
    tges = t1 - t0
    print(("False, ", "True, ")[score == int(data[1].split("/")[0])] + str(action) + ", " + str(
            score) + ", " + str(nodes) + ", " + str(round(tges, 3)))
    print(data)
