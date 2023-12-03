from aoc_util import *
import re
import functools
from math import prod as product


def compute_min_game_bag(game):
    color_map = {"red": 0, "green": 1, "blue": 2}
    m0 = re.match("Game (\d+): (.+)", game)
    game_id = int(m0.group(1))
    game_text = m0.group(2)
    draws = game_text.split("; ")
    min_bag = [0, 0, 0]
    for draw in draws:
        colors = draw.split(", ")
        for c in colors:
            s = c.split(" ")
            count = int(s[0])
            color = s[1]
            index = color_map[color]
            min_bag[index] = max(min_bag[index], count)
    return game_id, min_bag


def compute_power(bag):
    return product(bag)


def possible_subbag(bag, game_bag):
    comp = [i >= j for (i, j) in zip(bag, game_bag)]
    return all(comp)


bag = [12, 13, 14]
lines = load_input(2)
part_1 = 0
part_2 = 0
for line in lines:
    game_id, min_bag = compute_min_game_bag(line)
    possible = possible_subbag(bag, min_bag)
    if possible:
        part_1 += game_id
    part_2 += compute_power(min_bag)
print(part_1)
print(part_2)
# print(text[:5])
