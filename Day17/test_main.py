import pytest

from main import part1, part2, parse_heat_map, dijkstra, get_neighbours, DOWN, UP, LEFT, RIGHT, get_end_node

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 102


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 0


def test_parse_heat_map():
    # Given
    lines = ["2413432311323",
             "3215453535623",
             "3255245654254",
             "3446585845452",
             "4546657867536",
             "1438598798454",
             "4457876987766",
             "3637877979653",
             "4654967986887",
             "4564679986453",
             "1224686865563",
             "2546548887735",
             "4322674655533"]
    # When
    result = parse_heat_map(lines)
    # Then
    assert result == [['Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z'],
                      ['Z', 2, 4, 1, 3, 4, 3, 2, 3, 1, 1, 3, 2, 3, 'Z'],
                      ['Z', 3, 2, 1, 5, 4, 5, 3, 5, 3, 5, 6, 2, 3, 'Z'],
                      ['Z', 3, 2, 5, 5, 2, 4, 5, 6, 5, 4, 2, 5, 4, 'Z'],
                      ['Z', 3, 4, 4, 6, 5, 8, 5, 8, 4, 5, 4, 5, 2, 'Z'],
                      ['Z', 4, 5, 4, 6, 6, 5, 7, 8, 6, 7, 5, 3, 6, 'Z'],
                      ['Z', 1, 4, 3, 8, 5, 9, 8, 7, 9, 8, 4, 5, 4, 'Z'],
                      ['Z', 4, 4, 5, 7, 8, 7, 6, 9, 8, 7, 7, 6, 6, 'Z'],
                      ['Z', 3, 6, 3, 7, 8, 7, 7, 9, 7, 9, 6, 5, 3, 'Z'],
                      ['Z', 4, 6, 5, 4, 9, 6, 7, 9, 8, 6, 8, 8, 7, 'Z'],
                      ['Z', 4, 5, 6, 4, 6, 7, 9, 9, 8, 6, 4, 5, 3, 'Z'],
                      ['Z', 1, 2, 2, 4, 6, 8, 6, 8, 6, 5, 5, 6, 3, 'Z'],
                      ['Z', 2, 5, 4, 6, 5, 4, 8, 8, 8, 7, 7, 3, 5, 'Z'],
                      ['Z', 4, 3, 2, 2, 6, 7, 4, 6, 5, 5, 5, 3, 3, 'Z'],
                      ['Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z']]


def test_get_neighbours():
    # Given
    heat_map = [['Z', 'Z', 'Z', 'Z', 'Z'],
                ['Z', 1, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 1, 'Z'],
                ['Z', 'Z', 'Z', 'Z', 'Z']]
    # When
    result = get_neighbours(heat_map, (2, 2), (None, 0))
    # Then
    assert result == {((1, 2), (UP, 1)),
                      ((3, 2), (DOWN, 1)),
                      ((2, 1), (LEFT, 1)),
                      ((2, 3), (RIGHT, 1))}


@pytest.mark.parametrize("position, expected", [
    ((1, 1), {((1, 2), (RIGHT, 1)), ((2, 1), (DOWN, 1))}),
    ((3, 3), {((2, 3), (UP, 1)), ((3, 2), (LEFT, 1))}),
    ((2, 1), {((1, 1), (UP, 1)), ((2, 2), (RIGHT, 1)), ((3, 1), (DOWN, 1))}),
    ((2, 3), {((1, 3), (UP, 1)), ((2, 2), (LEFT, 1)), ((3, 3), (DOWN, 1))})])
def test_get_neighbours_border(position, expected):
    # Given
    heat_map = [['Z', 'Z', 'Z', 'Z', 'Z'],
                ['Z', 1, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 1, 'Z'],
                ['Z', 'Z', 'Z', 'Z', 'Z']]
    # When
    result = get_neighbours(heat_map, position, (None, 0))
    # Then
    assert result == expected


def test_get_neighbours_streak():
    # Given
    heat_map = [['Z', 'Z', 'Z', 'Z', 'Z'],
                ['Z', 1, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 1, 'Z'],
                ['Z', 'Z', 'Z', 'Z', 'Z']]
    # When
    result = get_neighbours(heat_map, (4, 2), (DOWN, 3))
    # Then
    assert result == {((4, 1), (LEFT, 1)),
                      ((4, 3), (RIGHT, 1))}


def test_get_neighbours_increment_streak():
    # Given
    heat_map = [['Z', 'Z', 'Z', 'Z', 'Z'],
                ['Z', 1, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 1, 'Z'],
                ['Z', 'Z', 'Z', 'Z', 'Z']]
    # When
    result = get_neighbours(heat_map, (3, 2), (DOWN, 2))
    # Then
    assert result == {((3, 1), (LEFT, 1)),
                      ((3, 3), (RIGHT, 1)),
                      ((4, 2), (DOWN, 3))}


def test_dijkstra():
    # Given
    heat_map = [['Z', 'Z', 'Z', 'Z', 'Z'],
                ['Z', 1, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 1, 'Z'],
                ['Z', 'Z', 'Z', 'Z', 'Z']]
    # When
    result = dijkstra(heat_map, (1, 1), (3, 3))
    # Then
    assert result == 4


def test_dijkstra_at_most_three():
    # Given
    heat_map = [['Z', 'Z', 'Z', 'Z', 'Z'],
                ['Z', 1, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 1, 'Z'],
                ['Z', 'Z', 'Z', 'Z', 'Z']]
    # When
    result = dijkstra(heat_map, (1, 1), (5, 3))
    # Then
    assert result == 14


def test_dijkstra_higher_heat_first():
    # Given
    heat_map = [['Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z'],
                ['Z', 1, 1, 5, 9, 9, 'Z'],
                ['Z', 9, 9, 1, 9, 9, 'Z'],
                ['Z', 9, 9, 1, 9, 9, 'Z'],
                ['Z', 9, 9, 1, 9, 9, 'Z'],
                ['Z', 9, 9, 1, 1, 1, 'Z'],
                ['Z', 'Z', 'Z', 'Z', 'Z', 'Z', 'Z']]
    # When
    result = dijkstra(heat_map, (1, 1), (5, 5))
    # Then
    assert result == 16


def test_get_end_node():
    # Given
    heat_map = [['Z', 'Z', 'Z', 'Z', 'Z'],
                ['Z', 1, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 9, 'Z'],
                ['Z', 9, 1, 1, 'Z'],
                ['Z', 'Z', 'Z', 'Z', 'Z']]
    # When
    result = get_end_node(heat_map)
    # Then
    assert result == (5, 3)
