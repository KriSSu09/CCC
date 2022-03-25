f = open("level2_5.in", "r")
g = open("output.txt", "w")
N = int(f.readline())
prices = []
for i in range(N):
    prices.append(int(f.readline()))
tasks = []
M = int(f.readline())
for i in range(M):
    input_string = f.readline().split()
    task = {'id': int(input_string[0]), 'duration': int(input_string[1]), 'min_cost': 99999999999999999999999999999999, 'start_id': -1}
    tasks.append(task)
for i in range(N):
    temp_sum = prices[i]
    for task in tasks:
        if task['duration'] == 1:
            if temp_sum < task['min_cost']:
                task['min_cost'] = temp_sum
                task['start_id'] = i
    for j in range(i+1, N):
        temp_sum += prices[j]
        for task in tasks:
            if task['duration'] == j-i+1:
                if temp_sum < task['min_cost']:
                    task['min_cost'] = temp_sum
                    task['start_id'] = i
    print(i)
g.write(str(M) + '\n')
for task in tasks:
    g.write(str(task['id']) + ' ' + str(task['start_id']) + '\n')
