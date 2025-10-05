import tkinter as tk
from tkinter import ttk
import threading
import queue
from tictactoe.presenter.game_presenter import GamePresenter
try:
    import winsound
except Exception:
    winsound = None

class GameGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("800x700")
        self.root.configure(bg='#2c3e50')
        
        # Presenter
        self.presenter = GamePresenter()
        
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
        # Queue used to schedule UI updates from worker threads
        self._ui_queue = queue.Queue()
        # Start a periodic UI queue processor
        self.root.after(100, self._process_ui_queue)

        self.setup_main_menu()
        # Animation & sound settings
        self._move_flash_ms = 120
        self._win_blink_count = 4
        self._win_blink_ms = 300
    
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
        self.board = self.presenter.create_board(self.size)
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
        # Play move sound and animate
        try:
            self._play_sound('move')
            self._animate_move(row, col, player='X')
        except Exception:
            pass
        
        # Check for human win
        if self.presenter.check_win(self.board, 'X', self.win_length):
            self.status_label.config(text="🎉 You Win! Congratulations!", foreground='#27ae60')
            self.game_over = True
            self.disable_all_buttons()
            return
        
        # Check for draw
        if self.presenter.is_full(self.board):
            self.status_label.config(text="🤝 It's a Draw!", foreground='#f39c12')
            self.game_over = True
            self.disable_all_buttons()
            return
        
        # AI move (non-blocking): run AI in a background thread and schedule UI update
        self.status_label.config(text="🤖 AI is thinking...", foreground='#3498db')

        def ai_worker(board_snapshot, result_queue):
            # Run AI on a copy to avoid partial state exposure
            b_copy = [row[:] for row in board_snapshot]
            self.presenter.ai_move(b_copy)
            # Put the resulting board into the queue for the main thread to apply
            result_queue.put(b_copy)

        threading.Thread(target=ai_worker, args=(self.board, self._ui_queue), daemon=True).start()

        # UI will be updated by _process_ui_queue when the worker finishes
        return
    
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
        if self.presenter.check_win(self.board, self.current_player, self.win_length):
            player_name = "Player 1" if self.current_player == 'X' else "Player 2"
            self.status_label.config(text=f"🎉 {player_name} Wins! Congratulations!", foreground='#27ae60')
            self.game_over = True
            self.disable_all_buttons()
            return
        
        # Check for draw
        if self.presenter.is_full(self.board):
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

    # --- Sound & animation helpers ---
    def _play_sound(self, kind: str) -> None:
        """Play a simple sound for events. On Windows use winsound; otherwise fallback to bell."""
        if winsound:
            if kind == 'move':
                winsound.MessageBeep(winsound.MB_OK)
            elif kind == 'win':
                winsound.MessageBeep(winsound.MB_ICONEXCLAMATION)
            elif kind == 'lose':
                winsound.MessageBeep(winsound.MB_ICONHAND)
        else:
            try:
                # fallback: beep via Tkinter
                self.root.bell()
            except Exception:
                pass

    def _animate_move(self, r: int, c: int, player: str) -> None:
        """Briefly flash the button background to emphasize the move."""
        btn = self.buttons[r][c]
        original_bg = btn.cget('bg')

        def flash(on: bool, remaining: int):
            try:
                btn.config(bg='#f1c40f' if on else original_bg)
                if remaining > 0:
                    self.root.after(self._move_flash_ms, flash, not on, remaining - 1)
            except Exception:
                pass

        flash(True, 1)

    def _find_winning_line(self, player: str):
        """Return list of coordinates for a winning line for player, or None."""
        size = len(self.board)
        wl = min(4, size)
        # Horizontal & vertical
        for r in range(size):
            for c in range(size - wl + 1):
                if all(self.board[r][c + i] == player for i in range(wl)):
                    return [(r, c + i) for i in range(wl)]
        for c in range(size):
            for r in range(size - wl + 1):
                if all(self.board[r + i][c] == player for i in range(wl)):
                    return [(r + i, c) for i in range(wl)]
        # Diagonals
        for r in range(size - wl + 1):
            for c in range(size - wl + 1):
                if all(self.board[r + i][c + i] == player for i in range(wl)):
                    return [(r + i, c + i) for i in range(wl)]
                if all(self.board[r + wl - 1 - i][c + i] == player for i in range(wl)):
                    return [(r + wl - 1 - i, c + i) for i in range(wl)]
        return None

    def _highlight_winning_line(self, coords):
        """Blink the winning buttons a few times."""
        if not coords:
            return

        def blink(count: int):
            try:
                for r, c in coords:
                    btn = self.buttons[r][c]
                    btn.config(bg='#2ecc71' if count % 2 == 0 else '#ecf0f1')
                if count < self._win_blink_count * 2:
                    self.root.after(self._win_blink_ms, blink, count + 1)
            except Exception:
                pass

        blink(0)

    def _process_ui_queue(self):
        """Process UI update tasks from worker threads."""
        try:
            while True:
                b_copy = self._ui_queue.get_nowait()
                # Apply differences from b_copy to self.board and buttons
                for i in range(self.size):
                    for j in range(self.size):
                        if self.board[i][j] != b_copy[i][j]:
                            self.board[i][j] = b_copy[i][j]
                            if b_copy[i][j] == 'O':
                                self.buttons[i][j].config(text='O', fg='#3498db', state='disabled')
                                # Animate AI move and play sound
                                try:
                                    self._play_sound('move')
                                    self._animate_move(i, j, player='O')
                                except Exception:
                                    pass
                # Check for AI win
                if self.presenter.check_win(self.board, 'O', self.win_length):
                    self.status_label.config(text="🤖 AI Wins! Better luck next time!", foreground='#e74c3c')
                    self.game_over = True
                    self.disable_all_buttons()
                    # Highlight winning line and play losing sound
                    try:
                        coords = self._find_winning_line('O')
                        if coords:
                            self._highlight_winning_line(coords)
                        self._play_sound('lose')
                    except Exception:
                        pass
                elif self.presenter.is_full(self.board):
                    self.status_label.config(text="🤝 It's a Draw!", foreground='#f39c12')
                    self.game_over = True
                    self.disable_all_buttons()
                else:
                    self.status_label.config(text="Your turn! Click a cell to make your move", foreground='#f39c12')
        except queue.Empty:
            pass
        finally:
            # Schedule next check
            self.root.after(100, self._process_ui_queue)


def main():
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
