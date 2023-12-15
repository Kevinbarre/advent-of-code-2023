def part1(lines):
    steps = parse_steps(lines[0])
    return sum(hash_algorithm(step) for step in steps)


def part2(lines):
    return 0


def parse_steps(steps):
    return [step for step in steps.split(',')]


def hash_algorithm(string):
    current_value = 0
    for char in string:
        current_value += ord(char)
        current_value *= 17
        current_value %= 256
    return current_value


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
