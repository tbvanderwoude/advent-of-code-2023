from aoc_util import *
from collections import deque

# Constructs
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


def all_neighbours(point):
    deltas = c_delta_map.values()
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


# Idea: 'blow up' the grid, adding extra tiles between pipes that are pushed together
# After adding some padding, the exterior of the grid can be flood-filled, leaving the remaining
# '.' tiles not seen during this flood-fill to lie inside the cycle
def construct_padded_expanded_grid(seen, grid):
    # Cleans up the grid so that the only tubes remaining form the cycle
    for i, j, _ in grid_generator(grid):
        if (i, j) not in seen:
            grid[j][i] = "."
    new_grid = ["".join(l) for l in grid]

    # Create blown-up grid with "," tiles in interstices
    blown_up_grid = []
    for l in new_grid:
        new_l = list(",".join(l.strip()))
        blown_up_grid.append(new_l)
        blown_up_grid.append(list("," * len(new_l)))

    blown_up_grid.pop()

    # Reconnects broken up pipes using horizontal and vertical pipe pieces
    for j, r in enumerate(grid):
        for i, c in enumerate(r):
            if i < len(r) - 1 and points_connected((i, j), (i + 1, j)):
                blown_up_grid[2 * j][2 * i + 1] = "-"
            if j < len(grid) - 1 and points_connected((i, j), (i, j + 1)):
                blown_up_grid[2 * j + 1][2 * i] = "|"

    bu_w, _ = grid_dim(blown_up_grid)

    padded_grid = [
        ["," for _ in range(bu_w + 2)],
        *[[","] + l + [","] for l in blown_up_grid],
        ["," for _ in range(bu_w + 2)],
    ]
    return padded_grid


# Breadth-first floodfill of grid keeping track of depth and using a given neigbhour
# map
def bf_floodfill(start, neighbour_function):
    seen = set()
    queue = deque([(start, 0)])
    cost_map = dict()
    while queue:
        (n, c) = queue.pop()
        if not n in seen:
            seen.add(n)
            cost_map[n] = c
            neighbours = neighbour_function(n, c)
            queue.extendleft(neighbours)
    return seen, cost_map


grid = [list(s.strip()) for s in load_input(10)]
start = s_coord(grid)
fix_s_deltas(start)

neighbour_func_1 = lambda n, c: [
    (neigh, c + 1) for neigh in possible_neighbour_points(n)
]
seen, cost_map = bf_floodfill(start, neighbour_func_1)

max_cost_node = max(cost_map, key=lambda x: cost_map[x])
part_1 = cost_map[max_cost_node]
print(part_1)

padded_grid = construct_padded_expanded_grid(seen, grid)

show_grid = False
if show_grid:
    for l in padded_grid:
        print("".join(l))

neighbour_func_2 = lambda n, _: [
    ((i, j), 0)
    for (i, j) in all_neighbours(n)
    if in_bounds(i, j, padded_grid) and padded_grid[j][i] in [".", ","]
]
seen, _ = bf_floodfill((0, 0), neighbour_func_2)

part_2 = 0
for i, j, c in grid_generator(padded_grid):
    if c == "." and (i, j) not in seen:
        part_2 += 1
print(part_2)
