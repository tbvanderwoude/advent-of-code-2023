from aoc_util import *
import re
from itertools import cycle
from math import lcm


def nodes_to_int(node: str):
    base = ord("A")
    l = [(ord(x) - base) * 26 ** i for (i, x) in enumerate(reversed(node))]
    return sum(l)

def int_to_node_str(n):
    base = ord("A")
    chars = []
        
    f = lambda i: chr(n//(26 ** (2-i)) % 26 + ord("A"))
    return "".join([f(i) for i in range(3)])

def compute_steps_az(instructions: str, desert_map: dict[int, (int, int)]):
    final = nodes_to_int("ZZZ")
    start = nodes_to_int("AAA")

    current = start

    steps = 0
    for i in cycle(instructions):
        if current == final:
            break
        else:
            if i == "L":
                current = desert_map[current][0]
            elif i == "R":
                current = desert_map[current][1]
            steps += 1
    return steps


def compute_steps_to_zs(
    instructions: str, desert_map: dict[int, (int, int)], start: int
):
    seen = set()
    steps = 0
    steps_sequence = []
    current = start
    for i in cycle(instructions):
        # print(f"Step {steps}; Node {current_str}")
        is_end = current % 26 == 25
        if is_end:
            if current in seen:
                break
            else:
                seen.add(current)
                steps_sequence.append(steps)
        if i == "L":
            current = desert_map[current][0]
        elif i == "R":
            current = desert_map[current][1]
        steps += 1
    return steps_sequence


lines = load_input(8)

instructions = lines[0].strip()

connections = lines[2:]

# Construct map
desert_map = {}
for connection in connections:
    start, left, right = map(nodes_to_int, re.findall("\w+", connection))
    desert_map[start] = (left, right)

# Solve part 1
part_1 = compute_steps_az(instructions, desert_map)
print(part_1)

# Solve part 2
starts = list(filter(lambda x: x % 26 == 0, desert_map))

end_steps = [compute_steps_to_zs(instructions, desert_map, start)[0] for start in starts]

part_2 = lcm(*end_steps)
print(part_2)

# assert nodes_to_int("ABZ") % 26 == 25

# n = nodes_to_int("ABZ")
# node = int_to_node_str(n)
# print(n,node)