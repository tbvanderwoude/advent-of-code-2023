from aoc_util import *
from collections import deque 

# Labelling 0 -> N, 1 -> E, 2 -> S, 3 -> W
n_c_map = {'|': 'NS', '-': 'EW', 'L': 'NE', 'J': 'NW', '7': 'SW', 'F': 'SE', '.': '', 'S': 'NSEW', '\n': ''}
c_delta_map = {'N': (0,-1), 'S': (0,1), 'W': (-1,0), 'E': (1,0)}
n_delta_map = {k: [c_delta_map[c] for c in v] for k,v in n_c_map.items()}

def inv_map(kv):
    return {v: k for k,v in kv.items()}

def possible_neighbour_points(point):
    i,j = point
    c = grid[j][i]
    deltas = n_delta_map[c]
    return [(point[0] + d[0], point[1] + d[1]) for d in deltas]

def s_coord(grid):
    for (j,r) in enumerate(grid):
        for (i,c) in enumerate(r):
            if c == 'S':
                return (i,j)
            
def fix_s_deltas(s_coord):
    actual_s_deltas = []
    for n in possible_neighbour_points(s_coord):
        if s_coord in possible_neighbour_points(n):
            actual_s_deltas.append((s_coord[0]-n[0],s_coord[1] - n[1]))
    n_delta_map['S'] = actual_s_deltas

grid = load_input(10)
start = s_coord(grid)
fix_s_deltas(start)

# Vanilla BFS with depth-tracking
seen = set()
current = start
queue = deque([(start,0)])
cost_map = dict()
while queue:
    (n,c) = queue.pop()
    if not n in seen:
        seen.add(n)
        cost_map[n] = c
        ns = possible_neighbour_points(n)
        neighbours = [(neigh, c + 1) for neigh in ns]
        queue.extendleft(neighbours)

max_cost_node= max(cost_map, key=lambda x: cost_map[x])
print(max_cost_node)
part_1 = cost_map[max_cost_node]
print(part_1)
