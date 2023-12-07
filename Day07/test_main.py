from main import part1, part2, parse_hands, Hand, get_total_winnings

filename = "example.txt"


def test_part1():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part1(lines)
    # Then
    assert result == 6440


def test_part2():
    # Given
    with open(filename) as f:
        lines = f.read().splitlines()
    # When
    result = part2(lines)
    # Then
    assert result == 0


def test_parse_hands():
    # Given
    lines = ["32T3K 765", "T55J5 684"]
    # When
    result = parse_hands(lines)
    # Then
    assert len(result) == 2
    assert result[0].cards == "32T3K"
    assert result[0].bid == 765
    assert result[1].cards == "T55J5"
    assert result[1].bid == 684


def test_sort_hands():
    # Given
    hands = [Hand("32T3K", 765), Hand("T55J5", 684), Hand("KK677", 28), Hand("KTJJT", 220), Hand("QQQJA", 483)]
    # When
    hands.sort()
    # Then
    assert hands == [Hand("32T3K", 765), Hand("KTJJT", 220), Hand("KK677", 28), Hand("T55J5", 684), Hand("QQQJA", 483)]


def test_hand_lt():
    # Given
    hand1 = Hand("32T3K", 765)
    hand2 = Hand("KTJJT", 220)
    hand3 = Hand("KK677", 28)
    hand4 = Hand("T55J5", 684)
    hand5 = Hand("QQQJA", 483)
    # When
    # Then
    assert hand1 < hand2
    assert hand1 < hand3
    assert hand1 < hand4
    assert hand1 < hand5
    assert hand2 < hand3
    assert hand2 < hand4
    assert hand2 < hand5
    assert hand3 < hand4
    assert hand3 < hand5
    assert hand4 < hand5


def test_total_winnings():
    # Given
    hands = [Hand("32T3K", 765), Hand("T55J5", 684), Hand("KK677", 28), Hand("KTJJT", 220), Hand("QQQJA", 483)]
    # When
    result = get_total_winnings(hands)
    # Then
    assert result == 6440
