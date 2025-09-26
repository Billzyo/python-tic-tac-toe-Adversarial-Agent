import random
import L2 as l2
import L3 as l3

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

def get_candidate_moves(board, radius=1):
    """Get moves near existing pieces to reduce search space"""
    size = len(board)
    candidates = set()
    
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

def minimax_alpha_beta(board, depth, is_maximizing, alpha=-float('inf'), beta=float('inf')):
    """Minimax with alpha-beta pruning for better performance"""
    score = evaluate(board)
    if score == 10 or score == -10 or is_full(board) or depth == 0:
        return score

    if is_maximizing:
        best = -float('inf')
        candidates = get_candidate_moves(board)
        
        for r, c in candidates:
            board[r][c] = 'O'
            best = max(best, minimax_alpha_beta(board, depth-1, False, alpha, beta))
            board[r][c] = '.'
            
            # Alpha-beta pruning
            alpha = max(alpha, best)
            if beta <= alpha:
                break  # Beta cutoff
                
        return best
    else:
        best = float('inf')
        candidates = get_candidate_moves(board)
        
        for r, c in candidates:
            board[r][c] = 'X'
            best = min(best, minimax_alpha_beta(board, depth-1, True, alpha, beta))
            board[r][c] = '.'
            
            # Alpha-beta pruning
            beta = min(beta, best)
            if beta <= alpha:
                break  # Alpha cutoff
                
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

def ai_move(board):
    """Optimized AI move using alpha-beta pruning and candidate moves"""
    best_val = -float('inf')
    best_move = None
    
    # Get candidate moves (near existing pieces)
    candidates = get_candidate_moves(board)
    
    # If no candidates, fallback to all empty cells
    if not candidates:
        size = len(board)
        candidates = [(r, c) for r in range(size) for c in range(size) if board[r][c] == '.']
    
    # Evaluate each candidate move
    for r, c in candidates:
        board[r][c] = 'O'
        move_val = minimax_alpha_beta(board, depth=2, is_maximizing=False)
        board[r][c] = '.'
        
        if move_val > best_val:
            best_val = move_val
            best_move = (r, c)
    
    # Make the best move
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

