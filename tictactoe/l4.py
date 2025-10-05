"""Core game logic and AI (moved from top-level L4.py)
"""
import random
from collections import deque

# Transposition table for caching board evaluations
transposition_table = {}

def clear_transposition_table():
    global transposition_table
    transposition_table.clear()

def create_board(size=8):
    return [['.' for _ in range(size)] for _ in range(size)]

def is_full(board):
    return all(cell!='.' for row in board for cell in row)

def check_win(board,player,win_length=4):
    size=len(board)
    # Horizontal & vertical
    for r in range(size):
        for c in range(size-win_length+1):
            if all(board[r][c+i]==player for i in range(win_length)):
                return True
            if all(board[c+i][r]==player for i in range(win_length)):
                return True
    # Diagonal
    for r in range(size-win_length+1):
        for c in range(size-win_length+1):
            if all(board[r+i][c+i]==player for i in range(win_length)):
                return True
            if all(board[r+win_length-1-i][c+i]==player for i in range(win_length)):
                return True
    return False

def evaluate(board):
    if check_win(board,'O'):
        return 10
    elif check_win(board,'X'):
        return -10
    else:
        return 0

def board_to_string(board):
    return ''.join(''.join(row) for row in board)

def minimax_alpha_beta(board, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
    board_key = board_to_string(board)
    if (board_key, depth, is_maximizing) in transposition_table:
        return transposition_table[(board_key, depth, is_maximizing)]
    score = evaluate(board)
    if score == 10 or score == -10 or is_full(board) or depth == 0:
        transposition_table[(board_key, depth, is_maximizing)] = score
        return score
    if is_maximizing:
        best = -float('inf')
        player = 'O'
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c]=='.':
                    board[r][c]=player
                    best = max(best, minimax_alpha_beta(board, depth-1, False, alpha, beta))
                    board[r][c]='.'
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        break
        transposition_table[(board_key, depth, is_maximizing)] = best
        return best
    else:
        best = float('inf')
        player = 'X'
        for r in range(len(board)):
            for c in range(len(board)):
                if board[r][c]=='.':
                    board[r][c]=player
                    best = min(best, minimax_alpha_beta(board, depth-1, True, alpha, beta))
                    board[r][c]='.'
                    beta = min(beta, best)
                    if beta <= alpha:
                        break
        transposition_table[(board_key, depth, is_maximizing)] = best
        return best

def check_immediate_tactics(board, player='O'):
    size = len(board)
    win_length = min(4, size)
    empty_cells = [(r, c) for r in range(size) for c in range(size) if board[r][c] == '.']
    for r, c in empty_cells:
        board[r][c] = player
        if check_win(board, player, win_length):
            board[r][c] = '.'
            return (r, c), 'win'
        board[r][c] = '.'
    opponent = 'X' if player == 'O' else 'O'
    for r, c in empty_cells:
        board[r][c] = opponent
        if check_win(board, opponent, win_length):
            board[r][c] = '.'
            return (r, c), 'block'
        board[r][c] = '.'
    return None, None

def ai_move(board, time_limit=1.0):
    tactical_move, _ = check_immediate_tactics(board, 'O')
    if tactical_move:
        board[tactical_move[0]][tactical_move[1]] = 'O'
        return
    candidates = [(r, c) for r in range(len(board)) for c in range(len(board)) if board[r][c]=='.']
    if not candidates:
        return
    best_move = None
    start_time = __import__('time').time()
    depth = 1
    while __import__('time').time() - start_time < time_limit and depth <= 3:
        for r, c in candidates:
            if __import__('time').time() - start_time >= time_limit:
                break
            board[r][c] = 'O'
            val = minimax_alpha_beta(board, depth=depth, is_maximizing=False)
            board[r][c] = '.'
            if best_move is None or val > best_val:
                best_val = val
                best_move = (r, c)
        depth += 1
    if best_move:
        board[best_move[0]][best_move[1]] = 'O'
    else:
        r, c = random.choice(candidates)
        board[r][c] = 'O'
