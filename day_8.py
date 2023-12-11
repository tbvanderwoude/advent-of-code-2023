from aoc_util import *
import re
from itertools import cycle

def nodes_to_int(node: str):
    base = ord('A')
    l = [(ord(x) - base) * 26 ** i for (i,x) in enumerate(reversed(node))]
    return sum(l)


lines = load_input(8)

instructions = lines[0].strip()

connections = lines[2:]

desert_map = {}
for connection in connections:
    start, left, right = map(nodes_to_int,re.findall("\w+",connection))
    desert_map[start] = (left,right)

final = nodes_to_int("ZZZ")
start = nodes_to_int("AAA")

current = start

steps = 0
for i in cycle(instructions):
    if current == final:
        break
    else:
        if i == 'L':
            current = desert_map[current][0]
        elif i == 'R':
            current = desert_map[current][1]
        steps += 1
print(steps)
        
