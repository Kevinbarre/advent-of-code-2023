from typing import NamedTuple


def part1(lines):
    trail = parse_trail(lines)
    target_position = get_target_position(trail)
    paths = get_all_paths(trail, (1, 2), target_position)
    return max(len(path) for path in paths)


def part2(lines):
    return 0


class Direction(NamedTuple):
    j: int
    i: int


UP = Direction(-1, 0)
DOWN = Direction(1, 0)
LEFT = Direction(0, -1)
RIGHT = Direction(0, 1)


def parse_trail(lines):
    width = len(lines[0])
    border_row = [''.join('#' for _ in range(width + 2))]
    return border_row + ['#' + row + '#' for row in lines] + border_row


def get_possible_steps(trail, current_position, already_visited_cells):
    possible_steps = set()
    current_cell = trail[current_position[0]][current_position[1]]
    if current_cell == '^':
        directions = [UP]
    elif current_cell == 'v':
        directions = [DOWN]
    elif current_cell == '<':
        directions = [LEFT]
    elif current_cell == '>':
        directions = [RIGHT]
    else:  # current_cell == '.'
        directions = [UP, DOWN, LEFT, RIGHT]
    for direction in directions:
        next_position = (current_position[0] + direction[0], current_position[1] + direction[1])
        if next_position in already_visited_cells:
            # Not allowed go on the same cell twice
            continue
        trail_cell = trail[next_position[0]][next_position[1]]
        if trail_cell != '#':
            possible_steps.add(next_position)
    return possible_steps


def navigate_trail(trail, current_position, already_visited_cells):
    future_paths = set()
    possible_steps = get_possible_steps(trail, current_position, already_visited_cells)
    for possible_step in possible_steps:
        future_paths.add((possible_step, already_visited_cells.union({current_position})))
    return future_paths


def get_all_paths(trail, starting_position, target_position):
    paths = set()
    possible_paths = {(starting_position, frozenset())}
    while possible_paths:
        current_position, already_visited_cells = possible_paths.pop()
        if current_position == target_position:
            # One possible path found
            paths.add(already_visited_cells)
        future_possible_paths = navigate_trail(trail, current_position, already_visited_cells)
        possible_paths.update(future_possible_paths)
    return paths


def get_target_position(trail):
    height = len(trail)
    width = len(trail[0])
    return height - 2, width - 3


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
