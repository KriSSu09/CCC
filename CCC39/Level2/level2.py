for i in range(1, 6):
    with open(f'level2_{i}.in') as f, open(f'level2_{i}.out', 'w') as out:
        N = int(f.readline())
        for _ in range(N):
            path = f.readline().strip()
            current_height = 0
            current_width = 0
            height_max = 0
            height_min = 0
            width_max = 0
            width_min = 0
            for direction in path:
                if direction == 'W':
                    current_height += 1
                elif direction == 'S':
                    current_height -= 1
                elif direction == 'A':
                    current_width -= 1
                elif direction == 'D':
                    current_width += 1
                height_max = max(height_max, current_height)
                height_min = min(height_min, current_height)
                width_max = max(width_max, current_width)
                width_min = min(width_min, current_width)
            height = height_max - height_min + 1
            width = width_max - width_min + 1
            out.write(f'{width} {height}\n')

