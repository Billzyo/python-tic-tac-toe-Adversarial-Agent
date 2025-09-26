import tkinter as tk
from tkinter import ttk
import L4 as l4

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2c3e50')
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Title.TLabel', font=('Arial', 24, 'bold'), background='#2c3e50', foreground='white')
        self.style.configure('Game.TButton', font=('Arial', 14), padding=20)
        self.style.configure('Info.TLabel', font=('Arial', 12), background='#2c3e50', foreground='#ecf0f1')
        
        self.setup_main_menu()
    
    def setup_main_menu(self):
        # Clear existing widgets
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Main title
        title_label = ttk.Label(self.root, text="❌⭕ Tic Tac Toe", style='Title.TLabel')
        title_label.pack(pady=30)
        
        # Subtitle
        subtitle_label = ttk.Label(self.root, text="Play against the AI (minimax)", style='Info.TLabel')
        subtitle_label.pack(pady=10)
        
        # Game buttons frame
        buttons_frame = tk.Frame(self.root, bg='#2c3e50')
        buttons_frame.pack(expand=True, fill='both', padx=50, pady=30)

        # Tic Tac Toe Button
        ttt_btn = ttk.Button(buttons_frame, text="Play Tic Tac Toe", 
                            command=self.open_tic_tac_toe, style='Game.TButton')
        ttt_btn.pack(fill='x', pady=10)
        
        # Exit button
        exit_btn = ttk.Button(buttons_frame, text="🚪 Exit", command=self.root.quit, style='Game.TButton')
        exit_btn.pack(fill='x', pady=20)
    
    def open_tic_tac_toe(self):
        self.ttt_window = TicTacToeWindow(self.root, l4)

class TicTacToeWindow:
    def __init__(self, parent, game_module):
        self.parent = parent
        self.game_module = game_module
        
        # Create new window
        self.window = tk.Toplevel(parent)
        self.window.title("Tic Tac Toe - AI Challenge")
        self.window.geometry("600x700")
        self.window.configure(bg='#34495e')
        
        # Title
        title_label = ttk.Label(self.window, text="❌⭕ Tic Tac Toe - AI Challenge", 
                               font=('Arial', 18, 'bold'), background='#34495e', foreground='white')
        title_label.pack(pady=20)
        
        # Control frame
        control_frame = tk.Frame(self.window, bg='#34495e')
        control_frame.pack(pady=10)
        
        # Size selection
        ttk.Label(control_frame, text="Board Size:", background='#34495e', foreground='white').pack(side='left', padx=5)
        self.size_var = tk.StringVar(value="8")
        size_combo = ttk.Combobox(control_frame, textvariable=self.size_var, values=["4", "5", "6", "7", "8", "9", "10"], width=5)
        size_combo.pack(side='left', padx=5)
        
        # New game button
        new_game_btn = ttk.Button(control_frame, text="🆕 New Game", command=self.new_game)
        new_game_btn.pack(side='left', padx=10)
        
        # Close button
        close_btn = ttk.Button(control_frame, text="❌ Close", command=self.window.destroy)
        close_btn.pack(side='left', padx=10)
        
        # Status label
        self.status_label = ttk.Label(self.window, text="Your turn! Click a cell to make your move", 
                                     font=('Arial', 12), background='#34495e', foreground='#f39c12')
        self.status_label.pack(pady=10)
        
        # Game board frame
        self.board_frame = tk.Frame(self.window, bg='#34495e')
        self.board_frame.pack(pady=20)
        
        # Initialize game
        self.size = 8
        self.board = None
        self.win_length = 4
        self.game_over = False
        
        self.new_game()
    
    def new_game(self):
        self.size = int(self.size_var.get())
        self.win_length = min(4, self.size)
        self.board = self.game_module.create_board(self.size)
        self.game_over = False
        
        # Clear and recreate board
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        # Create buttons for each cell
        self.buttons = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                btn = tk.Button(self.board_frame, text="", font=('Arial', 12, 'bold'), 
                               width=3, height=2, command=lambda r=i, c=j: self.make_move(r, c),
                               bg='#ecf0f1', fg='#2c3e50', relief='raised', bd=2)
                btn.grid(row=i, column=j, padx=2, pady=2)
                row.append(btn)
            self.buttons.append(row)
        
        self.status_label.config(text="Your turn! Click a cell to make your move", foreground='#f39c12')
    
    def make_move(self, row, col):
        if self.game_over or self.board[row][col] != '.':
            return
        
        # Human move
        self.board[row][col] = 'X'
        self.buttons[row][col].config(text='X', fg='#e74c3c', state='disabled')
        
        # Check for human win
        if self.game_module.check_win(self.board, 'X', self.win_length):
            self.status_label.config(text="🎉 You Win! Congratulations!", foreground='#27ae60')
            self.game_over = True
            self.disable_all_buttons()
            return
        
        # Check for draw
        if self.game_module.is_full(self.board):
            self.status_label.config(text="🤝 It's a Draw!", foreground='#f39c12')
            self.game_over = True
            self.disable_all_buttons()
            return
        
        # AI move
        self.status_label.config(text="🤖 AI is thinking...", foreground='#3498db')
        self.window.update()
        
        self.game_module.ai_move(self.board)
        
        # Find AI's move and update button
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == 'O' and self.buttons[i][j]['text'] == '':
                    self.buttons[i][j].config(text='O', fg='#3498db', state='disabled')
                    break
        
        # Check for AI win
        if self.game_module.check_win(self.board, 'O', self.win_length):
            self.status_label.config(text="🤖 AI Wins! Better luck next time!", foreground='#e74c3c')
            self.game_over = True
            self.disable_all_buttons()
            return
        
        # Check for draw
        if self.game_module.is_full(self.board):
            self.status_label.config(text="🤝 It's a Draw!", foreground='#f39c12')
            self.game_over = True
            self.disable_all_buttons()
            return
        
        self.status_label.config(text="Your turn! Click a cell to make your move", foreground='#f39c12')
    
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
