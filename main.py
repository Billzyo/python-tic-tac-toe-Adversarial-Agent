import L4 as l4
from gui_app import main as gui_main

def console_menu():
    """Original console-based menu (kept for compatibility)"""
    while True:
        print("\n=== Tic Tac Toe ===")
        print("1. Play Tic Tac Toe (console)")
        print("2. Launch GUI")
        print("0. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            print("\n--- Tic Tac Toe (Console) ---")
            l4.tic_tac_toe_game()
        elif choice == '2':
            print("Launching GUI...")
            gui_main()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 0, 1, or 2.")

if __name__ == "__main__":
    # Launch GUI by default, but allow console mode
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--console':
        console_menu()
    else:
        try:
            gui_main()
        except ImportError as e:
            print(f"GUI not available: {e}")
            print("Falling back to console mode...")
            console_menu()
