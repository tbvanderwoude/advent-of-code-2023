from aoc_util import *
from typing import List

lines = load_input(12, True)

def construct_base_pattern(groups):
    tokens = ["#" * group for group in groups]
    return ".".join(tokens)


def is_match(ref, pat):
    return all([c_r == "?" or c_r == c_p for (c_r, c_p) in zip(ref, pat)])


def construct_patterns_len(groups: List[int], ref_p: str) -> List[str]:
    l = len(ref_p)
    if groups == []:
        patt = "." * l
        if is_match(ref_p,patt):
            return [patt]
        else:
            return []
    base_len = sum(groups) + len(groups) - 1
    budget = l - base_len
    if budget == 0:
        base_pattern = construct_base_pattern(groups)
        if is_match(ref_p,base_pattern):
            return [base_pattern]
        else:
            return []
    if budget < 0:
        return []
    else:
        h, t = groups[0], groups[1:]
        all_sols = []
        for i in range(budget+1):
            prefix = "." * i + "#" * h
            if len(groups) > 1:
                prefix += '.'
            n_p = len(prefix)
            if is_match(ref_p[:n_p], prefix):
                tail_sol = construct_patterns_len(t, ref_p[n_p:])
                all_sols.extend([prefix + s for s in tail_sol])
        return all_sols


part_1 = 0
for line in lines:
    pattern, groups = line.split(" ")
    l = len(pattern)
    groups = read_numbers(groups.replace(",", " "))
    patterns = construct_patterns_len(groups, pattern)
    n = len(patterns)
    part_1 += n
    for p in patterns:
        assert(len(p) == l)
print(f"Part 1: {part_1}")