import re

NUMBERS = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9"
}


def part1(lines):
    return sum(calibration_value(line) for line in lines)


def part2(lines):
    return sum(calibration_value_with_letters(line) for line in lines)


def calibration_value(line):
    matches = re.findall(r"\d", line)
    first_digit = matches[0]
    last_digit = matches[-1]
    result = int(first_digit + last_digit)
    return result


def calibration_value_with_letters(line):
    matches = re.findall(r"(?=(\d|one|two|three|four|five|six|seven|eight|nine))", line)
    first_digit = matches[0]
    first_digit = convert_to_digit(first_digit)
    last_digit = matches[-1]
    last_digit = convert_to_digit(last_digit)
    result = int(first_digit + last_digit)
    return result


def convert_to_digit(digit):
    if digit.isdigit():
        return digit
    else:
        return NUMBERS[digit]


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.readlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
