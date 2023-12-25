from aoc_util import *

lines = load_input(12, True)

def construct_base_pattern(groups):
    tokens = ["#" * group for group in groups]
    return ".".join(tokens)


def is_match(ref, pat):
    return all([c_r == "?" or c_r == c_p for (c_r, c_p) in zip(ref, pat)])


def construct_patterns_len(groups, l, ref_p: str, first=True):
    if groups == []:
        return ["." * len(ref_p)]
    base_len = sum(groups) + len(groups) - 1
    budget = l - base_len
    if budget == 0:
        return [construct_base_pattern(groups)]
    elif budget < 0:
        return []
    else:
        h, t = groups[0], groups[1:]
        all_sols = []
        for i in range(budget):
            prefix = "." * i + "#" * h
            n_p = len(prefix)
            if is_match(ref_p[:n_p], prefix):
                tail_sol = construct_patterns_len(t, l - n_p, ref_p[n_p:])
                all_sols.extend([prefix + s for s in tail_sol])
        return all_sols
        # places = len(groups) + 2
        # print(f"To do: divide {budget} over {places} places")


for line in lines:
    pattern, groups = line.split(" ")
    l = len(pattern)
    groups = read_numbers(groups.replace(",", " "))
    # pattern = '.' + pattern + '.'
    print(pattern, groups)
    patterns = construct_patterns_len(groups, l, pattern)
    print(patterns)
    # print(construct_pattern_len(groups))
