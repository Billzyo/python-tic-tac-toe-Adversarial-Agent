import tkinter as tk
from tkinter import ttk
from . import l4
import threading
import queue
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
        self._ui_queue = queue.Queue()
        self.root.after(100, self._process_ui_queue)
        self._move_flash_ms = 120
        self._win_blink_count = 4
        self._win_blink_ms = 300

        self.setup_main_menu()

    # ... keep the rest of GUI logic similar to previous file but using l4 from package


def main():
    root = tk.Tk()
    app = GameGUI(root)
    root.mainloop()
