for in_file in range(1, 6):
    with open(f'level3_{in_file}.in') as f, open(f'level3_{in_file}.out', 'w') as out:
        N = int(f.readline())
        for _ in range(N):
            width, height = map(int, f.readline().split())
            lawn = [list(f.readline().strip()) for _ in range(height)]
            path = f.readline().strip()
            free_cells = sum(row.count('.') for row in lawn)

            if len(path) + 1 != free_cells:
                out.write('INVALID\n')
                continue

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
            out.write('VALID\n' if valid else 'INVALID\n')
