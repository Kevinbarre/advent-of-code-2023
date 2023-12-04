from main import part1, part2, parse_cards, Card, get_points

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 13


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 0


def test_parse_cards():
    # Given
    lines = ["Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"]
    # When
    cards = parse_cards(lines)
    # Then
    assert len(cards) == 1
    assert cards[0].winning_numbers == {41, 48, 83, 86, 17}
    assert cards[0].numbers == {83, 86, 6, 31, 17, 9, 48, 53}


def test_get_number_of_win():
    # Given
    card = Card({41, 48, 83, 86, 17}, {83, 86, 6, 31, 17, 9, 48, 53})
    # When
    result = card.get_number_of_win()
    # Then
    assert result == 4


def test_get_points_loosing_card():
    # Given
    card = Card({87, 83, 26, 28, 32}, {88, 30, 70, 12, 93, 22, 82, 36})
    # When
    result = get_points(card)
    # Then
    assert result == 0


def test_get_points_winning_card():
    # Given
    card = Card({41, 48, 83, 86, 17}, {83, 86, 6, 31, 17, 9, 48, 53})
    # When
    result = get_points(card)
    # Then
    assert result == 8
