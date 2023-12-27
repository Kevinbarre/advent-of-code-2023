import pytest

from main import part1, part2, parse_hailstones, Hailstone

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines, 7, 27)
    # Then
    assert result == 2


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 0


def test_parse_hailstones():
    # Given
    lines = ["19, 13, 30 @ -2,  1, -2",
             "18, 19, 22 @ -1, -1, -2",
             "20, 25, 34 @ -2, -2, -4",
             "12, 31, 28 @ -1, -2, -1",
             "20, 19, 15 @  1, -5, -3"]
    # When
    result = parse_hailstones(lines)
    # Then
    assert len(result) == 5
    assert result[0] == Hailstone(19, 13, 30, -2, 1, -2)
    assert result[1] == Hailstone(18, 19, 22, -1, -1, -2)
    assert result[2] == Hailstone(20, 25, 34, -2, -2, -4)
    assert result[3] == Hailstone(12, 31, 28, -1, -2, -1)
    assert result[4] == Hailstone(20, 19, 15, 1, -5, -3)


@pytest.mark.parametrize("hailstone_1, hailstone_2, expected", [
    (Hailstone(19, 13, 30, -2, 1, -2), Hailstone(18, 19, 22, -1, -1, -2), True),
    (Hailstone(19, 13, 30, -2, 1, -2), Hailstone(20, 25, 34, -2, -2, -4), True),
    (Hailstone(19, 13, 30, -2, 1, -2), Hailstone(12, 31, 28, -1, -2, -1), False),
    (Hailstone(19, 13, 30, -2, 1, -2), Hailstone(20, 19, 15, 1, -5, -3), False),
    (Hailstone(18, 19, 22, -1, -1, -2), Hailstone(20, 25, 34, -2, -2, -4), False),
    (Hailstone(18, 19, 22, -1, -1, -2), Hailstone(12, 31, 28, -1, -2, -1), False),
    (Hailstone(18, 19, 22, -1, -1, -2), Hailstone(20, 19, 15, 1, -5, -3), False),
    (Hailstone(20, 25, 34, -2, -2, -4), Hailstone(12, 31, 28, -1, -2, -1), False),
    (Hailstone(20, 25, 34, -2, -2, -4), Hailstone(20, 19, 15, 1, -5, -3), False),
    (Hailstone(12, 31, 28, -1, -2, -1), Hailstone(20, 19, 15, 1, -5, -3), False)])
def test_intersect_hailstones(hailstone_1, hailstone_2, expected):
    # Given
    # When
    result = hailstone_1.intersect_xy(hailstone_2, 7, 27)
    # Then
    assert result is expected
