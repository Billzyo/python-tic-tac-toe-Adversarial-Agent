from collections import deque

movements = [(0, -1), (0, 1), (-1, 0), (1, 0)]

def bfs(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    queue = deque([start])
    visited = {start: None}
    visited_nodes = []
    
    while queue:
        current = queue.popleft()
        visited_nodes.append(current)
        if current == goal:
            break
        for dx, dy in movements:
            nx, ny = current[0]+dx, current[1]+dy
            if 0<=nx<rows and 0<=ny<cols and maze[nx][ny]!='#' and (nx,ny) not in visited:
                queue.append((nx,ny))
                visited[(nx,ny)] = current

    path = []
    if goal in visited:
        node = goal
        while node != start:
            path.append(node)
            node = visited[node]
        path.append(start)
        path.reverse()

    return path, visited_nodes

def visualize_path(maze, path, visited):
    visual_maze = [row[:] for row in maze]
    for x,y in visited:
        if visual_maze[x][y] not in ['S','G'] and (x,y) not in path:
            visual_maze[x][y] = 'o'
    for x,y in path:
        if visual_maze[x][y] not in ['S','G']:
            visual_maze[x][y] = '*'
    for row in visual_maze:
        print(' '.join(row))

def play_maze_bfs():
    maze = [['S','.','.','#'], ['#','#','.','#'], ['.','.','.','G']]
    start = (0,0)
    goal = (2,3)
    path, visited = bfs(maze,start,goal)
    print(f"Path: {path}")
    print(f"Visited nodes: {len(visited)}")
    visualize_path(maze,path,visited)

