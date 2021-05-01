import random
import statistics
import collections

"""
l = []

for x in range(100000000):
    l.append(random.randint(1, 10))

c = collections.Counter()

for item in l:
    c[item] += 1

"""
"""
c = collections.Counter()
for x in range(10000000):
    c[random.randint(1, 10)] += 1
"""  

ll = [[15,32,33,39,45],[28,29,35,41,44],[4,8,23,30,37],
      [13,18,22,30,40],[2,7,24,33,43],[12,13,14,33,44],
      [22,32,36,39,42],[15,28,39,41,42],[5,20,26,33,43],
      [1,2,43,44,45],[20,26,32,38,45],[21,27,28,32,43],
      [7,14,16,19,35],[3,6,16,18,39],[2,5,20,24,26],
      [1,7,24,27,33],[12,15,23,37,38],[4,16,30,35,36],
      [7,30,34,39,42],[21,23,32,35,38],[10,24,29,35,36],
      [1,15,18,20,34],[1,2,4,6,25],[23,26,38,40,41],
      [20,25,33,36,45],[1,5,9,23,45],[20,25,33,37,42],
      [2,11,12,25,35],[8,24,26,29,44],[5,9,13,29,35]]

c = collections.Counter()

for group in ll:
    for num in group:
        c[num] += 1