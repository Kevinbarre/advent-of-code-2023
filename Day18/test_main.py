import pytest

from main import part1, part2, parse_instructions, Color, RIGHT, DOWN, LEFT, UP, build_trench, build_trench_right, \
    build_trench_left, build_trench_down, build_trench_up, count_size, flood_fill, parse_true_instructions, \
    get_vertices_coordinates, shoelace, get_perimeter, count_size_2

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 62


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 952408144115


def test_color():
    # Given
    rgb_code = "#70c710"
    # When
    result = Color(rgb_code)
    # Then
    assert result.r == 112
    assert result.g == 199
    assert result.b == 16


def test_parse_instructions():
    # Given
    lines = ["R 6 (#70c710)",
             "D 5 (#0dc571)",
             "L 2 (#5713f0)",
             "D 2 (#d2c081)",
             "R 2 (#59c680)",
             "D 2 (#411b91)",
             "L 5 (#8ceee2)",
             "U 2 (#caa173)",
             "L 1 (#1b58a2)",
             "U 2 (#caa171)",
             "R 2 (#7807d2)",
             "U 3 (#a77fa3)",
             "L 2 (#015232)",
             "U 2 (#7a21e3)"]
    # When
    result = parse_instructions(lines)
    # Then
    assert result == [(RIGHT, 6, Color("#70c710")),
                      (DOWN, 5, Color("#0dc571")),
                      (LEFT, 2, Color("#5713f0")),
                      (DOWN, 2, Color("#d2c081")),
                      (RIGHT, 2, Color("#59c680")),
                      (DOWN, 2, Color("#411b91")),
                      (LEFT, 5, Color("#8ceee2")),
                      (UP, 2, Color("#caa173")),
                      (LEFT, 1, Color("#1b58a2")),
                      (UP, 2, Color("#caa171")),
                      (RIGHT, 2, Color("#7807d2")),
                      (UP, 3, Color("#a77fa3")),
                      (LEFT, 2, Color("#015232")),
                      (UP, 2, Color("#7a21e3"))]


@pytest.mark.parametrize("trench, position, length, expected", [
    ([['#']], (0, 0), 2, [['#', '#', '#']]),
    ([['#', '.']], (0, 0), 2, [['#', '#', '#']]),
    ([['#'], ['.']], (0, 0), 2, [['#', '#', '#'], ['.', '.', '.']]),
    ([['#', '#', '#'], ['#', '.', '.']], (1, 0), 3, [['#', '#', '#', '.'], ['#', '#', '#', '#']])])
def test_build_trench_right(trench, position, length, expected):
    # Given
    # When
    result = build_trench_right(trench, position, length)
    # Then
    assert result == expected


@pytest.mark.parametrize("trench, position, length, expected", [
    ([['#', '.']], (0, 0), 2, [['#', '#', '#', '.']]),
    ([['.', '.', '.', '#']], (0, 3), 2, [['.', '#', '#', '#']]),
    ([['#'], ['.']], (0, 0), 2, [['#', '#', '#'], ['.', '.', '.']]),
    ([['#', '#', '#'], ['#', '.', '.']], (1, 0), 2, [['.', '.', '#', '#', '#'], ['#', '#', '#', '.', '.']])])
def test_build_trench_left(trench, position, length, expected):
    # Given
    # When
    result = build_trench_left(trench, position, length)
    # Then
    assert result == expected


@pytest.mark.parametrize("trench, position, length, expected", [
    ([['#']], (0, 0), 2, [['#'], ['#'], ['#']]),
    ([['#'], ['.'], ['.']], (0, 0), 2, [['#'], ['#'], ['#']]),
    ([['#', '.']], (0, 0), 2, [['#', '.'], ['#', '.'], ['#', '.']]),
    ([['#', '#'], ['.', '#'], ['#', '#']], (0, 0), 2, [['#', '#'], ['#', '#'], ['#', '#']])])
def test_build_trench_down(trench, position, length, expected):
    # Given
    # When
    result = build_trench_down(trench, position, length)
    # Then
    assert result == expected


@pytest.mark.parametrize("trench, position, length, expected", [
    ([['#']], (0, 0), 2, [['#'], ['#'], ['#']]),
    ([['.'], ['#'], ['.'], ['.']], (1, 0), 2, [['#'], ['#'], ['#'], ['.'], ['.']]),
    ([['#', '.']], (0, 0), 2, [['#', '.'], ['#', '.'], ['#', '.']]),
    ([['#', '#'], ['.', '#'], ['#', '#']], (2, 0), 2, [['#', '#'], ['#', '#'], ['#', '#']]),
    ([['#', '#', '#'], ['.', '.', '#'], ['#', '#', '#']], (2, 0), 2,
     [['#', '#', '#'], ['#', '.', '#'], ['#', '#', '#']])])
def test_build_trench_up(trench, position, length, expected):
    # Given
    # When
    result = build_trench_up(trench, position, length)
    # Then
    assert result == expected


