# Tic Tac Toe (with GUI and AI)

A Python project featuring a Tic-Tac-Toe game with both console and GUI interfaces. The GUI offers a clean, modern interface, and the AI opponent uses a minimax-based strategy.

## Features


# Tic Tac Toe (GUI + AI)

This repository contains a Tic-Tac-Toe implementation with both a modern Tkinter GUI and a console mode. The AI opponent is a minimax-based agent enhanced with alpha-beta pruning, move ordering, iterative deepening, and simple tactical checks.

## Highlights
- Play vs AI (minimax-based) or Player vs Player locally.
- Variable board sizes (4x4 up to 10x10).
- Simple, clean GUI with board size control and status messages.

## Requirements
- Python 3.8 or newer
- tkinter (bundled with standard Python on most installs)
- See `requirements.txt` for development and test tools (pytest, black, mypy, flake8).

## Quick start (Windows PowerShell)

1. Create and activate a virtual environment (recommended):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the GUI (recommended):

```powershell
python main.py
```

4. Or run the console mode:

```powershell
python main.py --console
```

## Running tests

If you add tests, place them under a `tests/` directory. To run tests locally:

```powershell
pip install pytest
pytest -q
```

## Suggested next improvements
- Add unit tests for `L4.py` (core game logic and AI tactics).
- Make AI moves run in a background thread so the GUI stays responsive during thinking.
- Highlight the winning line in the GUI and add undo/restart buttons.

## Project layout

```
.
├─ main.py           # Entry point (launches GUI by default)
├─ gui_app.py        # Tkinter GUI
├─ L4.py             # Game logic and AI
├─ L2.py, L3.py      # Supporting algorithms / examples
├─ requirements.txt  # dev & test dependencies
├─ README.md         # This file
```

## Contributing

- Open an issue for features or bugs.
- Keep changes small and focused; add tests for new behavior when possible.
- Follow formatting rules (`black`) and type-check with `mypy` as you improve code quality.

## License

This project is provided for educational purposes.
