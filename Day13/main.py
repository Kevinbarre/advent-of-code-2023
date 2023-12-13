from itertools import combinations
from math import floor
from statistics import fmean


def part1(lines):
    patterns = parse_patterns(lines)
    return sum(get_summary(pattern) for pattern in patterns)


def part2(lines):
    return 0


def parse_patterns(lines):
    patterns = []
    pattern = []
    for line in lines:
        if line:
            pattern.append(line)
        else:
            patterns.append(pattern)
            # Reset current pattern
            pattern = []
    # Add final pattern
    patterns.append(pattern)
    return patterns


def find_distinct_rows(pattern):
    distinct_rows = {}
    for i, row in enumerate(pattern):
        distinct_rows.setdefault(row, []).append(i)

    return distinct_rows


def count_columns_before_horizontal_reflection(distinct_rows):
    # First find axis of the possible horizontal reflection
    possible_axes = {}
    for identical_rows in distinct_rows.values():
        if len(identical_rows) == 1:
            # Ignore rows that are uniques
            continue
        if len(identical_rows) % 2 == 0:
            # Even number of identical rows means they are all part of the reflection
            possible_axes.setdefault(fmean(identical_rows), []).extend(identical_rows)
        else:
            # Odd number of identical rows means we must choose one to be excluded
            for remaining_rows in combinations(identical_rows, len(identical_rows) - 1):
                possible_axes.setdefault(fmean(remaining_rows), []).extend(remaining_rows)
    for axis, identical_rows in possible_axes.items():
        if axis.is_integer():
            # Discard axes that are on a row, they must be between them
            continue
        # Check that all remaining isolated rows are on the same side of the axis
        isolated_rows = [isolated_row for other_rows in distinct_rows.values() for isolated_row in other_rows if
                         isolated_row not in identical_rows]
        if all(row < axis for row in isolated_rows) or all(row > axis for row in isolated_rows):
            # Need to count row 0 as well
            return floor(axis) + 1
    return 0


def transpose_pattern(pattern):
    return [''.join(column) for column in zip(*pattern)]


def get_summary(pattern):
    # Try horizontal first
    distinct_rows = find_distinct_rows(pattern)
    horizontal_count = count_columns_before_horizontal_reflection(distinct_rows)
    if horizontal_count:
        return horizontal_count * 100
    # Try vertical
    transposed = transpose_pattern(pattern)
    distinct_columns = find_distinct_rows(transposed)
    vertical_count = count_columns_before_horizontal_reflection(distinct_columns)
    return vertical_count


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
