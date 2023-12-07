from aoc_util import *
from pprint import pprint

# Note:


class Interval:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def contains(self, x):
        return self.a <= x and x < self.b

    def overlap(self, other):
        return self.b > other.a and self.a < other.b

    def __add__(self, value):
        return Interval(self.a + value, self.b + value)

    def intersect(self, other):
        if self.overlap(other):
            return Interval(max(self.a, other.a), min(self.b, other.b))
        else:
            raise ValueError("There is no intersection")

    def __repr__(self):
        return f"Interval({self.a} - {self.b})"


class Range:
    def __init__(self, source_interval, shift):
        self.source_interval = source_interval
        self.shift = shift

    def contains(self, x):
        return self.source_interval.contains(x)

    def map_val(self, x):
        if self.contains(x):
            return x + self.shift
        else:
            raise ValueError("Cannot map {x}")


class RangeMap:
    def __init__(self, from_name, to_name, ranges):
        self.from_name = from_name
        self.to_name = to_name
        self.ranges = list(sorted(ranges, key=lambda x: x.source_interval.a))

    def get(self, i):
        for range in self.ranges:
            if range.contains(i):
                return range.map_val(i)
        return i

    def apply_range_map(self, interval):
        overlaps = [
            (interval.intersect(x.source_interval), x.shift)
            for x in self.ranges
            if x.source_interval.overlap(interval)
        ]
        if overlaps == []:
            return [interval]

        additional_intervals = []

        if interval.a < overlaps[0][0].a:
            additional_intervals.append((Interval(interval.a, overlaps[0][0].a), 0))

        for i in range(len(overlaps) - 1):
            current = overlaps[i]
            next = overlaps[i + 1]
            current_end = current[0].b
            next_start = next[0].a
            if current_end != next_start:
                additional_intervals.append((Interval(current_end, next_start), 0))

        if interval.b > overlaps[-1][0].b:
            additional_intervals.append((Interval(overlaps[-1][0].b, interval.b), 0))

        all_intervals = additional_intervals + overlaps

        return [i + shift for (i, shift) in all_intervals]


def construct_map_dict(lines):
    map_strs = " ".join(lines[2:]).split("\n \n ")
    map_by_name = {}
    for map_str in map_strs:
        lines = map_str.split("\n")
        from_name, to_name = lines[0].removesuffix(" map:").split("-to-")
        ranges = []
        for m in lines[1:]:
            dest_start, source_start, width = read_numbers(m)
            interval = Interval(source_start, source_start + width)
            shift = dest_start - source_start
            ranges.append(Range(interval, shift))
        range_map = RangeMap(from_name, to_name, ranges)
        map_by_name[from_name] = range_map
    return map_by_name


def solve_part_1(seeds, map_by_name):
    locations = []
    for seed in seeds:
        map_name = "seed"
        val = seed
        while map_name in map_by_name:
            needed_map = map_by_name[map_name]
            # Set the new name of the map
            map_name = needed_map.to_name
            val = needed_map.get(val)
        # print(val)
        locations.append(val)
    return min(locations)


def solve_part_2(seed_intervals, map_by_name):
    intervals = seed_intervals
    map_name = "seed"
    while map_name in map_by_name:
        new_intervals = []
        needed_map = map_by_name[map_name]
        # Set the new name of the map
        map_name = needed_map.to_name
        for interval in intervals:
            new_intervals.extend(needed_map.apply_range_map(interval))
        intervals = new_intervals
    return min(intervals, key=lambda x: x.a).a


lines = load_input(5)

seeds = read_numbers(lines[0].split(":")[1])
seed_intervals = [Interval(a, a + b) for (a, b) in zip(seeds[0::2], seeds[1::2])]
map_by_name = construct_map_dict(lines)

part_1 = solve_part_1(seeds, map_by_name)
print(part_1)
part_2 = solve_part_2(seed_intervals, map_by_name)
print(part_2)
