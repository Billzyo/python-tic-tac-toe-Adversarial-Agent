import random
import L2 as l2
import L3 as l3

# Transposition table for caching board evaluations
transposition_table = {}

def clear_transposition_table():
    """Clear the transposition table to free memory"""
    global transposition_table
    transposition_table.clear()

# --- Tic Tac Toe Functions ---
def create_board(size=8):
    return [['.' for _ in range(size)] for _ in range(size)]

def print_board(board):
    print("\n  " + " ".join(str(i) for i in range(len(board[0]))))
    for idx,row in enumerate(board):
        print(idx," ".join(row))
    print()

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

def human_move(board):
    size = len(board)
    while True:
        try:
            move = input(f"Enter your move as row,col (0-{size-1}): ")
            row, col = map(int, move.split(','))
            if 0 <= row < size and 0 <= col < size and board[row][col] == '.':
                board[row][col] = 'X'
                break
            else:
                print("Invalid or occupied cell.")
        except ValueError:
            print("Enter valid integers in the format row,col (e.g., 0,1).")

# --- Optimized Minimax with Alpha-Beta Pruning ---
def evaluate(board):
    if check_win(board,'O'):
        return 10
    elif check_win(board,'X'):
        return -10
    else:
        return 0

def get_adaptive_radius(board):
    """Calculate adaptive radius based on board size and game phase"""
    size = len(board)
    occupied_count = sum(1 for row in board for cell in row if cell != '.')
    total_cells = size * size
    
    # Base radius on board size
    base_radius = min(2, max(1, size // 4))
    
    # Adjust based on game phase
    if occupied_count < total_cells * 0.1:  # Opening
        return base_radius
    elif occupied_count < total_cells * 0.5:  # Midgame
        return base_radius + 1
    else:  # Endgame
        return base_radius + 2

def get_candidate_moves(board, radius=None):
    """Get moves near existing pieces with adaptive radius"""
    size = len(board)
    candidates = set()
    
    if radius is None:
        radius = get_adaptive_radius(board)
    
    # Find all occupied cells
    occupied = []
    for r in range(size):
        for c in range(size):
            if board[r][c] != '.':
                occupied.append((r, c))
    
    # If board is empty, return center area
    if not occupied:
        center = size // 2
        for r in range(max(0, center-1), min(size, center+2)):
            for c in range(max(0, center-1), min(size, center+2)):
                if board[r][c] == '.':
                    candidates.add((r, c))
        return list(candidates)
    
    # Add cells within radius of occupied cells
    for r, c in occupied:
        for dr in range(-radius, radius+1):
            for dc in range(-radius, radius+1):
                nr, nc = r + dr, c + dc
                if (0 <= nr < size and 0 <= nc < size and 
                    board[nr][nc] == '.'):
                    candidates.add((nr, nc))
    
    # If no candidates found (shouldn't happen), fallback to all empty
    if not candidates:
        for r in range(size):
            for c in range(size):
                if board[r][c] == '.':
                    candidates.add((r, c))
    
    return list(candidates)

def evaluate_move_priority(move, board, player='O'):
    """Evaluate move priority for better ordering (higher = better)"""
    r, c = move
    size = len(board)
    priority = 0
    
    # Center moves are generally better
    center = size // 2
    distance_from_center = abs(r - center) + abs(c - center)
    priority += (size - distance_from_center) * 10
    
    # Check for immediate win
    board[r][c] = player
    if check_win(board, player, min(4, size)):
        priority += 1000
    board[r][c] = '.'
    
    # Check for immediate block
    opponent = 'X' if player == 'O' else 'O'
    board[r][c] = opponent
    if check_win(board, opponent, min(4, size)):
        priority += 900
    board[r][c] = '.'
    
    # Prefer moves near existing pieces
    nearby_pieces = 0
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            nr, nc = r + dr, c + dc
            if (0 <= nr < size and 0 <= nc < size and 
                board[nr][nc] != '.'):
                nearby_pieces += 1
    priority += nearby_pieces * 5
    
    return priority

def get_ordered_candidates(board, player='O'):
    """Get candidate moves ordered by priority"""
    candidates = get_candidate_moves(board)
    return sorted(candidates, key=lambda move: evaluate_move_priority(move, board, player), reverse=True)

def board_to_string(board):
    """Convert board to string for hashing"""
    return ''.join(''.join(row) for row in board)

def minimax_alpha_beta(board, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
    """Minimax with alpha-beta pruning, move ordering, and transposition table"""
    # Check transposition table
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
        candidates = get_ordered_candidates(board, player)
        
        for r, c in candidates:
            board[r][c] = player
            best = max(best, minimax_alpha_beta(board, depth-1, False, alpha, beta))
            board[r][c] = '.'
            
            # Alpha-beta pruning
            alpha = max(alpha, best)
            if beta <= alpha:
                break  # Beta cutoff
                
        transposition_table[(board_key, depth, is_maximizing)] = best
        return best
    else:
        best = float('inf')
        player = 'X'
        candidates = get_ordered_candidates(board, player)
        
        for r, c in candidates:
            board[r][c] = player
            best = min(best, minimax_alpha_beta(board, depth-1, True, alpha, beta))
            board[r][c] = '.'
            
            # Alpha-beta pruning
            beta = min(beta, best)
            if beta <= alpha:
                break  # Alpha cutoff
                
        transposition_table[(board_key, depth, is_maximizing)] = best
        return best

# Keep original minimax for backward compatibility
def minimax(board, depth, is_maximizing):
    score = evaluate(board)
    if score==10 or score==-10 or is_full(board) or depth==0:
        return score

    size = len(board)
    if is_maximizing:
        best = -1000
        for r in range(size):
            for c in range(size):
                if board[r][c]=='.':
                    board[r][c]='O'
                    best = max(best,minimax(board,depth-1,False))
                    board[r][c]='.'
        return best
    else:
        best = 1000
        for r in range(size):
            for c in range(size):
                if board[r][c]=='.':
                    board[r][c]='X'
                    best = min(best,minimax(board,depth-1,True))
                    board[r][c]='.'
        return best

def check_immediate_tactics(board, player='O'):
    """Check for immediate win or block moves"""
    size = len(board)
    win_length = min(4, size)
    
    # Get all empty cells
    empty_cells = [(r, c) for r in range(size) for c in range(size) if board[r][c] == '.']
    
    # Check for immediate win
    for r, c in empty_cells:
        board[r][c] = player
        if check_win(board, player, win_length):
            board[r][c] = '.'
            return (r, c), 'win'
        board[r][c] = '.'
    
    # Check for immediate block
    opponent = 'X' if player == 'O' else 'O'
    for r, c in empty_cells:
        board[r][c] = opponent
        if check_win(board, opponent, win_length):
            board[r][c] = '.'
            return (r, c), 'block'
        board[r][c] = '.'
    
    return None, None

def ai_move(board, time_limit=1.0):
    """Enhanced AI move with tactical checks and time management"""
    import time
    
    # First, check for immediate tactical moves
    tactical_move, tactic_type = check_immediate_tactics(board, 'O')
    if tactical_move:
        board[tactical_move[0]][tactical_move[1]] = 'O'
        return
    
    # Get ordered candidate moves
    candidates = get_ordered_candidates(board, 'O')
    
    # If no candidates, fallback to all empty cells
    if not candidates:
        size = len(board)
        candidates = [(r, c) for r in range(size) for c in range(size) if board[r][c] == '.']
    
    best_val = -float('inf')
    best_move = None
    start_time = time.time()
    
    # Iterative deepening with time limit
    depth = 1
    while time.time() - start_time < time_limit and depth <= 4:
        current_best = None
        current_val = -float('inf')
        
        for r, c in candidates:
            if time.time() - start_time >= time_limit:
                break
                
            board[r][c] = 'O'
            move_val = minimax_alpha_beta(board, depth=depth, is_maximizing=False)
            board[r][c] = '.'
            
            if move_val > current_val:
                current_val = move_val
                current_best = (r, c)
        
        if current_best:
            best_move = current_best
            best_val = current_val
        
        depth += 1
    
    # Make the best move found
    if best_move:
        board[best_move[0]][best_move[1]] = 'O'
    else:
        # Fallback: random move from candidates
        if candidates:
            r, c = random.choice(candidates)
            board[r][c] = 'O'

def ai_move_original(board):
    """Original AI move function (kept for comparison)"""
    size=len(board)
    best_val = -1000
    best_move = None
    # Check all empty cells
    for r in range(size):
        for c in range(size):
            if board[r][c]=='.':
                board[r][c]='O'
                move_val = minimax(board, depth=2, is_maximizing=False)
                board[r][c]='.'
                if move_val > best_val:
                    best_val = move_val
                    best_move = (r,c)
    if best_move:
        board[best_move[0]][best_move[1]]='O'
    else:
        # fallback random
        empty=[(r,c) for r in range(size) for c in range(size) if board[r][c]=='.']
        if empty:
            r,c=random.choice(empty)
            board[r][c]='O'

# --- Main Game Loop ---
def tic_tac_toe_game():
    try:
        size = int(input("Enter board size (min 4, default 8): "))
        if size<4:
            size=8
    except:
        size=8
    win_length = min(4,size)  # always 4 in a row to win
    board=create_board(size)
    print_board(board)
    
    while True:
        human_move(board)
        print_board(board)
        if check_win(board,'X',win_length):
            print("Human wins!")
            break
        if is_full(board):
            print("Draw!")
            break

        ai_move(board)
        print_board(board)
        if check_win(board,'O',win_length):
            print("AI wins!")
            break
        if is_full(board):
            print("Draw!")
            break

