def part1(lines):
    sequences = parse_sequences(lines)
    return sum(get_next_value(sequence) for sequence in sequences)


def part2(lines):
    sequences = parse_sequences(lines)
    return sum(get_previous_value(sequence) for sequence in sequences)


def parse_sequences(lines):
    return [list(map(int, line.split())) for line in lines]


def compute_differences(sequence):
    return [next_one - previous for previous, next_one in zip(sequence, sequence[1:])]


def get_all_differences(sequence):
    all_differences = []
    last_differences = sequence
    while not all(element == 0 for element in last_differences):
        last_differences = compute_differences(last_differences)
        all_differences.append(last_differences)
    return all_differences


def get_next_value(sequence):
    all_differences = get_all_differences(sequence)
    return sequence[-1] + sum(differences[-1] for differences in all_differences)


def get_previous_value(sequence):
    all_differences = get_all_differences(sequence)
    return sequence[0] - sum(differences[0] * ((-1) ** i) for i, differences in enumerate(all_differences))


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
