from aoc_util import *
import re
from itertools import product
from collections import defaultdict


class Grid:
    def __init__(self, rows):
        self.rows = rows
        self.w = len(rows[0])
        self.h = len(rows)

    def get(self, i, j):
        if i < self.w and i >= 0 and j < self.h and j >= 0:
            return self.rows[j][i]
        else:
            return "."

    def get_word_neighborhood(self, i, j, w):
        i_vals = range(i - 1, i + w + 1)
        j_vals = range(j - 1, j + 2)
        neighbours = [(k, l, self.get(k, l)) for (k, l) in product(i_vals, j_vals)]
        return neighbours


lines = load_input(3)
grid = Grid(lines)

words = []
for j, line in enumerate(lines):
    for match in re.finditer(r"\d+", line):
        # help(match)
        i = match.start()
        word_str = match[0]
        words.append((i, j, word_str))


def contains_symbol(l):
    symbols = ["*", "/", "+", "#", "$", "%", "=", "-", "@", "&"]
    return any([x in symbols for (_, _, x) in l])


def get_stars(l):
    return [(i, j) for (i, j, x) in l if x == "*"]


def invert_map(m):
    inverse = defaultdict(list)
    for k in m:
        for v in m[k]:
            inverse[v].append(k)
    return inverse


part_1 = 0
word_star_map = defaultdict(list)
for i, j, word_str in words:
    n = grid.get_word_neighborhood(i, j, len(word_str))
    if contains_symbol(n):
        part_1 += int(word_str)
        stars = get_stars(n)
        # Before, the problem was that part numbers aren't unique so that
        # a map using the part number as key will not work
        # if word_star_map[word_str]!=[]:
        #     raise Exception("Help!")
        word_star_map[(i, j, word_str)] = stars
print(part_1)

star_word_map = invert_map(word_star_map)

part_2 = 0
for k, v in star_word_map.items():
    if len(v) == 2:
        part_2 += int(v[0][2]) * int(v[1][2])

print(part_2)
