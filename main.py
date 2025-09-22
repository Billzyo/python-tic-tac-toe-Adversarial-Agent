import L2 as l2
import L3 as l3
import L4 as l4

def main_menu():
    while True:
        print("\n=== Integrated Lab Games ===")
        print("1. Maze Game (BFS)")
        print("2. Maze Game (A*)")
        print("3. Tic Tac Toe (AI with minimax, variable size)")
        print("0. Exit")
        choice = input("Enter choice: ")

        if choice == '1':
            print("\n--- Maze BFS ---")
            l2.play_maze_bfs()
        elif choice == '2':
            print("\n--- Maze A* ---")
            l3.play_maze_astar()
        elif choice == '3':
            print("\n--- Tic Tac Toe ---")
            l4.tic_tac_toe_game()
        elif choice == '0':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please select 0, 1, 2, or 3.")

if __name__ == "__main__":
    main_menu()
