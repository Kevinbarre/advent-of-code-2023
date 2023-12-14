import pytest

from main import part1, part2, transpose_grid, sort_row, sort_full_row, tilt_north, get_load, tilt_west, tilt_south, \
    tilt_east, cycle_once, cycle_multiple_times

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 136


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 64


def test_transpose_grid():
    # Given
    grid = ["O.#",
            ".#O"]
    # When
    result = transpose_grid(grid)
    # Then
    assert result == ["O.",
                      ".#",
                      "#O"]


def test_sort_row():
    # Given
    row = "O...O..O."
    # When
    result = sort_row(row, True)
    # Then
    assert result == "OOO......"


def test_sort_row_not_reverse():
    # Given
    row = "O...O..O."
    # When
    result = sort_row(row, False)
    # Then
    assert result == "......OOO"


def test_sort_full_row():
    # Given
    row = "O..O.#.O.OO#O.O"
    # When
    result = sort_full_row(row)
    # Then
    assert result == "OO...#OOO..#OO."


def test_tilt_north():
    # Given
    grid = ["O....#....",
            "O.OO#....#",
            ".....##...",
            "OO.#O....O",
            ".O.....O#.",
            "O.#..O.#.#",
            "..O..#O..O",
            ".......O..",
            "#....###..",
            "#OO..#...."]
    # When
    result = tilt_north(grid)
    # Then
    assert result == ["OOOO.#.O..",
                      "OO..#....#",
                      "OO..O##..O",
                      "O..#.OO...",
                      "........#.",
                      "..#....#.#",
                      "..O..#.O.O",
                      "..O.......",
                      "#....###..",
                      "#....#...."]


def test_get_load():
    # Given
    grid = ["OOOO.#.O..",
            "OO..#....#",
            "OO..O##..O",
            "O..#.OO...",
            "........#.",
            "..#....#.#",
            "..O..#.O.O",
            "..O.......",
            "#....###..",
            "#....#...."]
    # When
    result = get_load(grid)
    # Then
    assert result == 136


def test_tilt_west():
    # Given
    grid = ["OOOO.#.O..",
            "OO..#....#",
            "OO..O##..O",
            "O..#.OO...",
            "........#.",
            "..#....#.#",
            "..O..#.O.O",
            "..O.......",
            "#....###..",
            "#....#...."]
    # When
    result = tilt_west(grid)
    # Then
    assert result == ["OOOO.#O...",
                      "OO..#....#",
                      "OOO..##O..",
                      "O..#OO....",
                      "........#.",
                      "..#....#.#",
                      "O....#OO..",
                      "O.........",
                      "#....###..",
                      "#....#...."]


def test_tilt_south():
    # Given
    grid = ["OOOO.#O...",
            "OO..#....#",
            "OOO..##O..",
            "O..#OO....",
            "........#.",
            "..#....#.#",
            "O....#OO..",
            "O.........",
            "#....###..",
            "#....#...."]
    # When
    result = tilt_south(grid)
    # Then
    assert result == [".....#....",
                      "....#.O..#",
                      "O..O.##...",
                      "O.O#......",
                      "O.O....O#.",
                      "O.#..O.#.#",
                      "O....#....",
                      "OO....OO..",
                      "#O...###..",
                      "#O..O#...."]


def test_tilt_east():
    # Given
    grid = [".....#....",
            "....#.O..#",
            "O..O.##...",
            "O.O#......",
            "O.O....O#.",
            "O.#..O.#.#",
            "O....#....",
            "OO....OO..",
            "#O...###..",
            "#O..O#...."]
    # When
    result = tilt_east(grid)
    # Then
    assert result == [".....#....",
                      "....#...O#",
                      "...OO##...",
                      ".OO#......",
                      ".....OOO#.",
                      ".O#...O#.#",
                      "....O#....",
                      "......OOOO",
                      "#...O###..",
                      "#..OO#...."]


def test_cycle_once():
    # Given
    grid = ("O....#....",
            "O.OO#....#",
            ".....##...",
            "OO.#O....O",
            ".O.....O#.",
            "O.#..O.#.#",
            "..O..#O..O",
            ".......O..",
            "#....###..",
            "#OO..#....")
    # When
    result = cycle_once(grid)
    # Then
    assert result == (".....#....",
                      "....#...O#",
                      "...OO##...",
                      ".OO#......",
                      ".....OOO#.",
                      ".O#...O#.#",
                      "....O#....",
                      "......OOOO",
                      "#...O###..",
                      "#..OO#....")


@pytest.mark.parametrize("test_input, expected", [(1, (".....#....",
                                                       "....#...O#",
                                                       "...OO##...",
                                                       ".OO#......",
                                                       ".....OOO#.",
                                                       ".O#...O#.#",
                                                       "....O#....",
                                                       "......OOOO",
                                                       "#...O###..",
                                                       "#..OO#....")),
                                                  (2, (".....#....",
                                                       "....#...O#",
                                                       ".....##...",
                                                       "..O#......",
                                                       ".....OOO#.",
                                                       ".O#...O#.#",
                                                       "....O#...O",
                                                       ".......OOO",
                                                       "#..OO###..",
                                                       "#.OOO#...O")),
                                                  (3, (".....#....",
                                                       "....#...O#",
                                                       ".....##...",
                                                       "..O#......",
                                                       ".....OOO#.",
                                                       ".O#...O#.#",
                                                       "....O#...O",
                                                       ".......OOO",
                                                       "#...O###.O",
                                                       "#.OOO#...O"))])
def test_cycle_multiple_times(test_input, expected):
    # Given
    grid = ("O....#....",
            "O.OO#....#",
            ".....##...",
            "OO.#O....O",
            ".O.....O#.",
            "O.#..O.#.#",
            "..O..#O..O",
            ".......O..",
            "#....###..",
            "#OO..#....")
    # When
    result = cycle_multiple_times(grid, test_input)
    # Then
    assert result == expected
