f = open("level3_5.in", "r")
g = open("output.txt", "w")
N = int(f.readline())
prices = []
for i in range(N):
    prices.append(int(f.readline()))
tasks = []
M = int(f.readline())
for i in range(M):
    input_string = f.readline().split()
    task = {'id': int(input_string[0]), 'power': int(input_string[1]), 'start_interval': int(input_string[2]), 'end_interval': int(input_string[3]), 'minute_id': -1, 'min_cost': 999999999999999999999999999999}
    tasks.append(task)
for task in tasks:
    for i in range(task['start_interval'], task['end_interval']+1):
        temp_cost = prices[i] * task['power']
        if temp_cost < task['min_cost']:
            task['min_cost'] = temp_cost
            task['minute_id'] = i
g.write(str(M) + '\n')
for task in tasks:
    g.write(str(task['id']) + ' ' + str(task['minute_id']) + ' ' + str(task['power']) + '\n')
