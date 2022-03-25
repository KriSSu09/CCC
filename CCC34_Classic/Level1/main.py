f = open("level1_5.in", "r")
g = open("output.txt", "w")
N = int(f.readline())
prices = []
for i in range(N):
    prices.append(int(f.readline()))
g.write(str(prices.index(min(prices))))
