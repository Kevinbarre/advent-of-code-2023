from main import part1, part2, parse_cards, Card, get_points, get_amount_of_each_card

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
    assert result == 30


def test_parse_cards():
    # Given
    lines = ["Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"]
    # When
    cards = parse_cards(lines)
    # Then
    assert len(cards) == 1
    assert cards[0].id == 1
    assert cards[0].winning_numbers == {41, 48, 83, 86, 17}
    assert cards[0].numbers == {83, 86, 6, 31, 17, 9, 48, 53}


def test_get_number_of_win():
    # Given
    card = Card(1, {41, 48, 83, 86, 17}, {83, 86, 6, 31, 17, 9, 48, 53})
    # When
    result = card.get_number_of_win()
    # Then
    assert result == 4


def test_get_points_loosing_card():
    # Given
    card = Card(5, {87, 83, 26, 28, 32}, {88, 30, 70, 12, 93, 22, 82, 36})
    # When
    result = get_points(card)
    # Then
    assert result == 0


def test_get_points_winning_card():
    # Given
    card = Card(1, {41, 48, 83, 86, 17}, {83, 86, 6, 31, 17, 9, 48, 53})
    # When
    result = get_points(card)
    # Then
    assert result == 8


def test_get_amount_of_each_card():
    # Given
    # Card 1 makes us win one copy of card 2 and one of card 3
    card1 = Card(1, {1, 2}, {1, 2})
    # Card 2 makes us win one copy of card 3
    card2 = Card(2, {1}, {1})
    # Card 3 does not make us win anymore card
    card3 = Card(3, {1}, {2})
    # When
    result = get_amount_of_each_card([card1, card2, card3])
    # Then
    assert result == {1: 1, 2: 2, 3: 4}
