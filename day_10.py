from aoc_util import *
from collections import deque

# Labelling 0 -> N, 1 -> E, 2 -> S, 3 -> W
n_c_map = {
    "|": "NS",
    "-": "EW",
    "L": "NE",
    "J": "NW",
    "7": "SW",
    "F": "SE",
    ".": "",
    "S": "NSEW",
    "\n": "",
}
c_delta_map = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "E": (1, 0)}
n_delta_map = {k: [c_delta_map[c] for c in v] for k, v in n_c_map.items()}


def inv_map(kv):
    return {v: k for k, v in kv.items()}


def all_neighbours(point):
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    return [(point[0] + d[0], point[1] + d[1]) for d in deltas]


def grid_dim(grid):
    w, h = len(grid[0]), len(grid)
    return w, h


def possible_neighbour_points(point):
    i, j = point
    c = grid[j][i]
    deltas = n_delta_map[c]
    return [(point[0] + d[0], point[1] + d[1]) for d in deltas]


def points_connected(p1, p2):
    return p1 in possible_neighbour_points(p2)


def in_bounds(i, j, grid):
    w, h = grid_dim(grid)
    return i >= 0 and i < w and j >= 0 and j < h


def grid_generator(grid):
    for j, r in enumerate(grid):
        for i, c in enumerate(r):
            yield (i, j, c)


def s_coord(grid):
    for i, j, c in grid_generator(grid):
        if c == "S":
            return (i, j)


def fix_s_deltas(s_coord):
    actual_s_deltas = []
    for n in possible_neighbour_points(s_coord):
        if s_coord in possible_neighbour_points(n):
            actual_s_deltas.append((n[0] - s_coord[0], n[1] - s_coord[1]))
    n_delta_map["S"] = actual_s_deltas
    print(actual_s_deltas)


grid = [list(s.strip()) for s in load_input(10)]
start = s_coord(grid)
fix_s_deltas(start)

# Vanilla BFS with depth-tracking
seen = set()
current = start
queue = deque([(start, 0)])
cost_map = dict()
while queue:
    (n, c) = queue.pop()
    if not n in seen:
        seen.add(n)
        cost_map[n] = c
        ns = possible_neighbour_points(n)
        neighbours = [(neigh, c + 1) for neigh in ns]
        queue.extendleft(neighbours)

max_cost_node = max(cost_map, key=lambda x: cost_map[x])
print(max_cost_node)
part_1 = cost_map[max_cost_node]
print(part_1)

# Cleans up the grid to clarify problem
for i, j, c in grid_generator(grid):
    if (i, j) not in seen:
        grid[j][i] = "."
new_grid = ["".join(l) for l in grid]
with open("inputs/day-10-cleaned.txt", "w") as f:
    for l in new_grid:
        f.write(l + "\n")

# Idea: 'blow up' the grid, adding extra tiles between pipes that are pushed together. Then you can just floodfill
# To compute the final area you will have to filter out these 'new' tiles

blown_up_grid = []
for l in new_grid:
    new_l = list(",".join(l.strip()))
    blown_up_grid.append(new_l)
    blown_up_grid.append(list("," * len(new_l)))

blown_up_grid.pop()

for j, r in enumerate(grid):
    for i, c in enumerate(r):
        if i < len(r) - 1 and points_connected((i, j), (i + 1, j)):
            blown_up_grid[2 * j][2 * i + 1] = "-"
        if j < len(grid) - 1 and points_connected((i, j), (i, j + 1)):
            blown_up_grid[2 * j + 1][2 * i] = "|"


bu_w, bu_h = grid_dim(blown_up_grid)

padded_grid = [
    ["," for _ in range(bu_w + 2)],
    *[[","] + l + [","] for l in blown_up_grid],
    ["," for _ in range(bu_w + 2)],
]


# print(padded_grid)
for l in padded_grid:
    print("".join(l))


# Vanilla BFS with depth-tracking
seen = set()
current = (0, 0)
queue = deque([start])
p_w, p_h = grid_dim(blown_up_grid)

while queue:
    n = queue.pop()
    if not n in seen:
        seen.add(n)
        for (i, j) in all_neighbours(n):
            if in_bounds(i, j, padded_grid):
                n_c = padded_grid[j][i]
                # print(n_c)
                if n_c == "." or n_c == ",":
                    queue.appendleft((i, j))

part_2 = 0
for i, j, c in grid_generator(padded_grid):
    if c == "." and (i, j) in seen:
        part_2 += 1
print(part_2)

# I am not proud about this one... I really don't see why I should count the dots that are in seen:
# is it not so that, starting at coordinate (0,0) in the padded grid this would count the dots
# outside not inside the structure?
