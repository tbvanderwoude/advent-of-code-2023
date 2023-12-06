from aoc_util import *
from pprint import pprint
from itertools import permutations

class Range:
    def __init__(self, source, dest, length):
        self.source = source
        self.dest = dest
        self.length = length
    
    def contains(self, x):
        return self.source <= x < self.source + self.length
    
    def __repr__(self):
        return f"Range({self.source} - {self.source + self.length - 1} => {self.dest} - {self.dest + self.length - 1})"
    def map(self,x):
        if self.contains(x):
            return self.dest + (x - self.source)
        else:
            raise ValueError("Cannot map {x}")


class RangeMap:
    def __init__(self, from_name, to_name, ranges):
        self.from_name = from_name
        self.to_name = to_name
        self.ranges = ranges

    def get(self, i):
        for range in self.ranges:
            if range.contains(i):
                return range.map(i)
        return i

lines = load_input(5)

seeds = read_numbers(lines[0].split(':')[1])
pprint(seeds)

map_strs = " ".join(lines[2:]).split('\n \n ')
map_by_name = {}
for map_str in map_strs:
    lines = map_str.split('\n')
    from_name, to_name = lines[0].removesuffix(' map:').split('-to-')
    ranges = []
    for map in lines[1:]:
        numbers = read_numbers(map)
        ranges.append(Range(numbers[1],numbers[0],numbers[2]))
    range_map = RangeMap(from_name, to_name, ranges)
    map_by_name[from_name] = range_map

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
part_1 = min(locations)
print(part_1)
# print(maps_str)