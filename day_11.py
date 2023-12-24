from aoc_util import *


class Point:
    def __init__(self, i, j):
        self.i = i
        self.j = j

    def __add__(self, other):
        return Point(self.i + other.i, self.j + other.j)

    def __sub__(self, other):
        return Point(self.i - other.i, self.j - other.j)

    def __repr__(self):
        return f"({self.i},{self.j})"


class Grid:
    def __init__(self, grid):
        self.grid = [l.strip() for l in grid]
        self.galaxies = []
        for i, j, c in grid_generator(self.grid):
            if c == "#":
                self.galaxies.append(Point(i, j))
        self.empty_i = []
        self.empty_j = []
        for j, row in enumerate(self.get_rows()):
            if all([x == "." for x in row]):
                self.empty_j.append(j)

        for i, column in enumerate(self.get_columns()):
            if all([x == "." for x in column]):
                self.empty_i.append(i)

    def expanded_manhattan_dist(self, p1, p2, factor=2):
        min_i = min(p1.i, p2.i)
        min_j = min(p1.j, p2.j)
        max_i = max(p1.i, p2.i)
        max_j = max(p1.j, p2.j)
        dist = 0
        empty_is = [x for x in self.empty_i if x >= min_i and x <= max_i]
        empty_js = [x for x in self.empty_j if x >= min_j and x <= max_j]

        dist += max_i - min_i + len(empty_is) * (factor - 1)
        dist += max_j - min_j + len(empty_js) * (factor - 1)

        return dist

    def width(self):
        return len(self.grid[0])

    def height(self):
        return len(self.grid)

    def get_row(self, j):
        if j >= 0 and j < self.height():
            return self.grid[j]
        else:
            return None

    def get_column(self, i):
        if i >= 0 and i < self.width():
            return [r[i] for r in self.grid]
        else:
            return None

    def get_rows(self):
        for j in range(self.height()):
            yield self.get_row(j)

    def get_columns(self):
        for i in range(self.width()):
            yield self.get_column(i)


def all_pairs(l):
    for i in range(len(l)):
        for j in range(i + 1):
            yield (l[i], l[j])


lines = load_input(11)
grid = Grid(lines)

solver = lambda f: sum(
    [grid.expanded_manhattan_dist(p1, p2, f) for (p1, p2) in all_pairs(grid.galaxies)]
)
part_1 = solver(2)
part_2 = solver(1000000)
print(part_1)
print(part_2)
