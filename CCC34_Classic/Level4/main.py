from functools import cmp_to_key


def find_lowest_task(tasks, price):
    for task in tasks:
        if task['power'] != 0:
            if task['start_interval'] <= price['minute'] <= task['end_interval']:
                return task
    return None


def find_lowest_price(prices, task):
    for price in prices:
        if price['power_draw'] < maxPower:
            if task['start_interval'] <= price['minute'] <= task['end_interval']:
                return price
    return None


def is_done(tasks):
    for task in tasks:
        if task['power'] !=0:
            return False
    return True


def add_in_power_draw(task, given_minute):
    for minute in task['power_draw']:
        if minute[0] == given_minute['minute']:
            minute[1] += 1
            return
    task['power_draw'].append([given_minute['minute'], 1])


f = open("level4_5.in", "r")
g = open("output.txt", "w")
maxPower = int(f.readline())
maxElectricityBill = int(f.readline())
N = int(f.readline())
prices = []
for i in range(N):
    temp_price = {'minute': i, 'price': int(f.readline()), 'power_draw': 0}
    prices.append(temp_price)
tasks = []
M = int(f.readline())
for i in range(M):
    input_string = f.readline().split()
    task = {'id': int(input_string[0]), 'power': int(input_string[1]), 'start_interval': int(input_string[2]), 'end_interval': int(input_string[3]), 'power_draw': [], 'min_cost': 999999999999999999999999999999}
    tasks.append(task)
prices = sorted(prices, key=cmp_to_key(
    lambda price1, price2: price1['price'] - price2['price']
))
current_bill = 0
# for price in prices:
#     while price['power_draw'] < maxPower:
#         current_task = find_lowest_task(tasks, price)
#         if current_task is None:
#             break
#         draw_time = 0
#         while current_task['power'] != 0 and price['power_draw'] < maxPower:
#             draw_time += 1
#             current_task['power'] -= 1
#             price['power_draw'] += 1
#         current_task['power_draw'].append([price['minute'], draw_time])
#         current_bill += price['price']*draw_time
while not is_done(tasks):
    for task in tasks:
        if task['power'] == 0:
            continue
        current_price = find_lowest_price(prices, task)
        if current_price is None:
            continue
        current_price['power_draw'] += 1
        task['power'] -= 1
        add_in_power_draw(task, current_price)
        current_bill += current_price['price']
if current_bill < maxElectricityBill:
    print(current_bill)
g.write(str(M) + '\n')
for task in tasks:
    g.write(str(task['id']) + ' ')
    for minute in task['power_draw']:
        g.write(str(minute[0]) + ' ' + str(minute[1]) + ' ')
    g.write('\n')
