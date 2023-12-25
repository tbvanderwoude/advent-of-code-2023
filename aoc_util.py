def load_input(day, strip_newline=False):
    try:
        with open(f"inputs/day-{day}.txt") as f:
            if strip_newline:
                return list(map(lambda s: s.strip(), f.readlines()))
            else:
                f.readlines()
    except:
        print("Input file could not be read, did you copy it to inputs?")
        return []


def read_numbers(s):
    return list(map(int, s.strip().split()))


def grid_generator(grid):
    for j, r in enumerate(grid):
        for i, c in enumerate(r):
            yield (i, j, c)
