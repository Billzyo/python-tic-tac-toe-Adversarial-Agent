import os
import sys
import copy

# Ensure project root is on sys.path so tests can import project modules
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import L4 as l4


def test_create_board_and_empty():
    b = l4.create_board(5)
    assert len(b) == 5
    assert all(len(row) == 5 for row in b)
    assert all(cell == '.' for row in b for cell in row)


def test_is_full_true_and_false():
    b = [['X' for _ in range(4)] for _ in range(4)]
    assert l4.is_full(b) is True
    b[0][0] = '.'
    assert l4.is_full(b) is False


def test_check_win_horizontal_vertical_diagonal():
    # Horizontal win
    b = l4.create_board(4)
    for c in range(4):
        b[1][c] = 'X'
    assert l4.check_win(b, 'X', win_length=4)

    # Vertical win
    b = l4.create_board(4)
    for r in range(4):
        b[r][2] = 'O'
    assert l4.check_win(b, 'O', win_length=4)

    # Diagonal win
    b = l4.create_board(4)
    for i in range(4):
        b[i][i] = 'X'
    assert l4.check_win(b, 'X', win_length=4)

    # Anti-diagonal win
    b = l4.create_board(4)
    for i in range(4):
        b[3 - i][i] = 'O'
    assert l4.check_win(b, 'O', win_length=4)


def test_check_immediate_tactics_identifies_win_and_block():
    # Immediate win for O
    b = l4.create_board(4)
    b[2][0] = 'O'
    b[2][1] = 'O'
    b[2][2] = 'O'
    move, typ = l4.check_immediate_tactics(b, 'O')
    assert typ == 'win'
    assert move == (2, 3)

    # Immediate block required (X about to win)
    b = l4.create_board(4)
    b[0][0] = 'X'
    b[0][1] = 'X'
    b[0][2] = 'X'
    move, typ = l4.check_immediate_tactics(b, 'O')
    assert typ == 'block'
    assert move == (0, 3)
