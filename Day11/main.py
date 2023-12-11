import itertools


def part1(lines):
    image = expand_space(lines)
    galaxies = find_galaxies(image)
    return sum(get_shortest_distance(first, second) for first, second in itertools.combinations(galaxies, 2))


def part2(lines, nb_expansions):
    expanded_rows, expanded_columns = get_expanded_rows_columns(lines)
    galaxies = find_galaxies(lines)
    return sum(get_shortest_distance_with_expansion(first, second, nb_expansions, expanded_rows, expanded_columns) for
               first, second in itertools.combinations(galaxies, 2))


def expand_space(image):
    expanded_image = []
    # Expand rows
    for row in image:
        if '#' in row:
            # Keep the row as is
            expanded_image.append(row)
        else:
            # Double the row
            expanded_image.append(row)
            expanded_image.append(row)
    # Expand columns
    nb_expanded_columns = 0  # Record how many times we expanded, to account for the offset in the column number
    for i in range(len(image[0])):
        if '#' in {row[i] for row in image}:
            # Keep the column as is
            continue
        else:
            # Double the column, taking into account already expanded columsn for the index
            expanded_column = i + nb_expanded_columns
            nb_expanded_columns += 1
            expanded_image = [row[:expanded_column] + '.' + row[expanded_column:] for row in expanded_image]

    return expanded_image


def find_galaxies(image):
    galaxies = set()
    for j in range(len(image)):
        for i in range(len(image[0])):
            if image[j][i] == '#':
                galaxies.add((j, i))
    return galaxies


def get_shortest_distance(first, second):
    first_j, first_i = first
    second_j, second_i = second
    return abs(first_j - second_j) + abs(first_i - second_i)


def get_shortest_distance_with_expansion(first, second, nb_expansions, expanded_rows, expanded_columns):
    first_j, first_i = first
    expanded_first_j, expanded_first_i = first
    second_j, second_i = second
    expanded_second_j, expanded_second_i = second
    for expanded_row in expanded_rows:
        if first_j > expanded_row:
            expanded_first_j += nb_expansions
        if second_j > expanded_row:
            expanded_second_j += nb_expansions
    for expanded_column in expanded_columns:
        if first_i > expanded_column:
            expanded_first_i += nb_expansions
        if second_i > expanded_column:
            expanded_second_i += nb_expansions
    return abs(expanded_first_j - expanded_second_j) + abs(expanded_first_i - expanded_second_i)


def get_expanded_rows_columns(image):
    expanded_rows = [j for j, row in enumerate(image) if '#' not in row]
    expanded_columns = [i for i in range(len(image[0])) if '#' not in {row[i] for row in image}]

    return expanded_rows, expanded_columns


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines, 999999))
