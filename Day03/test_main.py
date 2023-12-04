import pytest

from main import part1, part2, find_part_numbers, is_symbol, is_part_number, is_gear_symbol, is_gear, get_part_number, \
    find_gear_ratios

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
    assert result == 467835


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


@pytest.mark.parametrize("test_input,expected", [('1', False), ('.', False), ('#', False), ('*', True)])
def test_is_gear_symbol(test_input, expected):
    # Given
    # When
    result = is_gear_symbol(test_input)
    # Then
    assert result is expected


@pytest.mark.parametrize("test_input", ["435", ".435", "435.", ".435."])
def test_get_part_number(test_input):
    # Given
    i = 1
    # When
    result = get_part_number(test_input, i)
    # Then
    assert result == 435


def test_get_part_number_first_column():
    # Given
    row = "2.3"
    i = 0
    # When
    result = get_part_number(row, i)
    # Then
    assert result == 2


def test_get_part_number_last_column():
    # Given
    row = "2.3"
    i = 2
    # When
    result = get_part_number(row, i)
    # Then
    assert result == 3


def test_is_gear_single_star():
    # Given
    rows = ["*"]
    # When
    result = is_gear(0, 0, rows)
    # Then
    assert result is False


def test_is_gear_single_number():
    # Given
    rows = ["1*."]
    # When
    result = is_gear(0, 1, rows)
    # Then
    assert result is False


def test_is_gear_two_numbers():
    # Given
    rows = ["2*3"]
    # When
    result = is_gear(0, 1, rows)
    # Then
    assert result == 6


def test_is_gear_two_numbers_above():
    # Given
    rows = ["2.3", ".*.", "..."]
    # When
    result = is_gear(1, 1, rows)
    # Then
    assert result == 6


def test_is_gear_two_numbers_below():
    # Given
    rows = ["...", ".*.", "2.3"]
    # When
    result = is_gear(1, 1, rows)
    # Then
    assert result == 6


def test_is_gear_two_numbers_above_below():
    # Given
    rows = ["2..", ".*.", "..3"]
    # When
    result = is_gear(1, 1, rows)
    # Then
    assert result == 6


def test_is_gear_large_numbers():
    # Given
    rows = ["....283", "341*..."]
    # When
    result = is_gear(1, 3, rows)
    # Then
    assert result == 96503


def test_find_gear_ratios():
    # Given
    rows = ["2..", ".*.", "..3"]
    # When
    result = find_gear_ratios(rows)
    # Then
    assert result == [6]
