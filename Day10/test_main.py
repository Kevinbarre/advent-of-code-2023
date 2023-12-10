import pytest

from main import part1, part2, parse_tiles, get_start_position, find_connected_pipes, navigate, get_farthest_distance, \
    get_loop_positions, count_inside_loop, find_start_symbol

filename = "example.txt"


@pytest.mark.parametrize("test_input, expected", [(filename, 4), ("example2.txt", 8)])
def test_part1(test_input, expected):
    # Given
    with open(test_input) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == expected


@pytest.mark.parametrize("test_input, expected",
                         [(filename, 1), ("example2.txt", 1), ("example3.txt", 4), ("example4.txt", 8),
                          ("example5.txt", 10)])
def test_part2(test_input, expected):
    # Given
    with open(test_input) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == expected


def test_parse_tiles():
    # Given
    lines = ["-L|F7", "7S-7|", "L|7||", "-L-J|", "L|-JF"]
    # When
    result = parse_tiles(lines)
    # Then
    assert result == [".......", ".-L|F7.", ".7S-7|.", ".L|7||.", ".-L-J|.", ".L|-JF.", "......."]


@pytest.mark.parametrize("test_input, expected",
                         [([".......", ".-L|F7.", ".7S-7|.", ".L|7||.", ".-L-J|.", ".L|-JF.", "......."], (2, 2)),
                          ([".......", ".7-F7-.", "..FJ|7.", ".SJLL7.", ".|F--J.", ".LJ.LJ.", "......."], (3, 1))])
def test_get_start_position(test_input, expected):
    # Given
    # When
    result = get_start_position(test_input)
    # Then
    assert result == expected


def test_find_connected_pipes():
    # Given
    tiles = [".......", ".-L|F7.", ".7S-7|.", ".L|7||.", ".-L-J|.", ".L|-JF.", "......."]
    start_position = (2, 2)
    # When
    result = find_connected_pipes(tiles, start_position)
    # Then
    assert len(result) == 2
    assert (2, 3) in result
    assert (3, 2) in result


@pytest.mark.parametrize("current_position, next_position, expected",
                         [((2, 2), (2, 3), (2, 4)),
                          ((2, 3), (2, 4), (3, 4)),
                          ((2, 4), (3, 4), (4, 4)),
                          ((3, 4), (4, 4), (4, 3)),
                          ((4, 4), (4, 3), (4, 2)),
                          ((4, 3), (4, 2), (3, 2)),
                          ((4, 2), (3, 2), (2, 2)),
                          ])
def test_navigate(current_position, next_position, expected):
    # Given
    tiles = [".......", ".-L|F7.", ".7S-7|.", ".L|7||.", ".-L-J|.", ".L|-JF.", "......."]
    # When
    result = navigate(tiles, current_position, next_position)
    # Then
    assert result == expected


@pytest.mark.parametrize("test_input, expected",
                         [([".......", ".-L|F7.", ".7S-7|.", ".L|7||.", ".-L-J|.", ".L|-JF.", "......."], 4),
                          ([".......", ".7-F7-.", "..FJ|7.", ".SJLL7.", ".|F--J.", ".LJ.LJ.", "......."], 8)])
def test_get_farthest_distance(test_input, expected):
    # Given
    tiles = test_input
    # When
    result = get_farthest_distance(tiles)
    # Then
    assert result == expected


def test_get_loop_positions():
    # Given
    tiles = [".......", ".-L|F7.", ".7S-7|.", ".L|7||.", ".-L-J|.", ".L|-JF.", "......."]
    # When
    result = get_loop_positions(tiles)
    # Then
    assert result == {(2, 2), (2, 3), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (3, 2)}


@pytest.mark.parametrize("test_input, expected",
                         [([".....", ".S-7.", ".|.|.", ".L-J.", "....."], 'F'),
                          ([".....", ".FS7.", ".|.|.", ".L-J.", "....."], '-'),
                          ([".....", ".F-S.", ".|.|.", ".L-J.", "....."], '7'),
                          ([".....", ".F-7.", ".|.S.", ".L-J.", "....."], '|'),
                          ([".....", ".F-7.", ".|.|.", ".L-S.", "....."], 'J'),
                          ([".....", ".F-7.", ".|.|.", ".LSJ.", "....."], '-'),
                          ([".....", ".F-7.", ".|.|.", ".S-J.", "....."], 'L'),
                          ([".....", ".F-7.", ".S.|.", ".L-J.", "....."], '|')])
def test_find_start_symbol(test_input, expected):
    # Given
    # When
    result = find_start_symbol(test_input)
    # Then
    assert result == expected


@pytest.mark.parametrize("test_input, expected",
                         [(["...........",
                            ".S-------7.",
                            ".|F-----7|.",
                            ".||.....||.",
                            ".||.....||.",
                            ".|L-7.F-J|.",
                            ".|..|.|..|.",
                            ".L--J.L--J.",
                            "..........."], 4),
                          ([".F----7F7F7F7F-7....",
                            ".|F--7||||||||FJ....",
                            ".||.FJ||||||||L7....",
                            "FJL7L7LJLJ||LJ.L-7..",
                            "L--J.L7...LJS7F-7L7.",
                            "....F-J..F7FJ|L7L7L7",
                            "....L7.F7||L7|.L7L7|",
                            ".....|FJLJ|FJ|F7|.LJ",
                            "....FJL-7.||.||||...",
                            "....L---J.LJ.LJLJ..."], 8)])
def test_count_inside_loop(test_input, expected):
    # Given
    # When
    result = count_inside_loop(test_input)
    # Then
    assert result == expected
