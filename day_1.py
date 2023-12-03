from aoc_util import *


def solver(text, allow_text_digits=False):
    digit_map = {
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
    }
    callibration_values = []
    for line in text:
        numbers = []
        i = 0
        for c in line:
            if c.isdecimal():
                numbers.append(c)
            if allow_text_digits:
                subline = line[i:]
                for digit in digit_map:
                    index = subline.find(digit)
                    if index != -1 and index == 0:
                        numbers.append(digit_map[digit])
                        continue
            i += 1
        # Strings of first and last number
        first = numbers[0]
        last = numbers[-1]
        cal_str = first + last
        callibration_values.append(int(cal_str))
    cal_sum = sum(callibration_values)
    print(cal_sum)


if __name__ == "__main__":
    text = load_input(1)
    solver(text)
    solver(text, True)
