def part1(lines):
    grid = tilt_north(lines)
    return get_load(grid)


def part2(lines):
    grid = cycle_multiple_times(lines, 1000000000)
    return get_load(grid)


def transpose_grid(grid):
    return [''.join(column) for column in zip(*grid)]


def sort_row(row, reverse):
    return ''.join(sorted(row, reverse=reverse))


def sort_full_row(full_row, reverse=True):
    return '#'.join(sort_row(row, reverse) for row in full_row.split('#'))


def tilt_north(grid):
    transposed = transpose_grid(grid)
    transposed = [sort_full_row(full_row) for full_row in transposed]
    return transpose_grid(transposed)


def tilt_west(grid):
    return [sort_full_row(full_row) for full_row in grid]


def tilt_south(grid):
    transposed = transpose_grid(grid)
    transposed = [sort_full_row(full_row, False) for full_row in transposed]
    return transpose_grid(transposed)


def tilt_east(grid):
    return [sort_full_row(full_row, False) for full_row in grid]


def get_load(grid):
    total = 0
    depth = len(grid)
    for j, row in enumerate(grid):
        total += sum(depth - j for rock in row if rock == "O")
    return total


def cycle_once(grid):
    return tuple(tilt_east(tilt_south(tilt_west(tilt_north(grid)))))


def cycle_multiple_times(grid, nb_cycle):
    new_grid = tuple(grid)
    encountered_grids = {}
    for i in range(nb_cycle):
        if new_grid in encountered_grids:
            # Cycle found, no need to compute anymore cycles
            cycle_start = encountered_grids[new_grid]
            cycle_length = i - cycle_start
            final_index = ((nb_cycle - cycle_start) % cycle_length) + cycle_start
            target_grid = list(encountered_grids.keys())[
                list(encountered_grids.values()).index(final_index)]
            return target_grid
        else:
            encountered_grids[new_grid] = i
        new_grid = cycle_once(new_grid)
    return new_grid


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
