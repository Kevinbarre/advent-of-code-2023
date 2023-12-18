from typing import NamedTuple


class Direction(NamedTuple):
    j: int
    i: int


UP = Direction(-1, 0)
DOWN = Direction(1, 0)
LEFT = Direction(0, -1)
RIGHT = Direction(0, 1)


class Color:
    def __init__(self, rgb_code):
        self.r = int(rgb_code[1:3], 16)
        self.g = int(rgb_code[3:5], 16)
        self.b = int(rgb_code[5:], 16)

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b


def part1(lines):
    instructions = parse_instructions(lines)
    trench = build_trench(instructions)
    return count_size(trench)


def part2(lines):
    instructions = parse_true_instructions(lines)
    return count_size_2(instructions)


def parse_instructions(lines):
    instructions = []
    for line in lines:
        raw_direction, length, color = line.split()
        match raw_direction:
            case 'U':
                direction = UP
            case 'D':
                direction = DOWN
            case 'L':
                direction = LEFT
            case _:  # R
                direction = RIGHT
        instructions.append((direction, int(length), Color(color[1:-1])))
    return instructions


def build_trench_right(trench, position, length):
    current_j, current_i = position
    current_row = trench[current_j]
    for i in range(1, length + 1):
        try:
            # Replace possible '.' with a '#'
            current_row[current_i + i] = '#'
        except IndexError:
            # Reach the end of the row, append '#' on current row, and '.' on all other rows
            for m, row in enumerate(trench):
                if m == current_j:
                    row.append('#')
                else:
                    row.append('.')
    return trench


def build_trench_left(trench, position, length):
    current_j, current_i = position
    current_row = trench[current_j]
    for i in range(1, length + 1):
        new_index = current_i - i
        if new_index >= 0:
            # Replace possible '.' with a '#'
            current_row[new_index] = '#'
        else:
            # Reach the beginning of the row, prepend '#' on current row, and '.' on all other rows
            for m, row in enumerate(trench):
                if m == current_j:
                    row.insert(0, '#')
                else:
                    row.insert(0, '.')
    return trench


def build_trench_down(trench, position, length):
    current_j, current_i = position
    for j in range(1, length + 1):
        try:
            # Replace possible '.' with a '#'
            trench[current_j + j][current_i] = '#'
        except IndexError:
            # Reach the end of the column, add new row with '#' on current column, and '.' everywhere else
            new_row = ['.' if i != current_i else '#' for i in range(len(trench[0]))]
            trench.append(new_row)
    return trench


def build_trench_up(trench, position, length):
    current_j, current_i = position
    for j in range(1, length + 1):
        new_index = current_j - j
        if new_index >= 0:
            # Replace possible '.' with a '#'
            trench[new_index][current_i] = '#'
        else:
            # Reach the beginning of the column, prepend new row with '#' on current column, and '.' everywhere else
            new_row = ['.' if i != current_i else '#' for i in range(len(trench[0]))]
            trench.insert(0, new_row)
    return trench


def build_trench(instructions):
    position = (0, 0)
    trench = [['#']]
    for direction, length, _ in instructions:
        if direction == RIGHT:
            trench = build_trench_right(trench, position, length)
            # Need to account going right on the grid
            position = (position[0], position[1] + length)
        elif direction == LEFT:
            trench = build_trench_left(trench, position, length)
            # Need to account going up on the grid
            position = (position[0], max(0, position[1] - length))
        elif direction == DOWN:
            trench = build_trench_down(trench, position, length)
            # Need to account going down on the grid
            position = (position[0] + length, position[1])
        else:  # UP
            trench = build_trench_up(trench, position, length)
            # Need to account going up on the grid
            position = (max(0, position[0] - length), position[1])
    return trench


def flood_fill(trench, position):
    to_visit = [position]
    visited = set()
    while to_visit:
        position = to_visit.pop()
        visited.add(position)
        j, i = position
        if j < 0 or i < 0:
            continue
        try:
            if trench[j][i] == '.':
                trench[j][i] = 'X'
                for direction in [UP, DOWN, LEFT, RIGHT]:
                    new_position = (position[0] + direction[0], position[1] + direction[1])
                    if new_position not in visited:
                        to_visit.append(new_position)
        except IndexError:
            # Out of bound, ignore this cell
            pass


def count_size(trench):
    height = len(trench)
    width = len(trench[0])
    for i in range(width):
        if trench[0][i] == '.':
            # Found an empty space on top border, flood from here
            flood_fill(trench, (0, i))
        if trench[height - 1][i] == '.':
            # Found an empty space on bottom border, flood from here
            flood_fill(trench, (height - 1, i))
    for j in range(height):
        if trench[j][0] == '.':
            # Found an empty space on left border, flood from here
            flood_fill(trench, (j, 0))
        if trench[j][width - 1] == '.':
            # Found an empty space on right border, flood from here
            flood_fill(trench, (j, width - 1))
    # Count remaining borders and cells not flooded
    return sum(1 for row in trench for cell in row if cell in ('#', '.'))


def parse_true_instructions(lines):
    instructions = []
    for line in lines:
        _, _, raw_color = line.split()
        raw_length, raw_direction = raw_color[2:-2], raw_color[-2]
        match raw_direction:
            case '0':
                direction = RIGHT
            case '1':
                direction = DOWN
            case '2':
                direction = LEFT
            case _:  # 3
                direction = UP
        instructions.append((direction, int(raw_length, 16), None))
    return instructions


def get_vertices_coordinates(instructions):
    vertices_coordinates = []
    current_point = (0, 0)
    for direction, length, _ in instructions:
        vertices_coordinates.append(current_point)
        current_point = tuple(current_point[i] + direction[i] * length for i in (0, 1))
    return vertices_coordinates


def shoelace(vertices_coordinates):
    area = 0
    for i in range(len(vertices_coordinates)):  # Compute last member first
        yi_1, xi_1 = vertices_coordinates[i - 1]
        yi, xi = vertices_coordinates[i]
        area += (xi_1 * yi - xi * yi_1)
    return abs(area) / 2


def get_perimeter(instructions):
    return sum(length for _, length, _ in instructions)


def count_size_2(instructions):
    inner_area = int(shoelace(get_vertices_coordinates(instructions)))
    boundary = get_perimeter(instructions)
    return inner_area + boundary // 2 + 1


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
