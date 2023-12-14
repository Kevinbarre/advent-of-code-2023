def part1(lines):
    grid = tilt_north(lines)
    return get_load(grid)


def part2(lines):
    return 0


def transpose_grid(grid):
    return [''.join(column) for column in zip(*grid)]


def sort_row(row):
    return ''.join(sorted(row, reverse=True))


def sort_full_row(full_row):
    return '#'.join(sort_row(row) for row in full_row.split('#'))


def tilt_north(grid):
    transposed = transpose_grid(grid)
    transposed = [sort_full_row(full_row) for full_row in transposed]
    return transpose_grid(transposed)


def get_load(grid):
    total = 0
    depth = len(grid)
    for j, row in enumerate(grid):
        total += sum(depth - j for rock in row if rock == "O")
    return total


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
