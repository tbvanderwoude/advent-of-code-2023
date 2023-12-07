from aoc_util import *
from pprint import pprint
from itertools import permutations

class Interval:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    
    def contains(self, x):
        return self.a <= x and x <= self.b
    
    def overlap(self, other):
        return self.b >= other.a and self.a <= other.b
    
    def __add__(self, value):
        return Interval(self.a + value,self.b + value)
    
    def intersect(self, other):
        if self.overlap(other):
            return Interval(max(self.a,other.a),min(self.b,other.b))
        else:
            raise ValueError("There is no intersection")
        
    def __repr__(self):
        return f"[{self.a} - {self.b}]"
        
class Range:
    def __init__(self, source_interval, shift):
        self.source_interval = source_interval
        self.shift = shift
    
    def contains(self, x):
        return self.source_interval.contains(x)
    
    def map_val(self,x):
        if self.contains(x):
            return x + self.shift
        else:
            raise ValueError("Cannot map {x}")

    def map_interval(self,x):
        
        if self.contains(x):
            return x + self.shift
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
                return range.map_val(i)
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
        dest_start, source_start, width = read_numbers(map)
        interval = Interval(source_start,source_start + width - 1)
        shift = dest_start - source_start
        ranges.append(Range(interval,shift))
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

i_a = Interval(2,6)
i_b = Interval(5,10)
print(i_a.intersect(i_b))
# print(maps_str)