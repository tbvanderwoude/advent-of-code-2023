from aoc_util import *
from typing import List

lines = load_input(12, True)

def construct_base_pattern(groups):
    tokens = ["#" * group for group in groups]
    return ".".join(tokens)


def is_match(ref, pat):
    return all([c_r == "?" or c_r == c_p for (c_r, c_p) in zip(ref, pat)])

result_map = dict()
def count_patterns_len(groups: List[int], ref_p: str) -> int:
    if (tuple(groups), ref_p) in  result_map:
        return result_map[(tuple(groups),ref_p)]
    else:
        l = len(ref_p)
        if groups == []:
            patt = "." * l
            if is_match(ref_p,patt):
                return 1
            else:
                return 0
        base_len = sum(groups) + len(groups) - 1
        budget = l - base_len
        if budget == 0:
            base_pattern = construct_base_pattern(groups)
            if is_match(ref_p,base_pattern):
                return 1
            else:
                return 0
        if budget < 0:
            return []
        else:
            h, t = groups[0], groups[1:]
            all_sols = 0
            for i in range(budget+1):
                prefix = "." * i + "#" * h
                if len(groups) > 1:
                    prefix += '.'
                n_p = len(prefix)
                if is_match(ref_p[:n_p], prefix):
                    tail_sol = count_patterns_len(t, ref_p[n_p:])
                    all_sols += tail_sol
            result_map[(tuple(groups),ref_p)] = all_sols
            return all_sols


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
    n_alt = count_patterns_len(groups, pattern)
    part_1 += n_alt
print(f"Part 1: {part_1}")
part_2 = 0
for line in lines:
    base_pattern, groups = line.split(" ")
    copies = [base_pattern for _ in range(5)]
    pattern = "?".join(copies)
    l = len(pattern)
    groups = read_numbers(groups.replace(",", " "))
    groups = groups * 5
    # print(pattern,groups)
    n_alt = count_patterns_len(groups, pattern)
    # print(n_alt)
    part_2 += n_alt
print(f"Part 1: {part_2}")