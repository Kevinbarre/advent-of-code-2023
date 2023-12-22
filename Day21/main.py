from typing import NamedTuple


def part1(lines, steps):
    starting_position, garden = parse_garden(lines)
    return find_reachable_garden_plots(garden, starting_position, steps)


def part2(lines):
    return 0


class Direction(NamedTuple):
    j: int
    i: int


UP = Direction(-1, 0)
DOWN = Direction(1, 0)
LEFT = Direction(0, -1)
RIGHT = Direction(0, 1)


def parse_garden(lines):
    width = len(lines[0])
    border_row = [''.join('#' for i in range(width + 2))]
    # Add rocks around the garden
    garden = border_row + ['#' + row + '#' for row in lines] + border_row
    # Replace starting position with a garden plot
    for j, row in enumerate(garden):
        if 'S' in row:
            i = row.index('S')
            garden[j] = row[:i] + '.' + row[i + 1:]
            return (j, i), garden


def get_accessible_positions(garden, current_position):
    accessible_positions = set()
    for direction in [UP, DOWN, LEFT, RIGHT]:
        j = current_position[0] + direction[0]
        i = current_position[1] + direction[1]
        if garden[j][i] == '.':
            accessible_positions.add((j, i))
    return accessible_positions


def find_reachable_garden_plots(garden, starting_position, steps):
    odd_positions = set()
    even_positions = set()
    current_positions = {starting_position}
    for step in range(1, steps + 1):
        next_step_positions = set()
        for current_position in current_positions:
            accessible_positions = get_accessible_positions(garden, current_position)
            for accessible_position in accessible_positions:
                # If it's a new position, need to check it next step
                if accessible_position not in odd_positions and accessible_positions not in even_positions:
                    next_step_positions.add(accessible_position)
                # Add it to positions depending on the parity of current step
                if step % 2 == 0:
                    even_positions.add(accessible_position)
                else:  # step % 2 == 1
                    odd_positions.add(accessible_position)
        current_positions = next_step_positions
    return len(even_positions) if steps % 2 == 0 else len(odd_positions)


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines, 64))
    print("Part 2 : ", part2(f_lines))
