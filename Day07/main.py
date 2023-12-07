from collections import Counter
from functools import cmp_to_key

CARD_VALUE = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 11,
    'Q': 12,
    'K': 13,
    'A': 14
}

CARD_VALUE_JOKER = {
    'J': 1,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'Q': 12,
    'K': 13,
    'A': 14
}


def part1(lines):
    hands = parse_hands(lines)
    return get_total_winnings(hands, Counter, CARD_VALUE)


def part2(lines):
    hands = parse_hands(lines)
    return get_total_winnings(hands, get_counter_added_joker, CARD_VALUE_JOKER)


class Hand:
    def __init__(self, cards, bid):
        self.cards = cards
        self.bid = bid

    def __repr__(self):
        return "Hand(cards=%r, bid=%r)" % (self.cards, self.bid)

    def __eq__(self, other):
        return self.cards == other.cards and self.bid == other.bid


def compare_hands(hand1, hand2, get_counter, card_value):
    hand1_cards_occurrence = sorted(get_counter(hand1.cards).values(), reverse=True)
    hand2_cards_occurrence = sorted(get_counter(hand2.cards).values(), reverse=True)
    # Compare types first
    for hand1_nb, hand2_nb in zip(hand1_cards_occurrence, hand2_cards_occurrence):
        if hand1_nb != hand2_nb:
            return hand1_nb - hand2_nb
    # Same hand type, compare by cards order
    for hand1_card, hand2_card in zip(hand1.cards, hand2.cards):
        hand1_card_value = card_value[hand1_card]
        hand2_card_value = card_value[hand2_card]
        if hand1_card_value != hand2_card_value:
            return hand1_card_value - hand2_card_value


def get_counter_added_joker(cards):
    counter = Counter(cards)
    if 'J' in counter:
        nb_joker = counter['J']
        if nb_joker != 5:  # Handle case when cards are Five of a kind of jokers
            del counter['J']
            biggest = max(counter, key=counter.get)
            counter[biggest] += nb_joker
    return counter


def parse_hands(lines):
    hands = []
    for line in lines:
        cards, raw_bid = line.split()
        hands.append(Hand(cards, int(raw_bid)))
    return hands


def get_total_winnings(hands, get_counter, card_value):
    hands.sort(key=cmp_to_key(lambda hand1, hand2: compare_hands(hand1, hand2, get_counter, card_value)))
    return sum((i + 1) * hand.bid for i, hand in enumerate(hands))


if __name__ == '__main__':
    with open("input.txt") as f:
        f_lines = f.read().splitlines()

    print("Part 1 : ", part1(f_lines))
    print("Part 2 : ", part2(f_lines))
