import os
import sys
import time

# Ensure project root is on sys.path so tests can import project modules
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from tictactoe import l4


def test_ai_makes_legal_move_under_time_limit():
    b = l4.create_board(6)
    # Pre-fill some moves
    b[2][2] = 'X'
    b[3][3] = 'O'
    before = [row[:] for row in b]
    # Very small time limit; AI should still make a legal move and not raise
    l4.ai_move(b, time_limit=0.01)
    # Ensure exactly one new O was placed
    diff = [(r, c) for r in range(len(b)) for c in range(len(b)) if before[r][c] != b[r][c]]
    assert len(diff) == 1
    r, c = diff[0]
    assert b[r][c] == 'O'


def test_ai_takes_immediate_win_when_available():
    b = l4.create_board(4)
    # Setup O to have immediate win
    b[1][0] = 'O'
    b[1][1] = 'O'
    b[1][2] = 'O'
    l4.ai_move(b, time_limit=1.0)
    assert l4.check_win(b, 'O', win_length=4)


def test_ai_blocks_immediate_opponent_win():
    b = l4.create_board(4)
    # X about to win
    b[0][0] = 'X'
    b[0][1] = 'X'
    b[0][2] = 'X'
    # AI should block at (0,3)
    l4.ai_move(b, time_limit=1.0)
    assert b[0][3] == 'O'
