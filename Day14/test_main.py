from main import part1, part2, transpose_grid, sort_row, sort_full_row, tilt_north, get_load

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
    assert result == 0


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
    result = sort_row(row)
    # Then
    assert result == "OOO......"


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
