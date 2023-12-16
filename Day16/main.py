from enum import Enum


class Direction(Enum):
    UP = 1,
    DOWN = 2,
    LEFT = 3,
    RIGHT = 4


def part1(lines):
    grid = parse_grid(lines)
    energized_grid = energize_grid(grid)
    return get_energized_count(energized_grid)


def part2(lines):
    return 0


def parse_grid(lines):
    width = len(lines[0])
    border_row = ''.join("Z" for _ in range(width + 2))
    return [border_row] + ['Z' + line + 'Z' for line in lines] + [border_row]


def get_beam_from_direction(j, i, direction):
    # Determine next cell depending on beam direction
    if direction == Direction.UP:
        j -= 1
    elif direction == Direction.DOWN:
        j += 1
    elif direction == Direction.LEFT:
        i -= 1
    else:  # Direction RIGHT
        i += 1
    return j, i, direction


def step_beam(grid, beam):
    j, i, direction = beam
    # Check content of current cell in grid
    cell = grid[j][i]
    if cell == '.':
        # Bean keeps moving forward
        return {get_beam_from_direction(j, i, direction)}
    elif cell == 'Z':
        # Reached border, destroy beam
        return set()
    elif cell == '|':
        if direction in (Direction.UP, Direction.DOWN):
            # Pointy end of vertical splitter, act as empty space
            return {get_beam_from_direction(j, i, direction)}
        else:
            # Flat end of vertical splitter, divide beam vertically into two
            return {get_beam_from_direction(j, i, Direction.UP), get_beam_from_direction(j, i, Direction.DOWN)}
    elif cell == '-':
        if direction in (Direction.LEFT, Direction.RIGHT):
            # Pointy end of horizontal splitter, act as empty space
            return {get_beam_from_direction(j, i, direction)}
        else:
            # Flat end of horizontal splitter, divide beam horizontally into two
            return {get_beam_from_direction(j, i, Direction.LEFT), get_beam_from_direction(j, i, Direction.RIGHT)}
    elif cell == '\\':
        if direction == Direction.UP:
            return {get_beam_from_direction(j, i, Direction.LEFT)}
        elif direction == Direction.DOWN:
            return {get_beam_from_direction(j, i, Direction.RIGHT)}
        elif direction == Direction.LEFT:
            return {get_beam_from_direction(j, i, Direction.UP)}
        else:  # Direction RIGHT
            return {get_beam_from_direction(j, i, Direction.DOWN)}
    else:  # cell '/'
        if direction == Direction.UP:
            return {get_beam_from_direction(j, i, Direction.RIGHT)}
        elif direction == Direction.DOWN:
            return {get_beam_from_direction(j, i, Direction.LEFT)}
        elif direction == Direction.LEFT:
            return {get_beam_from_direction(j, i, Direction.DOWN)}
        else:  # Direction RIGHT
            return {get_beam_from_direction(j, i, Direction.UP)}


def energize_grid(grid):
    energized_grid = [[char if char == 'Z' else '.' for char in row] for row in grid]
    beams_history = set()
    beams = {(1, 1, Direction.RIGHT)}
    while beams:
        new_beams = set()
        for beam in beams:
            # Remember this bean already existed
            beams_history.add(beam)
            # Energize cell where beam is at
            j, i, _ = beam
            # Do not energize cells outside of initial grid
            if energized_grid[j][i] != 'Z':
                energized_grid[j][i] = '#'
            # Compute next step beams
            next_step_beams = step_beam(grid, beam)
            for new_beam in next_step_beams:
                if new_beam not in beams_history:
                    new_beams.add(new_beam)
        beams = new_beams
    return [''.join(char for char in line) for line in energized_grid]


def get_energized_count(energized_grid):
    return sum(1 for row in energized_grid for char in row if char == '#')


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
