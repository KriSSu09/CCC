import threading


def is_path_valid(width, height, lawn, path):
    free_cells = sum(row.count('.') for row in lawn)

    if len(path) + 1 != free_cells:
        return False

    valid = False
    for i in range(height):
        for j in range(width):
            if lawn[i][j] != '.':
                continue

            x, y = i, j
            visited = set()
            visited.add((x, y))
            path_valid = True

            for direction in path:
                if direction == 'W':
                    x -= 1
                elif direction == 'S':
                    x += 1
                elif direction == 'A':
                    y -= 1
                elif direction == 'D':
                    y += 1
                if not (0 <= x < height and 0 <= y < width and lawn[x][y] == '.' and (x, y) not in visited):
                    path_valid = False
                    break
                visited.add((x, y))

            if path_valid and len(visited) == free_cells:
                valid = True
                break
        if valid:
            break
    return valid


def dfs(x, y, width, height, lawn, path, visited, result):
    directions = [('D', 0, 1), ('S', 1, 0), ('A', 0, -1), ('W', -1, 0)]
    free_cells = sum(row.count('.') for row in lawn)
    if len(path) + 1 == free_cells:
        result.append(path)

    for dir_char, dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < height and 0 <= ny < width and not visited[nx][ny] and lawn[nx][ny] == '.':
            visited[nx][ny] = True
            dfs(nx, ny, width, height, lawn, path + dir_char, visited, result)
            if result:
                return  # Early return if one thread finds a valid path
            visited[nx][ny] = False


def find_valid_path(width, height, lawn):
    path = ''
    visited = [[False if cell == '.' else True for cell in row] for row in lawn]

    tree_location = next((i, j) for i in range(height) for j in range(width) if lawn[i][j] == 'X')
    start_x = tree_location[0] + 1
    start_y = tree_location[1]
    visited[start_x][start_y] = True

    # Loop around the tree initially
    directions = [('D', 0, 1), ('S', 1, 0), ('A', 0, -1), ('W', -1, 0)]
    loop_around_tree = [2, 3, 3, 0, 0, 1, 1]
    for direction in loop_around_tree:
        dx, dy = directions[direction][1:]
        start_x += dx
        start_y += dy
        path += directions[direction][0]
        visited[start_x][start_y] = True

    # Start two DFS threads from the current position
    result = []
    thread1 = threading.Thread(target=dfs,
                               args=(start_x, start_y, width, height, lawn, path, [row[:] for row in visited], result))
    thread2 = threading.Thread(target=dfs, args=(
        start_x, start_y + 1, width, height, lawn, path, [row[:] for row in visited], result))

    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()

    return result[0] if result else None


for test in range(1, 6):
    print(test)
    with open(f'level4_{test}.in') as f, open(f'level4_{test}.out', 'w') as out:
        N = int(f.readline())
        for bares in range(N):
            print(bares)
            width, height = map(int, f.readline().split())
            lawn = [f.readline().strip() for _ in range(height)]
            valid_path = find_valid_path(width, height, lawn)
            out.write(f'{valid_path}\n' if valid_path else 'No valid path found\n')
