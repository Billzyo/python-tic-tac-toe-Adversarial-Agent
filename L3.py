import heapq
import time

movements = [(0, -1), (0, 1), (-1, 0), (1, 0)]

def heuristic(current, goal):
    return abs(current[0]-goal[0]) + abs(current[1]-goal[1])

def a_star_search(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    open_set = []
    heapq.heappush(open_set,(0+heuristic(start,goal),0,start))
    came_from = {}
    g_score = {start:0}
    expanded_nodes = []

    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        expanded_nodes.append(current)
        if current == goal:
            break
        for dx,dy in movements:
            nx,ny = current[0]+dx,current[1]+dy
            if 0<=nx<rows and 0<=ny<cols and maze[nx][ny]!='#':
                neighbor=(nx,ny)
                tentative_g = current_g + 1
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    g_score[neighbor]=tentative_g
                    f_cost=tentative_g+heuristic(neighbor,goal)
                    heapq.heappush(open_set,(f_cost,tentative_g,neighbor))
                    came_from[neighbor]=current

    path=[]
    if goal in came_from or goal==start:
        node=goal
        while node!=start:
            path.append(node)
            node=came_from[node]
        path.append(start)
        path.reverse()
    return path, expanded_nodes, g_score.get(goal,float('inf'))

def visualize_path(maze,path,expanded):
    visual_maze=[row[:] for row in maze]
    for x,y in expanded:
        if visual_maze[x][y] not in ['S','G'] and (x,y) not in path:
            visual_maze[x][y]='o'
    for x,y in path:
        if visual_maze[x][y] not in ['S','G']:
            visual_maze[x][y]='*'
    for row in visual_maze:
        print(' '.join(row))

def play_maze_astar():
    maze = [['S','.','.','#'], ['#','#','.','#'], ['.','.','.','G']]
    start = (0,0)
    goal = (2,3)
    print("A* Search Results:")
    start_time = time.time()
    path, expanded, cost = a_star_search(maze,start,goal)
    end_time = time.time()
    print(f"Path: {path}")
    print(f"Nodes expanded: {len(expanded)}")
    print(f"Path cost: {cost}")
    print(f"Time taken: {end_time-start_time:.6f} sec")
    visualize_path(maze,path,expanded)

