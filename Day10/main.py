def part1(lines):
    tiles = parse_tiles(lines)
    return get_farthest_distance(tiles)


def part2(lines):
    return 0


def parse_tiles(lines):
    empty_row = ".".join("" for _ in range(0, len(lines[0]) + 3))
    tiles = ['.' + line + '.' for line in lines]
    return [empty_row] + tiles + [empty_row]


def get_start_position(tiles):
    for j, row in enumerate(tiles):
        for i, char in enumerate(row):
            if char == 'S':
                return j, i


def find_connected_pipes(tiles, start_position):
    j, i = start_position
    connected_pipes = []
    # Up
    tile = tiles[j - 1][i]
    if tile in ('|', 'F', '7'):
        connected_pipes.append((j - 1, i))
    # Down
    tile = tiles[j + 1][i]
    if tile in ('|', 'L', 'J'):
        connected_pipes.append((j + 1, i))
    # Left
    tile = tiles[j][i - 1]
    if tile in ('-', 'F', 'L'):
        connected_pipes.append((j, i - 1))
    # Right
    tile = tiles[j][i + 1]
    if tile in ('-', '7', 'J'):
        connected_pipes.append((j, i + 1))
    return connected_pipes


def navigate(tiles, current_position, next_position):
    current_j, current_i = current_position
    next_j, next_i = next_position
    current_move = (next_j - current_j, next_i - current_i)
    next_pipe = tiles[next_j][next_i]
    if current_move == (-1, 0):
        # Currently moving up
        if next_pipe == '|':
            # Continuing up
            return next_j - 1, next_i
        elif next_pipe == 'F':
            # Going right
            return next_j, next_i + 1
        else:
            # Going left
            return next_j, next_i - 1
    elif current_move == (1, 0):
        # Currently moving down
        if next_pipe == '|':
            # Continuing down
            return next_j + 1, next_i
        elif next_pipe == 'L':
            # Going right
            return next_j, next_i + 1
        else:
            # Going left
            return next_j, next_i - 1
    elif current_move == (0, -1):
        # Currently moving left
        if next_pipe == '-':
            # Continuing left
            return next_j, next_i - 1
        elif next_pipe == 'L':
            # Going up
            return next_j - 1, next_i
        else:
            # Going down
            return next_j + 1, next_i
    else:
        # Currently moving right
        if next_pipe == '-':
            # Continuing right
            return next_j, next_i + 1
        elif next_pipe == 'J':
            # Going up
            return next_j - 1, next_i
        else:
            # Going down
            return next_j + 1, next_i


def get_farthest_distance(tiles):
    start_position = get_start_position(tiles)
    current_position = start_position
    next_position, last_position = find_connected_pipes(tiles, start_position)
    loop_size = 1  # Already account for first step
    while next_position != last_position:
        future_position = navigate(tiles, current_position, next_position)
        current_position = next_position
        next_position = future_position
        loop_size += 1
    # Account for last step needed to reach again the start position
    return (loop_size + 1) // 2


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
