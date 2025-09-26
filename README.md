# Tic Tac Toe (with GUI and AI)

A Python project featuring a Tic-Tac-Toe game with both console and GUI interfaces. The GUI offers a clean, modern interface, and the AI opponent uses a minimax-based strategy.

## Features

### ❌⭕ Tic-Tac-Toe
- **Two Game Modes**:
  - 🤖 **AI Challenge**: Play against a minimax AI opponent
  - 👥 **Player vs Player**: Two players on one computer
- Variable board size (4x4 to 10x10)
- Interactive click-to-play interface
- Win detection for 4-in-a-row (or smaller for smaller boards)
- Clear turn indicators and game status

## Requirements
- Python 3.8+
- tkinter (included with Python)
  

## Getting Started

### GUI Mode (Recommended)
1. (Optional) Create and activate a virtual environment
   - Windows (PowerShell):
     ```bash
     python -m venv .venv
     .venv\\Scripts\\Activate.ps1
     ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run the GUI application
   ```bash
   python main.py
   ```

### Console Mode
If you prefer the original console interface:
```bash
python main.py --console
```

## Project Structure
```
.
├─ main.py           # Entry point (launches GUI by default)
├─ gui_app.py        # GUI application with modern interface
├─ L4.py             # Tic-Tac-Toe with minimax AI
├─ requirements.txt  # Python dependencies
├─ README.md         # This file
└─ __pycache__/      # Bytecode cache (generated)
```

## Configuration
- No configuration is required by default. If your scripts rely on environment variables or config files, document them here.

## Testing
- If you add tests, place them in a `tests/` directory and run with `pytest`:
  ```bash
  pip install pytest
  pytest -q
  ```

## Notes
- Keep functions well-documented with docstrings.
- Prefer descriptive variable and function names.
- Run `python -m pip install --upgrade pip` occasionally to keep pip up to date.

## License
This project is for educational purposes only.

```
MIT License
```
