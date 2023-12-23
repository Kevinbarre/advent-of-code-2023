from typing import NamedTuple


def part1(lines):
    trail = parse_trail(lines)
    target_position = get_target_position(trail)
    paths = get_all_paths(trail, (1, 2), target_position)
    return max(len(path) for path in paths)


def part2(lines):
    trail = parse_trail(lines)
    trail = remove_slopes(trail)
    target_position = get_target_position(trail)
    intersections = get_intersections(trail, target_position)
    return get_longest_path_from_intersections(intersections, (1, 2), target_position)


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


def remove_slopes(trail):
    return [row.replace('^', '.').replace('v', '.').replace('<', '.').replace('>', '.') for row in trail]


def get_intersections(trail, target_position):
    start = (1, 2)
    second_position = (2, 2)
    intersections = {}
    remaining_intersections = {(start, second_position)}
    while remaining_intersections:
        intersection, next_position = remaining_intersections.pop()
        path_length = 0
        possible_paths = {(next_position, frozenset({intersection}))}
        while True:
            current_position, already_visited_cells = possible_paths.pop()
            path_length += 1
            if current_position == target_position:
                # Found path to the end, stopping here
                intersections.setdefault(intersection, set()).add((current_position, path_length))
                break
            possible_paths = navigate_trail(trail, current_position, already_visited_cells)
            if len(possible_paths) != 1:
                # Found an intersection, stopping here
                # Record new path to this intersection
                intersections.setdefault(intersection, set()).add((current_position, path_length))
                if current_position not in intersections:
                    # We've never visited this intersection before, try to visit each possible path
                    for possible_path, _ in possible_paths:
                        remaining_intersections.add((current_position, possible_path))
                # Also add reverse path
                intersections.setdefault(current_position, set()).add((intersection, path_length))
                break
    return intersections


def get_longest_path_from_intersections(intersections, start, end):
    longest_path = 0
    possible_paths = {(start, 0, frozenset())}
    while possible_paths:
        intersection, path_length, visited_intersections = possible_paths.pop()
        visited_intersections = visited_intersections.union({intersection})
        for future_intersection, additional_path_length in intersections[intersection]:
            new_length = path_length + additional_path_length
            if future_intersection == end:
                # Found a path to the end, check if it's currently the longest one
                if new_length > longest_path:
                    longest_path = new_length
            else:
                if future_intersection not in visited_intersections:
                    possible_paths.add((future_intersection, new_length, visited_intersections))
    return longest_path


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
