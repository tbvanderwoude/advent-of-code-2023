from aoc_util import *
import math


def solve_quad(a, b, c):
    D = b**2 - 4 * a * c
    x1 = (-b + math.sqrt(D)) / (2 * a)
    x2 = (-b - math.sqrt(D)) / (2 * a)
    return x1, x2


def break_record_bounds(time, dist):
    # This uses the following quadratic equation which follows
    # from equating the formula t_c * (t_tot - t_c) to d_record
    # - t_c ** 2 + t_c * t_tot - d_record = 0
    # a = -1, b = t_tot, c = -d_record
    x1, x2 = solve_quad(-1, time, -dist)
    return math.ceil(x1 + 1e-6), math.floor(x2 - 1e-6)


def compute_ways(time, dist):
    x1, x2 = break_record_bounds(time, dist)
    return x2 - x1 + 1


lines = load_input(6)
f = lambda x: read_numbers(x.split(":")[1])
g = lambda x: int("".join(map(str, x)))
times = f(lines[0])
distances = f(lines[1])
single_time = g(times)
single_distance = g(distances)

races = list(zip(times, distances))
part_1 = 1
for time, dist in races:
    part_1 *= compute_ways(time, dist)
print(part_1)
part_2 = compute_ways(single_time, single_distance)
print(part_2)
