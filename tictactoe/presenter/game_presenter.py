from __future__ import annotations

# Presenter provides an interface between the View and the Model.
# It delegates logic to the Model while keeping the UI layer isolated
# from implementation details.

from tictactoe.model import l4 as model


class GamePresenter:
    def __init__(self):
        # Any session-specific state for coordinating view and model can be added here
        pass

    # Game setup and state
    def create_board(self, size: int = 8):
        return model.create_board(size)

    def is_full(self, board) -> bool:
        return model.is_full(board)

    def check_win(self, board, player: str, win_length: int):
        return model.check_win(board, player, win_length)

    # AI actions
    def ai_move(self, board, time_limit: float = 1.0):
        return model.ai_move(board, time_limit=time_limit)

    # Utilities exposed if needed by view
    def clear_cache(self):
        model.clear_transposition_table()

    def print_board(self, board) -> None:
        model.print_board(board)
