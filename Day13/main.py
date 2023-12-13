from itertools import combinations
from math import floor
from statistics import fmean


def part1(lines):
    patterns = parse_patterns(lines)
    return sum(get_summary(pattern) for pattern in patterns)


def part2(lines):
    patterns = parse_patterns(lines)
    return sum(find_smudge(pattern) for pattern in patterns)


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


def count_columns_before_horizontal_reflection(distinct_rows, ignored_axis):
    # First find axis of the possible horizontal reflection
    possible_axes = {}
    for identical_rows in distinct_rows.values():
        if len(identical_rows) == 1:
            # Ignore rows that are uniques
            continue
        else:
            # Need to check by pair
            for pair in combinations(identical_rows, 2):
                possible_axes.setdefault(fmean(pair), []).extend(pair)
    for axis, identical_rows in possible_axes.items():
        if axis.is_integer():
            # Discard axes that are on a row, they must be between them
            continue
        if floor(axis) + 1 == ignored_axis:
            # Discard ignored axis
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


def get_summary(pattern, ignored_value=None):
    # Try horizontal first
    distinct_rows = find_distinct_rows(pattern)
    ignored_horizontal = None
    if ignored_value and ignored_value % 100 == 0:
        # Need to ignore previously computed horizontal axis
        ignored_horizontal = ignored_value // 100
    horizontal_count = count_columns_before_horizontal_reflection(distinct_rows, ignored_horizontal)
    if horizontal_count:
        return horizontal_count * 100
    # Try vertical
    transposed = transpose_pattern(pattern)
    distinct_columns = find_distinct_rows(transposed)
    vertical_count = count_columns_before_horizontal_reflection(distinct_columns, ignored_value)
    return vertical_count


def fix_smudge(pattern, j, i):
    new_pattern = []
    for k, row in enumerate(pattern):
        if k != j:
            new_pattern.append(row)
        else:
            current_char = row[i]
            if current_char == '.':
                new_char = '#'
            else:
                new_char = '.'
            new_pattern.append(row[:i] + new_char + row[i + 1:])
    return new_pattern


def find_smudge(pattern):
    # First get summary of pattern without changing anything
    summary = get_summary(pattern)
    # Then try to update one element at a time, until it gives a non-zero summary
    for j in range(len(pattern)):
        for i in range(len(pattern[0])):
            new_pattern = fix_smudge(pattern, j, i)
            new_summary = get_summary(new_pattern, summary)
            if new_summary:
                return new_summary
    print("Error: No smudge found for pattern", pattern)
    return 0


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
