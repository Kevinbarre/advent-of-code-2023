from typing import NamedTuple


def part1(lines, steps):
    starting_position, garden = parse_garden(lines)
    return find_reachable_garden_plots(garden, starting_position, steps)


def part2(lines, steps):
    garden_width = len(lines)
    first_three_points = find_first_three_points(lines)
    quadratic_coefficients = get_quadratic_coefficients(first_three_points)
    return get_positions(quadratic_coefficients, garden_width, steps)


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


def expand_garden(lines, n):
    garden_width = len(lines)
    multiplier = 2 * n + 1
    initial_starting_position = (0, 0)
    # Replace starting position with a garden plot
    for j, row in enumerate(lines):
        if 'S' in row:
            i = row.index('S')
            lines[j] = row[:i] + '.' + row[i + 1:]
            initial_starting_position = (i, j)
    # Expand garden horizontally
    garden = [row * multiplier for row in lines]
    # Expand garden vertically
    garden = garden * multiplier
    return (initial_starting_position[0] + n * garden_width, initial_starting_position[1] + n * garden_width), garden


def find_first_three_points(lines):
    garden_width = len(lines)
    start_position, garden = expand_garden(lines, 2)
    first = find_reachable_garden_plots(garden, start_position, garden_width // 2)
    second = find_reachable_garden_plots(garden, start_position, garden_width + garden_width // 2)
    third = find_reachable_garden_plots(garden, start_position, 2 * garden_width + garden_width // 2)
    return first, second, third


def get_quadratic_coefficients(first_three_points):
    first, second, third = first_three_points
    # f(x) = a*x^2 + b*x + c
    # f(1) = a + b + c
    # f(2) = 4a + 2b + c
    # f(3) = 9a + 3b + c
    # a = (f(3) - 2*f(2) + f(1)) // 2 = (9a + 3b + c - 8a - 4b - 2c + a + b + c) // 2 = (2a +0b + 0c) // 2 = a
    a = (third - 2 * second + first) // 2
    # b = f(2) - f(1) - 3a = 4a + 2b + c -a -b -c -3a = 0a + b + 0c = b
    b = (second - first - 3 * a)
    # c = f(1) - a - b = a + b + c - a - b = 0a + 0b + c = c
    c = first - a - b
    return a, b, c


def get_positions(quadratic_coefficients, garden_width, steps):
    a, b, c = quadratic_coefficients
    n = 1 + (steps - garden_width // 2) // garden_width
    return a * n ** 2 + b * n + c


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines, 64))
    print("Part 2 : ", part2(f_lines, 26501365))
