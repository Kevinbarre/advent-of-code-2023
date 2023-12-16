import pytest

from main import part1, part2, parse_grid, Direction, step_beam, energize_grid, get_energized_count, \
    get_beam_from_direction, get_max_energized_count

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 46


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 51


def test_parse_grid():
    # Given
    lines = [".|...\\....",
             "|.-.\\.....",
             ".....|-...",
             "........|.",
             "..........",
             ".........\\",
             "..../.\\\\..",
             ".-.-/..|..",
             ".|....-|.\\",
             "..//.|...."]
    # When
    result = parse_grid(lines)
    # Then
    assert result == ["ZZZZZZZZZZZZ",
                      "Z.|...\\....Z",
                      "Z|.-.\\.....Z",
                      "Z.....|-...Z",
                      "Z........|.Z",
                      "Z..........Z",
                      "Z.........\\Z",
                      "Z..../.\\\\..Z",
                      "Z.-.-/..|..Z",
                      "Z.|....-|.\\Z",
                      "Z..//.|....Z",
                      "ZZZZZZZZZZZZ"]


@pytest.mark.parametrize("test_input, expected",
                         [(Direction.UP, (0, 1, Direction.UP)),
                          (Direction.DOWN, (2, 1, Direction.DOWN)),
                          (Direction.LEFT, (1, 0, Direction.LEFT)),
                          (Direction.RIGHT, (1, 2, Direction.RIGHT))])
def test_get_beam_from_direction(test_input, expected):
    # Given
    j, i = 1, 1
    # When
    result = get_beam_from_direction(j, i, test_input)
    # Then
    assert result == expected


@pytest.mark.parametrize("test_input, expected", [(Direction.UP, {(4, 2, Direction.UP)}),
                                                  (Direction.DOWN, {(6, 2, Direction.DOWN)}),
                                                  (Direction.LEFT, {(5, 1, Direction.LEFT)}),
                                                  (Direction.RIGHT, {(5, 3, Direction.RIGHT)})])
def test_step_beam_forward(test_input, expected):
    # Given
    grid = ["ZZZZZZZZZZZZ",
            "Z.|...\\....Z",
            "Z|.-.\\.....Z",
            "Z.....|-...Z",
            "Z........|.Z",
            "Z..........Z",
            "Z.........\\Z",
            "Z..../.\\\\..Z",
            "Z.-.-/..|..Z",
            "Z.|....-|.\\Z",
            "Z..//.|....Z",
            "ZZZZZZZZZZZZ"]
    beam = (5, 2, test_input)
    # When
    result = step_beam(grid, beam)
    # Then
    assert result == expected


@pytest.mark.parametrize("test_input", [(0, 1, Direction.UP),
                                        (11, 1, Direction.DOWN),
                                        (1, 0, Direction.LEFT),
                                        (10, 11, Direction.RIGHT)])
def test_step_beam_destroy_beam(test_input):
    # Given
    grid = ["ZZZZZZZZZZZZ",
            "Z.|...\\....Z",
            "Z|.-.\\.....Z",
            "Z.....|-...Z",
            "Z........|.Z",
            "Z..........Z",
            "Z.........\\Z",
            "Z..../.\\\\..Z",
            "Z.-.-/..|..Z",
            "Z.|....-|.\\Z",
            "Z..//.|....Z",
            "ZZZZZZZZZZZZ"]
    # When
    result = step_beam(grid, test_input)
    # Then
    assert result == set()


@pytest.mark.parametrize("test_input, expected", [((2, 1, Direction.UP), {(1, 1, Direction.UP)}),
                                                  ((2, 1, Direction.DOWN), {(3, 1, Direction.DOWN)}),
                                                  ((8, 2, Direction.LEFT), {(8, 1, Direction.LEFT)}),
                                                  ((8, 2, Direction.RIGHT), {(8, 3, Direction.RIGHT)})])
def test_step_beam_pointy_splitter(test_input, expected):
    # Given
    grid = ["ZZZZZZZZZZZZ",
            "Z.|...\\....Z",
            "Z|.-.\\.....Z",
            "Z.....|-...Z",
            "Z........|.Z",
            "Z..........Z",
            "Z.........\\Z",
            "Z..../.\\\\..Z",
            "Z.-.-/..|..Z",
            "Z.|....-|.\\Z",
            "Z..//.|....Z",
            "ZZZZZZZZZZZZ"]
    # When
    result = step_beam(grid, test_input)
    # Then
    assert result == expected


@pytest.mark.parametrize("test_input, expected",
                         [((2, 3, Direction.UP), {(2, 2, Direction.LEFT), (2, 4, Direction.RIGHT)}),
                          ((2, 3, Direction.DOWN), {(2, 2, Direction.LEFT), (2, 4, Direction.RIGHT)}),
                          ((4, 9, Direction.LEFT), {(3, 9, Direction.UP), (5, 9, Direction.DOWN)}),
                          ((4, 9, Direction.RIGHT), {(3, 9, Direction.UP), (5, 9, Direction.DOWN)})])
