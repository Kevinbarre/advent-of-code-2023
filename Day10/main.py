def part1(lines):
    tiles = parse_tiles(lines)
    return get_farthest_distance(tiles)


def part2(lines):
    tiles = parse_tiles(lines)
    return count_inside_loop(tiles)


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


def get_loop_positions(tiles):
    start_position = get_start_position(tiles)
    current_position = start_position
    next_position, last_position = find_connected_pipes(tiles, start_position)
    loop_positions = {start_position, next_position}
    while next_position != last_position:
        future_position = navigate(tiles, current_position, next_position)
        current_position = next_position
        next_position = future_position
        loop_positions.add(next_position)
    return loop_positions


def find_start_symbol(tiles):
    start_position = get_start_position(tiles)
    start_j, start_i = start_position
    first, last = find_connected_pipes(tiles, start_position)
    first_j, first_i = first
    last_j, last_i = last
    first_vector = (start_j - first_j, start_i - first_i)
    last_vector = (last_j - start_j, last_i - start_i)
    if first_vector == (-1, 0):
        # Coming to start by going up
        if last_vector == (-1, 0):
            # Exiting by going up
            return '|'
        elif last_vector == (0, -1):
            # Exiting by going left
            return '7'
        else:
            # Exiting by going right
            return 'F'
    elif first_vector == (1, 0):
        # Coming to start by going down
        if last_vector == (1, 0):
            # Exiting by going down
            return '|'
        elif last_vector == (0, -1):
            # Exiting by going left
            return 'J'
        else:
            # Exiting by going right
            return 'L'
    elif first_vector == (0, -1):
        # Coming to start by going left
        if last_vector == (0, -1):
            # Exiting by going left
            return '-'
        elif last_vector == (-1, 0):
            # Exiting by going up
            return 'L'
        else:
            # Exiting by going down
            return 'F'
    else:
        # Coming to start by going right
        if last_vector == (0, 1):
            # Exiting by going right
            return '-'
        elif last_vector == (-1, 0):
            # Exiting by going up
            return 'J'
        else:
            # Exiting by going down
            return '7'


def count_inside_loop(tiles):
    loop_positions = get_loop_positions(tiles)
    start_symbol = find_start_symbol(tiles)
    checked_symbols = ('|', 'F', '7')
    if start_symbol in ('|', 'F', '7'):
        # If start symbol should be one of the symbols we check, add it to the list
        checked_symbols = ('|', 'F', '7', 'S')
    count_inside = 0
    for j in range(0, len(tiles)):
        crossing_count = 0
        for i in range(0, len(tiles[0])):
            if (j, i) in loop_positions:
                if tiles[j][i] in checked_symbols:
                    # Crossed the loop
                    crossing_count += 1
            else:
                # Checking if current position is inside the loop (odd number of crossing)
                if crossing_count % 2 == 1:
                    count_inside += 1
    return count_inside


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
