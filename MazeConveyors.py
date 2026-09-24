def maze_solver_with_conveyors(maze: list[list[str]]) -> dict:
    rows = len(maze)
    cols = len(maze[0])

    start = None
    end = None

    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == 'S':
                start = (r, c)
            elif maze[r][c] == 'E':
                end = (r, c)

    if start is None or end is None:
        return {"distance": -1, "path": []}

    distance = [[-1] * cols for _ in range(rows)]
    parent = [[None] * cols for _ in range(rows)]
    move_path = [[None] * cols for _ in range(rows)]

    queue = __import__('collections').deque([start])
    distance[start[0]][start[1]] = 0

    directions = [
        (-1, 0),
        (1, 0),
        (0, -1),
        (0, 1)
    ]

    conveyor = {
        '>': (0, 1),
        '<': (0, -1),
        '^': (-1, 0),
        'v': (1, 0)
    }

    while queue:
        r, c = queue.popleft()

        for dr, dc in directions:
            nr = r + dr
            nc = c + dc

            if not (0 <= nr < rows and 0 <= nc < cols):
                continue

            if maze[nr][nc] == '#':
                continue

            fr, fc = nr, nc
            path = [(nr, nc)]
            valid = True
            visited = set()

            while maze[fr][fc] in conveyor:
                if (fr, fc) in visited:
                    valid = False
                    break

                visited.add((fr, fc))

                dr, dc = conveyor[maze[fr][fc]]
                fr += dr
                fc += dc

                if not (0 <= fr < rows and 0 <= fc < cols):
                    valid = False
                    break

                if maze[fr][fc] == '#':
                    valid = False
                    break

                path.append((fr, fc))

            if not valid:
                continue

            if distance[fr][fc] == -1:
                distance[fr][fc] = distance[r][c] + 1
                parent[fr][fc] = (r, c)
                move_path[fr][fc] = path
                queue.append((fr, fc))

    if distance[end[0]][end[1]] == -1:
        return {"distance": -1, "path": []}

    path = []
    current = end

    while current != start:
        r, c = current

        for cell in reversed(move_path[r][c]):
            path.append(list(cell))

        current = parent[r][c]

    path.append(list(start))
    path.reverse()

    return {
        "distance": distance[end[0]][end[1]],
        "path": path
    }
    
    pass

if __name__ == "__main__":
    maze = [
        ['S', '.', '>', '>', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 2, 'path': [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4]]}

    maze = [
        ['S', '.', '>', '#', 'E'],
        ['#', '#', '#', '#', '#']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {"distance": -1, "path": []}


    maze = [
        ['S', '.', 'v', '.', 'E'],
        ['#', '#', 'v', '.', '#'],
        ['.', '.', 'v', '.', '.'],
        ['#', '#', '.', '.', '#'],
        ['.', '.', '.', '.', '.']
    ]
    result = maze_solver_with_conveyors(maze)
    print(result)
    #Output: {'distance': 7, 'path': [[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2], [3, 3], [2, 3], [1, 3], [0, 3], [0, 4]]}
