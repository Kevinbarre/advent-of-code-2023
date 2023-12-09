import pytest

from main import part1, part2, parse_sequences, compute_differences, get_all_differences, get_next_value, \
    get_previous_value

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 114


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 2


def test_parse_sequences():
    # Given
    lines = ["0 3 6 9 12 15", "1 3 6 10 15 21", "10 13 16 21 30 45"]
    # When
    result = parse_sequences(lines)
    # Then
    assert result == [[0, 3, 6, 9, 12, 15], [1, 3, 6, 10, 15, 21], [10, 13, 16, 21, 30, 45]]


def test_compute_differences():
    # Given
    sequence = [0, 3, 6, 9, 12, 15]
    # When
    result = compute_differences(sequence)
    # Then
    assert result == [3, 3, 3, 3, 3]


def test_get_all_differences():
    # Given
    sequence = [10, 13, 16, 21, 30, 45]
    # When
    result = get_all_differences(sequence)
    # Then
    assert result == [[3, 3, 5, 9, 15], [0, 2, 4, 6], [2, 2, 2], [0, 0]]


def test_get_next_value():
    # Given
    sequence = [10, 13, 16, 21, 30, 45]
    # When
    result = get_next_value(sequence)
    # Then
    assert result == 68


@pytest.mark.parametrize("test_input, expected",
                         [([0, 3, 6, 9, 12, 15], -3), ([1, 3, 6, 10, 15, 21], 0), ([10, 13, 16, 21, 30, 45], 5)])
def test_get_previous_value(test_input, expected):
    # Given
    # When
    result = get_previous_value(test_input)
    # Then
    assert result == expected
