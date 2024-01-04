from aoc_util import *
from typing import List

def grids_from_lines(lines):
    grids = []
    line_accum = []
    for l in lines:
        l_s = l.strip()
        if l_s == '':
            grids.append(Grid(line_accum))
            line_accum = []
        else:
            line_accum.append(l_s)
    if line_accum != []:
        grids.append(Grid(line_accum))
    return grids

def get_grid_axes(grid: Grid):
    # x_symmetries = list(range(1,grid.width()-1))
    for row in grid.get_rows():
        print(f"Row: {row}")
        for x0 in range(grid.width()-1):
            print("-",row[:x0 + 1], row[x0:])
            # print(row[:x0+1], row[x0::-1])



lines = load_input(13)
grids: List[Grid] = grids_from_lines(lines)

print(grids)
for grid in grids[:2]:
    get_grid_axes(grid)