from collections import Counter
from functools import cmp_to_key

import pytest

from main import part1, part2, parse_hands, Hand, get_total_winnings, compare_hands, \
    get_counter_added_joker, CARD_VALUE_JOKER, CARD_VALUE

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
    assert result == 5905


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


@pytest.mark.parametrize("test_input",
                         [(Hand("32T3K", 765), Hand("KTJJT", 220)),
                          (Hand("32T3K", 765), Hand("KK677", 28)),
                          (Hand("32T3K", 765), Hand("T55J5", 684)),
                          (Hand("32T3K", 765), Hand("QQQJA", 483)),
                          (Hand("KTJJT", 220), Hand("KK677", 28)),
                          (Hand("KTJJT", 220), Hand("T55J5", 684)),
                          (Hand("KTJJT", 220), Hand("QQQJA", 483)),
                          (Hand("KK677", 28), Hand("T55J5", 684)),
                          (Hand("KK677", 28), Hand("QQQJA", 483)),
                          (Hand("T55J5", 684), Hand("QQQJA", 483))])
def test_compare_hands(test_input):
    # Given
    hand1, hand2 = test_input
    # When
    result = compare_hands(hand1, hand2, Counter, CARD_VALUE)
    # Then
    assert result < 0


def test_sort_hands():
    # Given
    hands = [Hand("32T3K", 765), Hand("T55J5", 684), Hand("KK677", 28), Hand("KTJJT", 220), Hand("QQQJA", 483)]
    # When
    hands.sort(key=cmp_to_key(lambda hand1, hand2: compare_hands(hand1, hand2, Counter, CARD_VALUE)))
    # Then
    assert hands == [Hand("32T3K", 765), Hand("KTJJT", 220), Hand("KK677", 28), Hand("T55J5", 684), Hand("QQQJA", 483)]


def test_total_winnings():
    # Given
    hands = [Hand("32T3K", 765), Hand("T55J5", 684), Hand("KK677", 28), Hand("KTJJT", 220), Hand("QQQJA", 483)]
    # When
    result = get_total_winnings(hands, Counter, CARD_VALUE)
    # Then
    assert result == 6440


@pytest.mark.parametrize("test_input, expected",
                         [("T55J5", "T5555"), ("KTJJT", "KTTTT"), ("QQQJA", "QQQQA"), ("JJJJJ", "JJJJJ")])
def test_get_counter_added_joker(test_input, expected):
    # Given
    # When
    counter = get_counter_added_joker(test_input)
    # Then
    assert counter == Counter(expected)


@pytest.mark.parametrize("test_input",
                         [(Hand("32T3K", 765), Hand("KK677", 28)),
                          (Hand("32T3K", 765), Hand("T55J5", 684)),
                          (Hand("32T3K", 765), Hand("QQQJA", 483)),
                          (Hand("32T3K", 765), Hand("KTJJT", 220)),
                          (Hand("KK677", 28), Hand("T55J5", 684)),
                          (Hand("KK677", 28), Hand("QQQJA", 483)),
                          (Hand("KK677", 28), Hand("KTJJT", 220)),
                          (Hand("T55J5", 684), Hand("QQQJA", 483)),
                          (Hand("T55J5", 684), Hand("KTJJT", 220)),
                          (Hand("QQQJA", 483), Hand("KTJJT", 220))])
def test_compare_hands_joker(test_input):
    # Given
    hand1, hand2 = test_input
    # When
    result = compare_hands(hand1, hand2, get_counter_added_joker, CARD_VALUE_JOKER)
    # Then
    assert result < 0
