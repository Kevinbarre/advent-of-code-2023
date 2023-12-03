import pytest

from main import part1, part2, calibration_value

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.readlines()
    # When
    result = part1(lines)
    # Then
    assert result == 142


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.readlines()
    # When
    result = part2(lines)
    # Then
    assert result == 0


@pytest.mark.parametrize("test_input,expected",
                         [("1abc2", 12), ("pqr3stu8vwx", 38), ("a1b2c3d4e5f", 15), ("treb7uchet", 77)])
def test_calibration_value(test_input, expected):
    # Given
    # When
    result = calibration_value(test_input)
    # Then
    assert result == expected
