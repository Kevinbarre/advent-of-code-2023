from functools import cache


def part1(lines):
    records = parse_input(lines)
    return sum(count_arrangements(conditions, groups) for conditions, groups in records)


def part2(lines):
    records = parse_input(lines)
    records = [unfold(record) for record in records]
    return sum(count_arrangements(conditions, groups) for conditions, groups in records)


def parse_input(lines):
    records = []
    for line in lines:
        conditions, raw_groups = line.split()
        groups = tuple(map(int, (raw_groups.split(","))))
        records.append((conditions, groups))
    return records


def unfold(record):
    conditions, groups = record
    new_conditions = "?".join(conditions for _ in range(5))
    new_groups = groups * 5
    return new_conditions, new_groups


@cache
def count_arrangements(conditions, groups):
    # Empty conditions
    if len(conditions) == 0:
        if len(groups) == 0:
            # No more groups to fit means one possible arrangement
            return 1
        else:
            # No way to fit the remaining groups
            return 0
    # If the conditions is not big enough to fit all remaining groups, that's no more possible solution
    if len(conditions) < sum(groups):
        return 0
    first_char = conditions[0]
    if first_char == '.':
        # Remove "." in first position, as it would be the same without it
        return count_arrangements(conditions[1:], groups)
    elif first_char == '?':
        # Try both possible ways, with '.' (which is the same as without it) and with '#'
        return count_arrangements(conditions[1:], groups) + count_arrangements("#" + conditions[1:], groups)
    # Else, conditions starts with '#'
    # If there are no more groups to fit, that one possible arrangement
    if len(groups) == 0:
        return 1
    # Check if possible to fit first group
    first_group = groups[0]
    if len(conditions) < first_group:
        # Not enough chars remaining for the first group, stop here
        return 0
    if "." not in conditions[:first_group]:
        # Possible to fit first group
        if len(groups) == 1:
            # Ensure no more remaining identified damaged char
            if "#" not in conditions[first_group:]:
                return 1
            else:
                return 0
        # Ensure possible to split after first group
        if conditions[first_group] == '#':
            return 0
        # Else, either an actual ".", or a "?" that should be considered a "."
        # We check remaining conditions
        return count_arrangements(conditions[first_group + 1:], groups[1:])
    else:
        # Not possible to fit first group here, so it's not a possible arrangement
        return 0


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
