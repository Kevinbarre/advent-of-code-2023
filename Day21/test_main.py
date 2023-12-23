import pytest

from main import part1, part2, parse_garden, get_accessible_positions, find_reachable_garden_plots, expand_garden, \
    find_first_three_points, get_quadratic_coefficients, get_positions

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines, 6)
    # Then
    assert result == 16


@pytest.mark.parametrize("test_input, expected",
                         [(7, 52), (8, 68), (25, 576), (42, 1576), (59, 3068), (76, 5052)])
def test_part2(test_input, expected):
    # Given
    with open("example2.txt") as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines, test_input)
    # Then
    assert result == expected


def test_parse_garden():
    # Given
    lines = ["...........",
             ".....###.#.",
             ".###.##..#.",
             "..#.#...#..",
             "....#.#....",
             ".##..S####.",
             ".##..#...#.",
             ".......##..",
             ".##.#.####.",
             ".##..##.##.",
             "..........."]
    # When
    starting_position, garden = parse_garden(lines)
    # Then
    assert starting_position == (6, 6)
    assert garden == ["#############",
                      "#...........#",
                      "#.....###.#.#",
                      "#.###.##..#.#",
                      "#..#.#...#..#",
                      "#....#.#....#",
                      "#.##...####.#",
                      "#.##..#...#.#",
                      "#.......##..#",
                      "#.##.#.####.#",
                      "#.##..##.##.#",
                      "#...........#",
                      "#############"]


def test_get_accessible_positions():
    # Given
    garden = ["#############",
              "#...........#",
              "#.....###.#.#",
              "#.###.##..#.#",
              "#..#.#...#..#",
              "#....#.#....#",
              "#.##...####.#",
              "#.##..#...#.#",
              "#.......##..#",
              "#.##.#.####.#",
              "#.##..##.##.#",
              "#...........#",
              "#############"]
    current_position = (6, 6)
    # When
    result = get_accessible_positions(garden, current_position)
    # Then
    assert result == {(5, 6), (6, 5)}


@pytest.mark.parametrize("test_input, expected", [(1, 2), (2, 4), (3, 6), (6, 16)])
def test_find_reachable_garden_plots(test_input, expected):
    # Given
    garden = ["#############",
              "#...........#",
              "#.....###.#.#",
              "#.###.##..#.#",
              "#..#.#...#..#",
              "#....#.#....#",
              "#.##...####.#",
              "#.##..#...#.#",
              "#.......##..#",
              "#.##.#.####.#",
              "#.##..##.##.#",
              "#...........#",
              "#############"]
    starting_position = (6, 6)
    # When
    result = find_reachable_garden_plots(garden, starting_position, test_input)
    # Then
    assert result == expected


def test_expand_garden():
    # Given
    lines = ["...........",
             ".....###.#.",
             ".###.##..#.",
             "..#.#...#..",
             "....#.#....",
             ".##..S####.",
             ".##..#...#.",
             ".......##..",
             ".##.#.####.",
             ".##..##.##.",
             "..........."]
    n = 1
    # When
    starting_position, expanded_garden = expand_garden(lines, n)
    # Then
    assert starting_position == (16, 16)
    assert expanded_garden == [
        ".................................",
        ".....###.#......###.#......###.#.",
        ".###.##..#..###.##..#..###.##..#.",
        "..#.#...#....#.#...#....#.#...#..",
        "....#.#........#.#........#.#....",
        ".##...####..##...####..##...####.",
        ".##..#...#..##..#...#..##..#...#.",
        ".......##.........##.........##..",
        ".##.#.####..##.#.####..##.#.####.",
        ".##..##.##..##..##.##..##..##.##.",
        ".................................",
        ".................................",
        ".....###.#......###.#......###.#.",
        ".###.##..#..###.##..#..###.##..#.",
        "..#.#...#....#.#...#....#.#...#..",
        "....#.#........#.#........#.#....",
        ".##...####..##...####..##...####.",
        ".##..#...#..##..#...#..##..#...#.",
        ".......##.........##.........##..",
        ".##.#.####..##.#.####..##.#.####.",
        ".##..##.##..##..##.##..##..##.##.",
        ".................................",
        ".................................",
        ".....###.#......###.#......###.#.",
        ".###.##..#..###.##..#..###.##..#.",
        "..#.#...#....#.#...#....#.#...#..",
        "....#.#........#.#........#.#....",
        ".##...####..##...####..##...####.",
        ".##..#...#..##..#...#..##..#...#.",
        ".......##.........##.........##..",
        ".##.#.####..##.#.####..##.#.####.",
        ".##..##.##..##..##.##..##..##.##.",
        ".................................",
    ]


def test_find_first_three_points():
    # Given
    lines = [".................",
             "..#..............",
             "...##........###.",
             ".............##..",
             "..#....#.#.......",
             ".......#.........",
             "......##.##......",
             "...##.#.....#....",
             "........S........",
             "....#....###.#...",
             "......#..#.#.....",
             ".....#.#..#......",
             ".#...............",
             ".#.....#.#....#..",
             "...#.........#.#.",
             "...........#..#..",
             "................."]
    # When
    result = find_first_three_points(lines)
    # Then
    assert result == (68, 576, 1576)


def test_get_quadratic_coefficients():
    # Given
    first_three_points = (68, 576, 1576)
    # When
    result = get_quadratic_coefficients(first_three_points)
    # Then
    assert result == (246, -230, 52)


@pytest.mark.parametrize("test_input, expected",
                         [(8, 68), (25, 576), (42, 1576), (59, 3068), (76, 5052)])
def test_get_positions(test_input, expected):
    # Given
    quadratic_coefficients = (246, -230, 52)
    garden_width = 17
    # When
    result = get_positions(quadratic_coefficients, garden_width, test_input)
    # Then
    assert result == expected
