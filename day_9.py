from aoc_util import *
from functools import reduce

def diff_seq(seq):
    return list(map(lambda x: x[1]-x[0], zip(seq,seq[1:])))
    

def construct_pyramid_until_zeroes(seq):
    if all([x == 0 for x in seq]):
        return [seq]
    else:
        delta = diff_seq(seq)
        return [seq] + construct_pyramid_until_zeroes(delta)


lines = load_input(9)
seqs = [read_numbers(l) for l in lines]

part_1 = 0
part_2 = 0
for seq in seqs:
    # print(seq)
    pyramid = construct_pyramid_until_zeroes(seq)
    # print(pyramid)
    new_element = sum([s[-1] for s in pyramid])
    prev_element = reduce(lambda x,y: y[0] - x, reversed(pyramid),0)

    # print(prev_element)
    part_1 += new_element
    part_2 += prev_element
print(part_1)
print(part_2)
