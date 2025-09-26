import tkinter as tk
from tkinter import ttk
import L4 as l4

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Title.TLabel', font=('Arial', 24, 'bold'), background='#2c3e50', foreground='white')
        self.style.configure('Game.TButton', font=('Arial', 12), padding=10)
        self.style.configure('Info.TLabel', font=('Arial', 12), background='#2c3e50', foreground='#ecf0f1')
        self.style.configure('Control.TButton', font=('Arial', 10), padding=5)
        
        # Game state
        self.game_mode = None
        self.board = None
        self.size = 8
        self.win_length = 4
        self.game_over = False
        self.current_player = 'X'
        self.buttons = []
        
        self.setup_main_menu()
    
    def setup_main_menu(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main title
        title_label = ttk.Label(self.root, text="❌⭕ Tic Tac Toe", style='Title.TLabel')
        title_label.pack(pady=20)
        
        # Subtitle
        subtitle_label = ttk.Label(self.root, text="Choose your game mode", style='Info.TLabel')
        subtitle_label.pack(pady=10)
        
        # Game buttons frame
        buttons_frame = tk.Frame(self.root, bg='#2c3e50')
        buttons_frame.pack(expand=True, fill='both', padx=50, pady=20)

        # AI vs Player Button
        ai_btn = ttk.Button(buttons_frame, text="🤖 Play vs AI", 
                           command=lambda: self.start_game('ai'), style='Game.TButton')
        ai_btn.pack(fill='x', pady=10)
        
        # Player vs Player Button
        pvp_btn = ttk.Button(buttons_frame, text="👥 Player vs Player", 
                            command=lambda: self.start_game('pvp'), style='Game.TButton')
        pvp_btn.pack(fill='x', pady=10)
        
        # Exit button
        exit_btn = ttk.Button(buttons_frame, text="🚪 Exit", command=self.root.quit, style='Game.TButton')
        exit_btn.pack(fill='x', pady=20)
    
    def start_game(self, mode):
        self.game_mode = mode
        self.setup_game_interface()
    
    def setup_game_interface(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Top control frame
        top_frame = tk.Frame(self.root, bg='#2c3e50')
        top_frame.pack(fill='x', padx=20, pady=10)
        
        # Title
        mode_text = "AI Challenge" if self.game_mode == 'ai' else "Player vs Player"
        title_label = ttk.Label(top_frame, text=f"❌⭕ Tic Tac Toe - {mode_text}", 
                               font=('Arial', 18, 'bold'), background='#2c3e50', foreground='white')
        title_label.pack(side='left')
        
        # Back to menu button
        back_btn = ttk.Button(top_frame, text="🏠 Menu", command=self.setup_main_menu, style='Control.TButton')
        back_btn.pack(side='right')
        
        # Control frame
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(pady=10)
        
        # Size selection
        ttk.Label(control_frame, text="Board Size:", background='#2c3e50', foreground='white').pack(side='left', padx=5)
        self.size_var = tk.StringVar(value="8")
        size_combo = ttk.Combobox(control_frame, textvariable=self.size_var, values=["4", "5", "6", "7", "8", "9", "10"], width=5)
        size_combo.pack(side='left', padx=5)
        
        # New game button
        new_game_btn = ttk.Button(control_frame, text="🆕 New Game", command=self.new_game, style='Control.TButton')
        new_game_btn.pack(side='left', padx=10)
        
        # Status label
        self.status_label = ttk.Label(self.root, text="", 
                                     font=('Arial', 12), background='#2c3e50', foreground='#f39c12')
        self.status_label.pack(pady=10)
        
        # Game board frame
        self.board_frame = tk.Frame(self.root, bg='#2c3e50')
        self.board_frame.pack(pady=20)
        
        # Initialize game
        self.new_game()
    
    def new_game(self):
        self.size = int(self.size_var.get())
        self.win_length = min(4, self.size)
        self.board = l4.create_board(self.size)
        self.game_over = False
        self.current_player = 'X'  # Reset to Player 1
        
        # Clear and recreate board
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        # Create buttons for each cell
        self.buttons = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                btn = tk.Button(self.board_frame, text="", font=('Arial', 10, 'bold'), 
                               width=3, height=2, command=lambda r=i, c=j: self.make_move(r, c),
                               bg='#ecf0f1', fg='#2c3e50', relief='raised', bd=2)
                btn.grid(row=i, column=j, padx=1, pady=1)
                row.append(btn)
            self.buttons.append(row)
        
        # Set initial status based on mode
        if self.game_mode == 'ai':
            self.status_label.config(text="Your turn! Click a cell to make your move", foreground='#f39c12')
        else:
            self.status_label.config(text="Player 1's turn (X)", foreground='#e74c3c')
    
    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != '.':
            return
        
        if self.game_mode == 'ai':
            self.make_ai_move(row, col)
        else:
            self.make_pvp_move(row, col)
    
    def make_ai_move(self, row, col):
        """Handle move in AI mode"""
        # Human move
        self.board[row][col] = 'X'
        self.buttons[row][col].config(text='X', fg='#e74c3c', state='disabled')
        
        # Check for human win
        if l4.check_win(self.board, 'X', self.win_length):
            self.status_label.config(text="🎉 You Win! Congratulations!", foreground='#27ae60')
            self.game_over = True
            self.disable_all_buttons()
            return
        
        # Check for draw
        if l4.is_full(self.board):
            self.status_label.config(text="🤝 It's a Draw!", foreground='#f39c12')
            self.game_over = True
            self.disable_all_buttons()
            return
        
        # AI move
        self.status_label.config(text="🤖 AI is thinking...", foreground='#3498db')
        self.root.update()
        
        l4.ai_move(self.board)
        
        # Find AI's move and update button
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 'O' and self.buttons[i][j]['text'] == '':
                    self.buttons[i][j].config(text='O', fg='#3498db', state='disabled')
                    break
        
        # Check for AI win
        if l4.check_win(self.board, 'O', self.win_length):
            self.status_label.config(text="🤖 AI Wins! Better luck next time!", foreground='#e74c3c')
            self.game_over = True
            self.disable_all_buttons()
            return
        
        # Check for draw
        if l4.is_full(self.board):
            self.status_label.config(text="🤝 It's a Draw!", foreground='#f39c12')
            self.game_over = True
            self.disable_all_buttons()
            return
        
        self.status_label.config(text="Your turn! Click a cell to make your move", foreground='#f39c12')
    
    def make_pvp_move(self, row, col):
        """Handle move in Player vs Player mode"""
        # Make the move for current player
        self.board[row][col] = self.current_player
        
        # Update button appearance
        if self.current_player == 'X':
            self.buttons[row][col].config(text='X', fg='#e74c3c', state='disabled')
        else:
            self.buttons[row][col].config(text='O', fg='#3498db', state='disabled')
        
        # Check for win
        if l4.check_win(self.board, self.current_player, self.win_length):
            player_name = "Player 1" if self.current_player == 'X' else "Player 2"
            self.status_label.config(text=f"🎉 {player_name} Wins! Congratulations!", foreground='#27ae60')
            self.game_over = True
            self.disable_all_buttons()
            return
        
        # Check for draw
        if l4.is_full(self.board):
            self.status_label.config(text="🤝 It's a Draw!", foreground='#f39c12')
            self.game_over = True
            self.disable_all_buttons()
            return
        
        # Switch players
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        
        # Update status
        if self.current_player == 'X':
            self.status_label.config(text="Player 1's turn (X)", foreground='#e74c3c')
        else:
            self.status_label.config(text="Player 2's turn (O)", foreground='#3498db')
    
    def disable_all_buttons(self):
        for i in range(self.size):
            for j in range(self.size):
                self.buttons[i][j].config(state='disabled')


def main():
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
