import re


def part1(lines):
    return sum(calibration_value(line) for line in lines)


def part2(lines):
    return 0


def calibration_value(line):
    matches = re.findall(r"\d", line)
    first_digit = matches[0]
    last_digit = matches[-1]
    result = int(first_digit + last_digit)
    return result


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.readlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
