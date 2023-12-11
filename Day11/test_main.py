import pytest

from main import part1, part2, expand_space, find_galaxies, get_shortest_distance, get_shortest_distance_with_expansion, \
    get_expanded_rows_columns

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 374


@pytest.mark.parametrize("nb_expansions, expected", [(1, 374), (9, 1030), (99, 8410)])
def test_part2(nb_expansions, expected):
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines, nb_expansions)
    # Then
    assert result == expected


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


@pytest.mark.parametrize("first, second, expected",
                         [((5, 1), (9, 4), 9),
                          ((0, 3), (8, 7), 15),
                          ((2, 0), (6, 9), 17),
                          ((9, 0), (9, 4), 5)])
def test_get_shortest_distance_with_expansion(first, second, expected):
    # Given
    nb_expansions = 1
    expanded_rows = [3, 7]
    expanded_columns = [2, 5, 8]
    # When
    result = get_shortest_distance_with_expansion(first, second, nb_expansions, expanded_rows, expanded_columns)
    # Then
    assert result == expected


def test_get_expanded_rows_columns():
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
    expanded_rows, expanded_columns = get_expanded_rows_columns(image)
    # Then
    assert expanded_rows == [3, 7]
    assert expanded_columns == [2, 5, 8]
