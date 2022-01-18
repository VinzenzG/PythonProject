import numpy as np
from numpy import int8

from agents.common import BoardPiece, NO_PLAYER, PLAYER1, PLAYER2, pretty_print_board, initialize_game_state, \
    apply_player_action, string_to_board, connected_four, check_end_state, GameState


def test_top_mask():
    from agents.commonBitboard import top_mask

    res = top_mask(1)
    ret = top_mask(6)
    assert res == 4096  # 2.[1] Spalte letzte Zeile
    print(res)
    assert ret == 140737488355328  # 7.[6] 47 shiften


def test_bottom_mask():
    from agents.commonBitboard import bottom_mask

    res = bottom_mask(1)
    ret = bottom_mask(6)
    assert res == 128  # 2.[1] Spalte letzte Zeile
    print(res)
    assert ret == 4398046511104  # 7.[6] 47 shiften


def test_can_play():
    from agents.commonBitboard import can_play
    res = can_play(0, 32)  # letzte Reihe belegt false
    ret = can_play(1, 32)  # frei true
    assert res == False
    assert ret == True


def test_play():
    from agents.commonBitboard import play

    res, mask = play(int(0), int(0), int(0))  # letzte Reihe belegt false
    ret, mask2 = play(1, 0, 0)  # frei true
    assert res == 0
    assert mask == 1

    assert ret == 0
    assert mask2 == 128


def test_initialize_game_state():
    from agents.common import initialize_game_state

    ret = initialize_game_state()

    assert isinstance(ret, np.ndarray)
    assert ret.dtype == BoardPiece
    assert ret.shape == (6, 7)
    assert np.all(ret == NO_PLAYER)


def test_pretty_print_board():
    from agents.common import pretty_print_board, initialize_game_state
    board = initialize_game_state()
    board[0][0] = PLAYER1
    ret = pretty_print_board(initialize_game_state())

    ret1 = np.ndarray((6, 7), BoardPiece())
    ret1.fill(PLAYER1)
    ret2 = np.ndarray((6, 7), BoardPiece())
    ret2.fill(PLAYER2)

    assert isinstance(ret, str)
    assert ret.partition('\n')[0] == "|==============|"
    assert ret.count('\n') == 8
    assert ret.split('\n')[7] == "|==============|"
    assert ret.split('\n')[8] == "|0 1 2 3 4 5 6 |"
    assert ret.split('\n')[1] == "|              |"
    assert pretty_print_board(ret1).split('\n')[1] == "|X X X X X X X |"
    assert pretty_print_board(ret2).split('\n')[1] == "|O O O O O O O |"
    assert pretty_print_board(board).split('\n')[6] == "|X             |"


def test_string_to_board():
    from agents.common import string_to_board
    ret = pretty_print_board(initialize_game_state())
    retTest = test_game_string()
    board = string_to_board(retTest)
    assert isinstance(string_to_board(retTest), np.ndarray)
    assert board.shape == (6, 7)
    assert board[0][1] == PLAYER2


def test_apply_player_action():
    board = initialize_game_state()
    boardhigh = string_to_board(test_game_string())
    action = 0
    player = PLAYER1
    copy = False
    ret = apply_player_action(board, action, player, copy)
    assert isinstance(ret, np.ndarray)
    assert apply_player_action(board, action, player, copy)[0][0] == 1
    assert apply_player_action(boardhigh, 1, player, copy)[2][1] == 1


def test_connected_four():
    board = string_to_board(test_game_string())
    boardh = string_to_board(test_horizontal_string())
    boardv = string_to_board(test_vertical_string())
    boardd = string_to_board(test_diagonal_string())
    boarddr = string_to_board(test_diagonalr_string())

    check = connected_four(board, PLAYER1)
    checkh = connected_four(boardh, PLAYER1)
    checkv = connected_four(boardv, PLAYER1)
    checkdl = connected_four(boardd, PLAYER1)
    checkdr = connected_four(boarddr, PLAYER1)

    assert isinstance(check, bool)
    # check
    assert checkh == True
    assert checkv == True
    assert checkdl == True


def test_check_end_state():
    board_player_one_win = string_to_board(test_horizontal_string())
    board_player_two_win = string_to_board(test_player2_string())
    board_still_playing = string_to_board(test_game_string())
    board_is_draw = string_to_board(test_draw_string())

    assert isinstance(check_end_state(board_still_playing, PLAYER1), GameState)
    assert check_end_state(board_player_one_win, PLAYER1) == GameState.IS_WIN
    assert check_end_state(board_player_two_win, PLAYER2) == GameState.IS_WIN
    assert check_end_state(board_still_playing, PLAYER1) == GameState.STILL_PLAYING
    assert check_end_state(board_is_draw, PLAYER1) == GameState.IS_DRAW


def test_game_string() -> str:
    return "|==============|\n" \
           "|              |\n" \
           "|              |\n" \
           "|    X X       |\n" \
           "|    O X X     |\n" \
           "|  O X O O     |\n" \
           "|  O O X X     |\n" \
           "|==============|\n" \
           "|0 1 2 3 4 5 6 |"


def test_horizontal_string() -> str:
    return "|==============|\n" \
           "|              |\n" \
           "|              |\n" \
           "|    X X       |\n" \
           "|    O X X     |\n" \
           "|  O X O O     |\n" \
           "|  X X X X     |\n" \
           "|==============|\n" \
           "|0 1 2 3 4 5 6 |"


def test_vertical_string() -> str:
    return "|==============|\n" \
           "|              |\n" \
           "|              |\n" \
           "|    X X       |\n" \
           "|    O X X     |\n" \
           "|  O X X O     |\n" \
           "|  O O X X     |\n" \
           "|==============|\n" \
           "|0 1 2 3 4 5 6 | "


def test_diagonal_string() -> str:
    return "|==============|\n" \
           "|              |\n" \
           "|              |\n" \
           "|    X X X     |\n" \
           "|    O X X     |\n" \
           "|  O X O O     |\n" \
           "|  X O X X     |\n" \
           "|==============|\n" \
           "|0 1 2 3 4 5 6 |"


def test_diagonalr_string() -> str:
    return "|==============|\n" \
           "|              |\n" \
           "|              |\n" \
           "|    X X       |\n" \
           "|    O X X     |\n" \
           "|  O X O X     |\n" \
           "|  O O X X X   |\n" \
           "|==============|\n" \
           "|0 1 2 3 4 5 6 |"


def test_player2_string() -> str:
    return "|==============|\n" \
           "|              |\n" \
           "|              |\n" \
           "|    O X       |\n" \
           "|    O O X     |\n" \
           "|  O X O O     |\n" \
           "|  O O X X O   |\n" \
           "|==============|\n" \
           "|0 1 2 3 4 5 6 |"


def test_draw_string() -> str:
    return "|==============|\n" \
           "|O O X O X O O |\n" \
           "|O O O X O O O |\n" \
           "|O X X X O X X |\n" \
           "|X O O X X O O |\n" \
           "|X O X O X X O |\n" \
           "|O O O X X O O |\n" \
           "|==============|\n" \
           "|0 1 2 3 4 5 6 |"
