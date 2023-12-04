from aoc_util import *


def read_numbers(s):
    return list(map(int, s.strip().split()))


lines = load_input(4)
n = len(lines)
part_1 = 0
multipliers = [1 for _ in range(len(lines))]
for i, card_str in enumerate(lines):
    numbers = card_str.split(":")[1]
    x = numbers.split("|")
    winning, card = read_numbers(x[0]), read_numbers(x[1])
    y = sum([n in winning for n in card])
    if y > 0:
        score = 2 ** (y - 1)
        part_1 += score
        self_mult = multipliers[i]
        print(
            f"Card {i+1} ({self_mult} copies) is winning {self_mult} * {y} = {self_mult * y} new cards!"
        )
        for j in range(1, y + 1):
            if i + j < n:
                multipliers[i + j] += self_mult

print(part_1)
part_2 = sum(multipliers)
print(part_2)