def test_step_beam_flat_splitter(test_input, expected):
    # Given
    grid = ["ZZZZZZZZZZZZ",
            "Z.|...\\....Z",
            "Z|.-.\\.....Z",
            "Z.....|-...Z",
            "Z........|.Z",
            "Z..........Z",
            "Z.........\\Z",
            "Z..../.\\\\..Z",
            "Z.-.-/..|..Z",
            "Z.|....-|.\\Z",
            "Z..//.|....Z",
            "ZZZZZZZZZZZZ"]
    # When
    result = step_beam(grid, test_input)
    # Then
    assert result == expected


@pytest.mark.parametrize("test_input, expected",
                         [((2, 5, Direction.UP), {(2, 4, Direction.LEFT)}),
                          ((2, 5, Direction.DOWN), {(2, 6, Direction.RIGHT)}),
                          ((2, 5, Direction.LEFT), {(1, 5, Direction.UP)}),
                          ((2, 5, Direction.RIGHT), {(3, 5, Direction.DOWN)})])
def test_step_beam_mirror_antislash(test_input, expected):
    # Given
    grid = ["ZZZZZZZZZZZZ",
            "Z.|...\\....Z",
            "Z|.-.\\.....Z",
            "Z.....|-...Z",
            "Z........|.Z",
            "Z..........Z",
            "Z.........\\Z",
            "Z..../.\\\\..Z",
            "Z.-.-/..|..Z",
            "Z.|....-|.\\Z",
            "Z..//.|....Z",
            "ZZZZZZZZZZZZ"]
    # When
    result = step_beam(grid, test_input)
    # Then
    assert result == expected


@pytest.mark.parametrize("test_input, expected",
                         [((8, 5, Direction.UP), {(8, 6, Direction.RIGHT)}),
                          ((7, 5, Direction.DOWN), {(7, 4, Direction.LEFT)}),
                          ((7, 5, Direction.LEFT), {(8, 5, Direction.DOWN)}),
                          ((7, 5, Direction.RIGHT), {(6, 5, Direction.UP)})])
def test_step_beam_mirror_slash(test_input, expected):
    # Given
    grid = ["ZZZZZZZZZZZZ",
            "Z.|...\\....Z",
            "Z|.-.\\.....Z",
            "Z.....|-...Z",
            "Z........|.Z",
            "Z..........Z",
            "Z.........\\Z",
            "Z..../.\\\\..Z",
            "Z.-.-/..|..Z",
            "Z.|....-|.\\Z",
            "Z..//.|....Z",
            "ZZZZZZZZZZZZ"]
    # When
    result = step_beam(grid, test_input)
    # Then
    assert result == expected


def test_step_beam_start_on_antislash():
    # Given
    grid = ["ZZZZ",
            "Z\\.Z",
            "Z..Z",
            "ZZZZ"]
    # When
    result = step_beam(grid, (1, 1, Direction.RIGHT))
    # Then
    assert result == {(2, 1, Direction.DOWN)}


def test_energize_grid():
    # Given
    grid = ["ZZZZZZZZZZZZ",
            "Z.|...\\....Z",
            "Z|.-.\\.....Z",
            "Z.....|-...Z",
            "Z........|.Z",
            "Z..........Z",
            "Z.........\\Z",
            "Z..../.\\\\..Z",
            "Z.-.-/..|..Z",
            "Z.|....-|.\\Z",
            "Z..//.|....Z",
            "ZZZZZZZZZZZZ"]
    # When
    result = energize_grid(grid, (1, 1, Direction.RIGHT))
    # Then
    assert result == ["ZZZZZZZZZZZZ",
                      "Z######....Z",
                      "Z.#...#....Z",
                      "Z.#...#####Z",
                      "Z.#...##...Z",
                      "Z.#...##...Z",
                      "Z.#...##...Z",
                      "Z.#..####..Z",
                      "Z########..Z",
                      "Z.#######..Z",
                      "Z.#...#.#..Z",
                      "ZZZZZZZZZZZZ"]


def test_get_energized_count():
    # Given
    energized_grid = ["ZZZZZZZZZZZZ",
                      "Z######....Z",
                      "Z.#...#....Z",
                      "Z.#...#####Z",
                      "Z.#...##...Z",
                      "Z.#...##...Z",
                      "Z.#...##...Z",
                      "Z.#..####..Z",
                      "Z########..Z",
                      "Z.#######..Z",
                      "Z.#...#.#..Z",
                      "ZZZZZZZZZZZZ"]
    # When
    result = get_energized_count(energized_grid)
    # Then
    assert result == 46


def test_get_max_energized_count():
    # Given
    grid = ["ZZZZZZZZZZZZ",
            "Z.|...\\....Z",
            "Z|.-.\\.....Z",
            "Z.....|-...Z",
            "Z........|.Z",
            "Z..........Z",
            "Z.........\\Z",
            "Z..../.\\\\..Z",
            "Z.-.-/..|..Z",
            "Z.|....-|.\\Z",
            "Z..//.|....Z",
            "ZZZZZZZZZZZZ"]
    # When
    result = get_max_energized_count(grid)
    # Then
    assert result == 51
