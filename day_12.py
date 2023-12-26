from aoc_util import *
from typing import List, Tuple

lines = load_input(12, True)

def construct_base_pattern(groups):
    tokens = ["#" * group for group in groups]
    return ".".join(tokens)


def is_match(ref, pat):
    return all([c_r == "?" or c_r == c_p for (c_r, c_p) in zip(ref, pat)])

result_map = dict()
def count_patterns_len(groups: Tuple[int], ref_p: str) -> int:
    if (groups, ref_p) in result_map:
        return result_map[(groups,ref_p)]
    else:
        l = len(ref_p)
        if groups == ():
            patt = "." * l
            return 1 if is_match(ref_p, patt) else 0
        base_len = sum(groups) + len(groups) - 1
        budget = l - base_len
        if budget == 0:
            base_pattern = construct_base_pattern(groups)
            return 1 if is_match(ref_p, base_pattern) else 0
        else:
            h, t = groups[0], groups[1:]
            all_counts = 0
            for i in range(budget+1):
                prefix = "." * i + "#" * h
                if len(groups) > 1:
                    prefix += '.'
                n_p = len(prefix)
                if is_match(ref_p[:n_p], prefix):
                    all_counts += count_patterns_len(t, ref_p[n_p:])
            result_map[(groups,ref_p)] = all_counts
            return all_counts


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
    groups = tuple(read_numbers(groups.replace(",", " ")))
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
    groups = tuple(groups * 5)
    n_alt = count_patterns_len(groups, pattern)
    part_2 += n_alt
print(f"Part 2: {part_2}")