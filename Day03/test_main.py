import pytest

from main import part1, part2, find_part_numbers, is_symbol, is_part_number

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 4361


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 0


def test_find_part_numbers_no_symbol():
    # Given
    rows = [".467."]
    # When
    result = find_part_numbers(rows)
    # Then
    assert result == []


def test_find_part_numbers_single_part_number():
    # Given
    rows = [".467#"]
    # When
    result = find_part_numbers(rows)
    # Then
    assert result == [467]


def test_find_part_numbers_multiple_part_number():
    # Given
    rows = [".467#890."]
    # When
    result = find_part_numbers(rows)
    # Then
    assert result == [467, 890]


def test_find_part_numbers_last_column():
    # Given
    rows = ["....", "#467", "...."]
    # When
    result = find_part_numbers(rows)
    # Then
    assert result == [467]


def test_is_part_number_not_part_number():
    # Given
    rows = [".....", ".467.", "....."]
    # When
    result = is_part_number(1, 1, 3, rows)
    # Then
    assert result is False


@pytest.mark.parametrize("test_input", ["$....", ".$...", "..$..", "...$.", "....$"])
def test_is_part_number_symbol_above(test_input):
    # Given
    rows = [test_input, ".467.", "....."]
    # When
    result = is_part_number(1, 1, 3, rows)
    # Then
    assert result is True


@pytest.mark.parametrize("test_input", ["$....", ".$...", "..$..", "...$.", "....$"])
def test_is_part_number_symbol_below(test_input):
    # Given
    rows = [".....", ".467.", test_input]
    # When
    result = is_part_number(1, 1, 3, rows)
    # Then
    assert result is True


def test_is_part_number_symbol_on_left():
    # Given
    rows = [".....", "#467.", "....."]
    # When
    result = is_part_number(1, 1, 3, rows)
    # Then
    assert result is True


def test_is_part_number_symbol_on_right():
    # Given
    rows = [".....", ".467#", "....."]
    # When
    result = is_part_number(1, 1, 3, rows)
    # Then
    assert result is True


def test_is_part_number_first_row():
    # Given
    rows = [".467#", "....."]
    # When
    result = is_part_number(0, 1, 3, rows)
    # Then
    assert result is True


def test_is_part_number_last_row():
    # Given
    rows = [".....", ".467#"]
    # When
    result = is_part_number(1, 1, 3, rows)
    # Then
    assert result is True


def test_is_part_number_first_column():
    # Given
    rows = ["....", "467#", "...."]
    # When
    result = is_part_number(1, 0, 2, rows)
    # Then
    assert result is True


def test_is_part_number_last_column():
    # Given
    rows = ["....", "#467", "...."]
    # When
    result = is_part_number(1, 1, 3, rows)
    # Then
    assert result is True


def test_is_part_number_not_part_number_last_column():
    # Given
    rows = ["....", ".467", "...."]
    # When
    result = is_part_number(1, 1, 3, rows)
    # Then
    assert result is False


@pytest.mark.parametrize("test_input,expected", [('1', False), ('.', False), ('#', True), ('$', True)])
def test_is_symbol(test_input, expected):
    # Given
    # When
    result = is_symbol(test_input)
    # Then
    assert result is expected
