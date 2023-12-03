import pytest

from main import part1, part2, calibration_value, convert_to_digit, calibration_value_with_letters

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
    with open("example2.txt") as f:
        lines = f.readlines()
    # When
    result = part2(lines)
    # Then
    assert result == 281


@pytest.mark.parametrize("test_input,expected",
                         [("1abc2", 12), ("pqr3stu8vwx", 38), ("a1b2c3d4e5f", 15), ("treb7uchet", 77)])
def test_calibration_value(test_input, expected):
    # Given
    # When
    result = calibration_value(test_input)
    # Then
    assert result == expected


@pytest.mark.parametrize("test_input,expected",
                         [("two1nine", 29), ("eightwothree", 83), ("abcone2threexyz", 13), ("xtwone3four", 24),
                          ("4nineeightseven2", 42), ("zoneight234", 14), ("7pqrstsixteen", 76), ("eighthree", 83),
                          ("sevenine", 79)])
def test_calibration_value_with_letters(test_input, expected):
    # Given
    # When
    result = calibration_value_with_letters(test_input)
    # Then
    assert result == expected


@pytest.mark.parametrize("test_input,expected",
                         [("1", "1"), ("one", "1")])
def test_convert_to_digit(test_input, expected):
    # Given
    # When
    result = convert_to_digit(test_input)
    # Then
    assert result == expected
