import pytest

from main import part1, part2, parse_garden, get_accessible_positions, find_reachable_garden_plots

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines, 6)
    # Then
    assert result == 16


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 0


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
