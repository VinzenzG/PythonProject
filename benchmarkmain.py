import time

import numpy as np

from agents.agent_minimax.newOrder import generate_new_order
from agents.common import PLAYER1, PLAYER2
from agents.common import initialize_game_state, apply_player_action

# t0 = time.time()
# print(pretty_print_board(board))
# print(
#     f'{player_name} you are playing with {PLAYER1_PRINT if player == PLAYER1 else PLAYER2_PRINT}'
# )
#
# print(f"Move time: {time.time() - t0:.3f}s")


if __name__ == "__main__":
    with open("./Benchmark data sets/Test_L2_R1") as f:
        for line in f:
            data = line.split(" ")
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
            # rightscore, bestAction, Score, exploredNodes, neededTime in sec
            print(("False, ", "True, ")[score == int(data[1].split("/")[0])] + str(action) + ", " + str(
                score) + ", " + str(nodes) + ", " + str(round(tges, 3)))
            print(data)
            with open("./Benchmark data sets/iteration3_L2_R1", 'a') as file:
                file.write(("False, ", "True, ")[score == int(data[1].split("/")[0])] + str(action) + ", " + str(
                    score) + ", " + str(nodes) + ", " + str(round(tges, 3)) + "\n")
                file.close()
