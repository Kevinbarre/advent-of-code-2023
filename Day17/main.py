import heapq
import math

UP = (-1, 0)
DOWN = (1, 0)
LEFT = (0, -1)
RIGHT = (0, 1)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]


def part1(lines):
    heat_map = parse_heat_map(lines)
    end_node = get_end_node(heat_map)
    return dijkstra(heat_map, (1, 1), end_node)


def part2(lines):
    return 0


def parse_heat_map(lines):
    width = len(lines[0])
    border_row = ['Z' for _ in range(width + 2)]
    padded_heath_map = [['Z'] + [int(cell) for cell in row] + ['Z'] for row in lines]
    return [border_row] + padded_heath_map + [border_row]


def get_neighbours(heat_map, position, direction_streak):
    j, i = position
    direction, streak = direction_streak
    neighbours = set()
    directions = list(DIRECTIONS)
    if streak == 3:
        # Already 3 steps in the same direction, next neighbour in this direction should not be offered
        directions.remove(direction)
    if direction:
        # Prevent reversing direction
        directions.remove((-direction[0], -direction[1]))
    for new_direction in directions:
        k, m = new_direction
        y, x = j + k, i + m
        if heat_map[y][x] != 'Z':
            direction_count = 1
            if new_direction == direction:
                direction_count += streak
            neighbours.add(((y, x), (new_direction, direction_count)))
    return neighbours


def dijkstra(heat_map, start, end):
    distances = {(start, (None, 0)): 0}
    next_cells = [(0, start, (None, 0), [])]
    while next_cells:
        cell_heat, cell_position, direction_streak, path = heapq.heappop(next_cells)
        if cell_position == end:
            # End reached, can return
            return cell_heat
        neighbours = get_neighbours(heat_map, cell_position, direction_streak)
        for neighbour, neighbour_direction_streak in neighbours:
            j, i = neighbour
            neighbour_distance = cell_heat + heat_map[j][i]
            if neighbour_distance < distances.get((neighbour, neighbour_direction_streak), math.inf):
                # Update known distances with the new one to neighbour from this direction & streak,
                # if it's lower than existing one
                distances[(neighbour, neighbour_direction_streak)] = neighbour_distance
                # Add neighbour to next_cells with its current direction, streak, and path used to reach it
                new_path = path + [(cell_position, direction_streak)]
                heapq.heappush(next_cells, (neighbour_distance, neighbour, neighbour_direction_streak, new_path))


def get_end_node(heat_map):
    end_j = len(heat_map) - 2
    end_i = len(heat_map[0]) - 2
    return end_j, end_i


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
