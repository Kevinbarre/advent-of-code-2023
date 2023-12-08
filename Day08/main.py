import itertools


def part1(lines):
    instructions, maps = parse_input(lines)
    return reach_zzz(instructions, maps)


def part2(lines):
    return 0


def parse_input(lines):
    instructions = lines[0]
    maps = {}
    for line in lines[2:]:
        raw_key, raw_values = line.split('=')
        raw_left, raw_right = raw_values.split(',')
        maps[raw_key.strip()] = (raw_left.strip()[1:], raw_right.strip()[:-1])
    return instructions, maps


def apply_instruction(instruction, current_position, maps):
    left, right = maps[current_position]
    if instruction == "L":
        return left
    else:
        return right


def reach_zzz(instructions, maps):
    current_position = "AAA"
    infinite_instructions = itertools.cycle(instructions)
    steps = 0
    while current_position != "ZZZ":
        current_position = apply_instruction(next(infinite_instructions), current_position, maps)
        steps += 1
    return steps


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
