from collections import Counter

for i in range(1, 6):
    with open(f'level1_{i}.in') as f:
        N = int(f.readline())
        for _ in range(N):
            path = f.readline().strip()
            counts = Counter(path)
            output = f"{counts['W']} {counts['D']} {counts['S']} {counts['A']}"
            with open(f'level1_{i}.out', 'a') as out:
                out.write(output + '\n')
            # print(output)
