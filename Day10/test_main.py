import pytest

from main import part1, part2, parse_tiles, get_start_position, find_connected_pipes, navigate, get_farthest_distance

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


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 0


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
