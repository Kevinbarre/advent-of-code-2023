import pytest

from main import part1, part2, expand_space, find_galaxies, get_shortest_distance

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 374


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 0


def test_expand_space():
    # Given
    image = ["...#......",
             ".......#..",
             "#.........",
             "..........",
             "......#...",
             ".#........",
             ".........#",
             "..........",
             ".......#..",
             "#...#....."]
    # When
    result = expand_space(image)
    # Then
    assert result == ["....#........",
                      ".........#...",
                      "#............",
                      ".............",
                      ".............",
                      "........#....",
                      ".#...........",
                      "............#",
                      ".............",
                      ".............",
                      ".........#...",
                      "#....#......."]


def test_find_galaxies():
    # Given
    image = ["....#........",
             ".........#...",
             "#............",
             ".............",
             ".............",
             "........#....",
             ".#...........",
             "............#",
             ".............",
             ".............",
             ".........#...",
             "#....#......."]
    # When
    result = find_galaxies(image)
    # Then
    assert result == {(0, 4), (1, 9), (2, 0), (5, 8), (6, 1), (7, 12), (10, 9), (11, 0), (11, 5)}


@pytest.mark.parametrize("first, second, expected",
                         [((6, 1), (11, 5), 9),
                          ((0, 4), (10, 9), 15),
                          ((2, 0), (7, 12), 17),
                          ((11, 0), (11, 5), 5)])
def test_get_shortest_distance(first, second, expected):
    # Given
    # When
    result = get_shortest_distance(first, second)
    # Then
    assert result == expected