def test_build_trench():
    # Given
    instructions = [(RIGHT, 2, Color("#000000")),
                    (DOWN, 2, Color("#000000")),
                    (LEFT, 2, Color("#000000")),
                    (UP, 2, Color("#000000"))]
    # When
    result = build_trench(instructions)
    # Then
    assert result == [['#', '#', '#'],
                      ['#', '.', '#'],
                      ['#', '#', '#']]


@pytest.mark.parametrize("trench, position, expected", [
    ([['.', '.', '.'], ['.', '.', '.'], ['.', '.', '.']], (0, 0), [['X', 'X', 'X'], ['X', 'X', 'X'], ['X', 'X', 'X']]),
    ([['.', '#', '.'], ['.', '#', '.'], ['.', '#', '.']], (0, 0), [['X', '#', '.'], ['X', '#', '.'], ['X', '#', '.']])])
def test_flood_fill(trench, position, expected):
    # Given
    # When
    flood_fill(trench, position)
    # Then
    assert trench == expected


@pytest.mark.parametrize("trench, expected", [
    ([['#', '#', '#'],
      ['#', '.', '#'],
      ['#', '#', '#']], 9),
    ([['.', '.', '.'],
      ['.', '#', '.'],
      ['.', '.', '.']], 1)
])
def test_count_size(trench, expected):
    # Given
    # When
    result = count_size(trench)
    # Then
    assert result == expected


def test_parse_true_instructions():
    # Given
    lines = ["R 6 (#70c710)",
             "D 5 (#0dc571)",
             "L 2 (#5713f0)",
             "D 2 (#d2c081)",
             "R 2 (#59c680)",
             "D 2 (#411b91)",
             "L 5 (#8ceee2)",
             "U 2 (#caa173)",
             "L 1 (#1b58a2)",
             "U 2 (#caa171)",
             "R 2 (#7807d2)",
             "U 3 (#a77fa3)",
             "L 2 (#015232)",
             "U 2 (#7a21e3)"]
    # When
    result = parse_true_instructions(lines)
    # Then
    assert result == [(RIGHT, 461937, None),
                      (DOWN, 56407, None),
                      (RIGHT, 356671, None),
                      (DOWN, 863240, None),
                      (RIGHT, 367720, None),
                      (DOWN, 266681, None),
                      (LEFT, 577262, None),
                      (UP, 829975, None),
                      (LEFT, 112010, None),
                      (DOWN, 829975, None),
                      (LEFT, 491645, None),
                      (UP, 686074, None),
                      (LEFT, 5411, None),
                      (UP, 500254, None)]


def test_get_vertices_coordinates():
    # Given
    instructions = [(RIGHT, 6, None),
                    (DOWN, 5, None),
                    (LEFT, 2, None),
                    (DOWN, 2, None),
                    (RIGHT, 2, None),
                    (DOWN, 2, None),
                    (LEFT, 5, None),
                    (UP, 2, None),
                    (LEFT, 1, None),
                    (UP, 2, None),
                    (RIGHT, 2, None),
                    (UP, 3, None),
                    (LEFT, 2, None),
                    (UP, 2, None)]
    # When
    result = get_vertices_coordinates(instructions)
    # Then
    assert result == [(0, 0), (0, 6), (5, 6), (5, 4), (7, 4), (7, 6), (9, 6), (9, 1), (7, 1), (7, 0), (5, 0), (5, 2),
                      (2, 2), (2, 0)]


def test_shoelace():
    # Given
    vertices_coordinates = [(0, 0), (0, 6), (5, 6), (5, 4), (7, 4), (7, 6), (9, 6), (9, 1), (7, 1), (7, 0), (5, 0),
                            (5, 2), (2, 2), (2, 0)]
    # When
    result = int(shoelace(vertices_coordinates))
    # Then
    assert result == 42


def test_shoelace_wikipedia():
    # Given
    vertices_coordinates = [(6, 1), (1, 3), (2, 7), (4, 4), (5, 8)]
    # When
    result = shoelace(vertices_coordinates)
    # Then
    assert result == 16.5


def test_get_perimeter():
    # Given
    instructions = [(RIGHT, 6, None),
                    (DOWN, 5, None),
                    (LEFT, 2, None),
                    (DOWN, 2, None),
                    (RIGHT, 2, None),
                    (DOWN, 2, None),
                    (LEFT, 5, None),
                    (UP, 2, None),
                    (LEFT, 1, None),
                    (UP, 2, None),
                    (RIGHT, 2, None),
                    (UP, 3, None),
                    (LEFT, 2, None),
                    (UP, 2, None)]
    # When
    result = get_perimeter(instructions)
    # Then
    assert result == 38


def test_count_size_2():
    # Given
    instructions = [(RIGHT, 6, None),
                    (DOWN, 5, None),
                    (LEFT, 2, None),
                    (DOWN, 2, None),
                    (RIGHT, 2, None),
                    (DOWN, 2, None),
                    (LEFT, 5, None),
                    (UP, 2, None),
                    (LEFT, 1, None),
                    (UP, 2, None),
                    (RIGHT, 2, None),
                    (UP, 3, None),
                    (LEFT, 2, None),
                    (UP, 2, None)]
    # when
    result = count_size_2(instructions)
    # Then
    assert result == 62
