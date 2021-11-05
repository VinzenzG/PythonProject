import numpy as np
from numpy import int8

from agents.common import BoardPiece, NO_PLAYER, PLAYER1, PLAYER2, pretty_print_board, initialize_game_state, \
    test_game_string, apply_player_action, string_to_board


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


