from typing import Optional, Tuple

import numpy as np
from random import randrange
from agents.common import BoardPiece, SavedState, PlayerAction, NO_PLAYER


def generate_move_random(
    board: np.ndarray, player: BoardPiece, saved_state: Optional[SavedState]
) -> Tuple[PlayerAction, Optional[SavedState]]:
    # Choose a valid, non-full column randomly and return it as `action`
    rand = randrange(7)
    while True:
        if board[5][rand] != NO_PLAYER:
            rand = randrange(7)
            continue
        break

    return rand, saved_state