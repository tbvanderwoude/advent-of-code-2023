def load_input(day, strip_newline=False):
    try:
        with open(f"inputs/day-{day}.txt") as f:
            if strip_newline:
                return list(map(lambda s: s.strip(), f.readlines()))
            else:
                return f.readlines()
    except:
        print("Input file could not be read, did you copy it to inputs?")
        return []


def read_numbers(s):
    return list(map(int, s.strip().split()))


def grid_generator(grid):
    for j, r in enumerate(grid):
        for i, c in enumerate(r):
            yield (i, j, c)

class Grid:
    def __init__(self, grid):
        self.grid = [l.strip() for l in grid]

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
